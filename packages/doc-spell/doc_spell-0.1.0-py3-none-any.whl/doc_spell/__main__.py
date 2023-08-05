"""
Demonstrates pydevkit features.

EPILOG:
Example 1:
```
PYDEVKIT_LOG_HANDLER=app ./script --log-level=debug
```

Example 2:
```
./script --log-level=debug --log-handler=json
```
"""


import pydevkit.log.config  # noqa: F401
from pydevkit.log import prettify
from pydevkit.argparse import ArgumentParser
import yaml
import os
from yaml.loader import SafeLoader
from .cspell import spell_checker
from . import __version__

import sys
import logging

log = logging.getLogger(__name__)

CONFIG = ".doc-spell.yml"


def get_args():
    p = ArgumentParser(help=__doc__, version=__version__)
    p.add_argument("-c", help="configuration file", dest="config", default=CONFIG)
    p.add_argument("files", help="files to check", nargs="+")

    return p.parse_known_args()


def main():
    args, unknown_args = get_args()
    if unknown_args:
        log.warning("Unknown arguments: %s", unknown_args)
        sys.exit(1)
    log.info("reading configuration from `%s`", args.config)
    try:
        path = os.path.expanduser(args.config)
        conf = yaml.load(open(path, "r"), Loader=SafeLoader)
    except Exception as exp:
        log.error("%s", exp)
        conf = {}
    log.debug("config: %s", prettify(conf))
    rc = 0
    for f in args.files:
        try:
            spell_checker(f, conf)
        except Exception as exp:
            log.error("%s", exp)
            rc = 1
    return rc


if __name__ == "__main__":
    main()
