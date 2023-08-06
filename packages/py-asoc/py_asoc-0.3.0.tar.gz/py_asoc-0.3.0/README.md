# Appscan on Cloud Python API

Generated initially from Appscan on Cloud (
ASOC) [swagger spec](https://cloud.appscan.com/swagger/index.html), added various functionality and
CLI interface.

## CLI

### Install

#### Requirements

-   ASOC CLI on the path
    -   https://help.hcltechsw.com/appscan/ASoC/src_utility_install.html
-   Node.js >= 14 if you want the ability to generate badges
    -   https://nodejs.org/en/download
    -   Also, prefer to pre-install badge-maker: `npm install badge-maker`

```shell
pip install py-asoc

# or for badges
pip install py-asoc[badges]
```

### Run

```
Usage: asoc [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  -a, --app_id TEXT      ASOC App ID  [required]
  -k, --key_id TEXT      ASOC Key ID  [required]
  -s, --key_secret TEXT  ASOC Key Secret  [required]
  -n, --scan_name TEXT   Scan Name  [default: main]
  -h, --help             Show this message and exit.

Commands:
  num-issues-badge
  scan
  status-badge
  upload-external
  wait
```

#### scan

creates an IRX package and uploads it to ASOC, then either creates a new scan or starts an existing
one.

#### upload-external

Uploads any json files in the givven directory to ASOC as external issues.

#### wait

waits for the scan to finish.

#### status-badge

generates a badge for the application risk level

#### num-issues-badge

generates a badge for the number of unresolved issues for the application
