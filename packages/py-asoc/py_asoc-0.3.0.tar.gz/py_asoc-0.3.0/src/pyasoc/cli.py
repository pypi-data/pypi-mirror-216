import csv
import shlex
from pprint import pprint
from tempfile import NamedTemporaryFile
from typing import TextIO

from cloup import (
    Choice,
    File,
    Path,
    argument,
    group,
    option,
    option_group,
    pass_context,
)
from cloup.constraints import require_one

from .asoc import Asoc, IssueLevels


@group(context_settings={"help_option_names": ["-h", "--help"]}, chain=True)
@option_group(
    "Application",
    option("-a", "--app-id", help="ASOC App ID", type=str),
    option("-an", "--app-name", help="ASOC App Name", type=str),
    constraint=require_one,
)
@option("-k", "--key-id", help="ASOC Key ID", type=str, required=True)
@option("-s", "--key-secret", help="ASOC Key Secret", type=str, required=True)
@option("-n", "--scan-name", help="Scan Name", type=str, default="main", show_default=True)
@option("--asset-group-id", help="Asset Group ID (defaults to Default Asset Group)", type=str)
@option(
    "-bi",
    "--business-impact",
    type=Choice(
        [
            "Unspecified",
            "Low",
            "Medium",
            "High",
            "Critical",
        ],
        case_sensitive=False,
    ),
    default="Low",
    show_default=True,
)
@pass_context
def cli(
    ctx,
    app_id,
    app_name,
    key_id,
    key_secret,
    scan_name,
    asset_group_id,
    business_impact,
):
    asoc = Asoc(
        key_id=key_id,
        key_secret=key_secret,
        app_id=app_id,
        scan_name=scan_name,
        app_name=app_name,
        asset_group_id=asset_group_id,
    )
    ctx.ensure_object(dict)
    ctx.obj["asoc"] = asoc


@cli.command()
@pass_context
@argument("directory", type=Path(resolve_path=True, exists=True, file_okay=False, writable=True))
@option("-pa", "--packager-args", default="")
@option("--packager", default="appscan.sh", show_default=True)
@option("--comment", default="", show_default=True, help="Comment for new scan")
@option("--personal", is_flag=True, default=False, show_default=True, help="Personal scan")
def scan(ctx, directory, packager_args, packager, comment, personal):
    asoc: Asoc = ctx.obj["asoc"]
    asoc.create_scan(
        directory,
        packager=packager,
        extra_options=shlex.split(packager_args),
        comment=comment,
        personal=personal,
    )


@cli.command()
@pass_context
@option("-tm", "--timeout-minutes", default=60, show_default=True)
def wait(ctx, timeout_minutes: int = 60):
    asoc: Asoc = ctx.obj["asoc"]
    pprint(asoc.wait(timeout_minutes=timeout_minutes))


@cli.command()
@pass_context
@argument(
    "output_file",
    type=File("w", encoding="utf-8"),
    default="-",
)
def status_badge(ctx, output_file: TextIO):
    asoc: Asoc = ctx.obj["asoc"]
    asoc.write_status_badge(output_file)


@cli.command()
@pass_context
@argument(
    "output_file",
    type=File("w", encoding="utf-8"),
    default="-",
)
@option(
    "--cutoff-level",
    type=Choice([a.value for a in IssueLevels], case_sensitive=False),
    default="medium",
    help="count issues of this status and higher",
    show_default=True,
)
def num_issues_badge(ctx, output_file: TextIO, cutoff_level: str):
    asoc: Asoc = ctx.obj["asoc"]
    asoc.write_num_issues_badge(output_file, cutoff_level=cutoff_level)


@cli.command()
@pass_context
@argument(
    "directory",
    type=Path(
        resolve_path=True,
        exists=True,
        file_okay=False,
        writable=True,
        path_type=Path,
    ),
    default=".",
)
def upload_external(ctx, directory):
    asoc: Asoc = ctx.obj["asoc"]

    new, fix, reopen, stay_open = asoc.filter_issues(directory.glob("*.json"))

    if fix:
        print(f"Marking {len(fix)} issues as fixed")
        asoc.change_issue_status_bulk([a.id for a in fix], "Fixed")
    if reopen:
        print(f"Marking {len(reopen)} issues as reopened")
        asoc.change_issue_status_bulk([a.id for a in reopen], "Reopened")
    if stay_open:
        print(f"Leaving {len(stay_open)} issues as still open")
        # print(asoc.change_issue_status_bulk([a.id for a in stay_open], "Open"))

    if new:
        print(f"Adding {len(new)} new issues")
        fieldnames = []
        for v in new:
            for k in v.keys():
                if k not in fieldnames:
                    fieldnames.append(k)
        with NamedTemporaryFile(suffix=".csv", mode="w+t", encoding="utf8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect="excel")
            writer.writeheader()
            for v in new:
                writer.writerow(v)
            csvfile.flush()
            csvfile.seek(0)
            out = asoc.import_file(csvfile.name)
        print(out)
