import json
import os
import subprocess  # nosec: B404
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timedelta
from os import PathLike
from pathlib import Path
from typing import Iterable, TextIO

from javascript import require
from pytz import utc

from .api.account_api import AccountApi
from .api.apps_api import AppsApi
from .api.file_upload_api import FileUploadApi
from .api.issues_api import IssuesApi
from .api.scans_api import ScansApi
from .api_client import ApiClient
from .configuration import Configuration
from .models import (
    AppScanSaaSModelsV2MinScanData,
    AppScanSaaSModelsV2ScanExecution,
    AppScanSaaSModelsV2StaticAnalyzerScan,
    CommonModelsASMModelsApplicationModel,
    SystemWebHttpODataPageResultUtilitiesIssueModel,
    UserSiteCommonModelsApiKey,
    UserSiteCommonModelsNewStaticAnalyzerScan,
    UserSiteCommonModelsScanExecute,
    UtilitiesIssueModel,
    UtilitiesUpdateIssue,
)


@contextmanager
def cd(path: str | PathLike):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


def parse_issue(issue):
    ret = {
        "External Id": issue["id"],
        # "Issue Type": ,
        "Location": f'{issue["location"]["file"]} ({issue["location"]["start_line"]})',
        "Severity": issue["severity"],
        # "Context": ,
        "CVE": issue["cve"],
        # "CVSS": ,
        # "Domain": ,
        # "Element": ,
        # "Host": ,
        "Line": issue["location"]["start_line"],
        # "Path": ,
        # "Port": ,
        "File Name": issue["location"]["file"],
    }
    if ret["Severity"] == "Info":
        ret["Severity"] = "Informational"
    desc = issue.get("description", "").strip().replace(",", "")
    msg = issue.get("message", "").strip().replace(",", "")
    if desc and msg:
        ret["Issue Type"] = msg
        ret["Context"] = desc
    elif desc:
        ret["Issue Type"] = desc
    elif msg:
        ret["Issue Type"] = msg
    ret["Issue Type"] = f'{issue["scanner"]["name"]}: {ret["Issue Type"]}'
    return ret


RISK_RATING_COLORS = {
    "Unknown": "blue",
    "Low": "brightgreen",
    "Medium": "yellow",
    "High": "orange",
    "Critical": "red",
}


class Asoc:
    def __init__(self, key_id, key_secret, app_id, scan_name="main"):
        self.scan_id = self.exec_id = None
        self.key_id = key_id
        self.key_secret = key_secret
        self.app_id = app_id
        self.scan_name = scan_name
        self._token_expires = datetime(1990, 1, 1, 1, 1).astimezone(utc)
        self._config = Configuration()
        self._config.api_key_prefix = {"Authorization": "Bearer"}
        if proxy := os.getenv("https_proxy", os.getenv("HTTPS_PROXY")):
            self._config.proxy = proxy
        self._client = ApiClient(configuration=self._config)
        self._config.refresh_api_key_hook = self._get_token

        self._account = AccountApi(api_client=self._client)
        self._issues = IssuesApi(api_client=self._client)
        self._scans = ScansApi(api_client=self._client)

    def _get_token(self, obj: Configuration):
        if self._token_expires > datetime.now().astimezone(utc):
            print("reusing token")
            return

        r = self._account.account_api_key_login(
            UserSiteCommonModelsApiKey(
                key_id=self.key_id,
                key_secret=self.key_secret,
            ),
            # _request_timeout=10,
        )
        obj.api_key["Authorization"] = r.token
        self._token_expires = r.expire

    def _new_scan_start(self, file_id, **kwargs) -> AppScanSaaSModelsV2StaticAnalyzerScan:
        return self._scans.scans_create_static_analyzer_scan(
            UserSiteCommonModelsNewStaticAnalyzerScan(
                app_id=self.app_id,
                application_file_id=file_id,
                scan_name=self.scan_name,
                enable_mail_notification=False,
                comment=kwargs.get("comment", ""),
                personal=kwargs.get("personal", False),
            )
        )

    def _old_scan_start(self, scan_id: str, file_id: str) -> AppScanSaaSModelsV2ScanExecution:
        return self._scans.scans_execute_scan_by_scanid(
            scan_id=scan_id, model=UserSiteCommonModelsScanExecute(file_id=file_id)
        )

    # region external issue handling
    def get_external_issues(self) -> list[UtilitiesIssueModel]:
        r: SystemWebHttpODataPageResultUtilitiesIssueModel
        r = self._issues.issues_get_issues_for_scope_by_scope_and_scopeid(
            scope="Application",
            scope_id=self.app_id,
            top=5000,
            filter="length(ExternalId) gt 1",
            # _request_timeout=10,
        )
        return r.items

    def filter_issues(self, files: Iterable[str | PathLike]):
        issues = {}
        for f in files:
            try:
                with open(f, encoding="utf8") as fh:
                    data = json.load(fh)
                    for v in data.get("vulnerabilities", []):
                        iss = parse_issue(v)
                        if iss["External Id"] not in issues:
                            issues[iss["External Id"]] = iss
                        # break
            except (json.JSONDecodeError, KeyError):
                pass
        existing_issues = self.get_external_issues()
        existing_open: dict[str, UtilitiesIssueModel] = {
            a.external_id: a
            for a in existing_issues
            if a.status
            in (
                "Open",
                "Reopened",
                "New",
            )
        }
        existing_fixed: dict[str, UtilitiesIssueModel] = {
            a.external_id: a for a in existing_issues if a.status in ("Fixed",)
        }
        existing_passed: dict[str, UtilitiesIssueModel] = {
            a.external_id: a
            for a in existing_issues
            if a.status
            in (
                "Passed",
                "Noise",
            )
        }

        new_issues: list[dict] = []
        to_fix: list[UtilitiesIssueModel] = []
        to_reopen: list[UtilitiesIssueModel] = []
        stay_open: list[UtilitiesIssueModel] = []
        for eid, v in issues.items():
            if eid in existing_open:
                # is already open
                stay_open.append(existing_open.pop(eid))
            elif eid in existing_fixed:
                # need to reopen
                to_reopen.append(existing_fixed.pop(eid))
            elif eid in existing_passed:
                # has been changed to passed or fixed, ignore
                pass
            else:
                new_issues.append(v)
        for v in existing_open.values():
            to_fix.append(v)
        return new_issues, to_fix, to_reopen, stay_open

    def change_issue_status(self, issue_id: str, status):
        self._issues.issues_update_issue_by_id(
            id=issue_id, issue_data=UtilitiesUpdateIssue(status=status)
        )

    def change_issue_status_bulk(self, issue_ids: list[str], status):
        all_ids = ":".join(issue_ids)
        return self._issues.issues_update_issues_for_scope_by_scope_and_scopeid(
            scope="Application",
            scope_id=self.app_id,
            issue_data=UtilitiesUpdateIssue(status=status),
            odata_filter=f"substringof(Id,'{all_ids}')",
        )
        # for ii in issue_ids:
        #     self.change_issue_status(ii, status)

    def import_file(self, file: str | bytes | PathLike):
        return self._issues.issues_import_file(
            file_to_upload=file, app_id=self.app_id, scan_name=self.scan_name
        )

    # endregion

    def upload_file(self, file: str | bytes | PathLike) -> str:
        fa = FileUploadApi(self._client)
        return fa.file_upload_upload(file_to_upload=file).file_id

    def get_app(self) -> CommonModelsASMModelsApplicationModel:
        aa = AppsApi(self._client)
        return aa.apps_get_app_by_id(self.app_id)

    def get_badge(self, output: None | PathLike | str = None):
        out = sys.stdout
        try:
            if output is not None:
                out = open(output, "w", encoding="utf8")
            self.write_badge(out)
            out.flush()
        finally:
            if output is not None:
                out.close()

    def write_badge(self, handle: TextIO):
        app_status = self.get_app()
        bm = require("badge-maker")
        handle.write(
            bm.makeBadge(
                {
                    "label": "AppScan Risk Rating",
                    "message": app_status.risk_rating,
                    "color": RISK_RATING_COLORS[app_status.risk_rating],
                    "style": "flat",
                }
            )
        )

    def scan_exists(self) -> bool | AppScanSaaSModelsV2MinScanData:
        q = self._scans.scans_get_scans_page2(
            filter=f"AppId eq Guid'{self.app_id}' and Name eq '{self.scan_name}'"
        )
        if len(q.items) == 0:
            return False
        return q.items[0]

    def get_scan(self, execution_id: str | None = None) -> AppScanSaaSModelsV2ScanExecution:
        if execution_id is None:
            if self.exec_id is None:
                execution_id = self.scan_exists().latest_execution.id
            else:
                execution_id = self.exec_id
        return self._scans.scans_execution_by_executionid(execution_id=execution_id)

    def package(
        self,
        working_dir: str | bytes | PathLike = ".",
        extra_options: None | list[str] = None,
        packager: str | bytes | PathLike = "appscan.sh",
    ):
        if extra_options is None:
            extra_options = []
        with cd(working_dir):
            subprocess.run(  # nosec: B603
                [packager, "prepare", "-n", self.scan_name + ".irx", *extra_options],
                check=True,
                stderr=sys.stderr,
                stdout=sys.stdout,
            )

    def create_scan(self, working_dir: str | bytes | PathLike = ".", **kwargs):
        with cd(working_dir):
            if not Path(self.scan_name + ".irx").exists():
                self.package(
                    working_dir=working_dir,
                    extra_options=kwargs.get("extra_options"),
                    packager=kwargs.get("packager", "appscan.sh"),
                )
            file_id = self.upload_file(self.scan_name + ".irx")
            if scan_info := self.scan_exists():
                scan_id = scan_info.id
                exec_info = self._old_scan_start(scan_id=scan_id, file_id=file_id)
                exec_id = exec_info.id
            else:
                exec_info = self._new_scan_start(file_id=file_id, **kwargs)
                exec_id = exec_info.latest_execution.id
                scan_id = exec_info.latest_execution.scan_id
        self.scan_id = scan_id
        self.exec_id = exec_id
        print(exec_id)
        return scan_id, exec_id

    def wait(self, interval: int = 10, timeout_minutes: int = 60):
        start = datetime.now()
        while True:
            scan_info = self.get_scan()
            print(scan_info.id)
            if scan_info.status in ("Ready", "Failed"):
                break
            if datetime.now() - start > timedelta(minutes=timeout_minutes):
                raise TimeoutError("Scan timed out")
            time.sleep(interval)
        return scan_info
