import csv
import shlex
from pathlib import Path
from pprint import pprint
from tempfile import NamedTemporaryFile
from typing import TextIO

import click

from .asoc import Asoc


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, chain=True)
@click.option("-a", "--app_id", help="ASOC App ID", type=str, required=True)
@click.option("-k", "--key_id", help="ASOC Key ID", type=str, required=True)
@click.option("-s", "--key_secret", help="ASOC Key Secret", type=str, required=True)
@click.option("-n", "--scan_name", help="Scan Name", type=str, default="main", show_default=True)
@click.pass_context
def cli(ctx, app_id, key_id, key_secret, scan_name):
    asoc = Asoc(key_id=key_id, key_secret=key_secret, app_id=app_id, scan_name=scan_name)
    ctx.ensure_object(dict)
    ctx.obj["asoc"] = asoc


@cli.command()
@click.pass_context
@click.argument(
    "directory", type=click.Path(resolve_path=True, exists=True, file_okay=False, writable=True)
)
@click.option("-pa", "--packager_args", default="")
@click.option("--packager", default="appscan.sh", show_default=True)
@click.option("--comment", default="", show_default=True, help="Comment for new scan")
@click.option("--personal", is_flag=True, default=False, show_default=True, help="Personal scan")
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
@click.pass_context
def wait(ctx):
    asoc: Asoc = ctx.obj["asoc"]
    pprint(asoc.wait())


@cli.command()
@click.pass_context
@click.argument("file", type=click.File("w", encoding="utf-8"), default="-")
def create_badge(ctx, file: TextIO):
    asoc: Asoc = ctx.obj["asoc"]
    asoc.write_badge(file)


@cli.command()
@click.pass_context
@click.argument(
    "directory",
    type=click.Path(
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
