#!/usr/bin/env python3
import argparse

import settings as st

from class_xmltv import XMLTV
# parse arguments
parser = argparse.ArgumentParser(description='xmltv time-tool')
parser.add_argument('--xmltv_link_arch', '-a',
        type=str,
        default=st.list_archives_tvprogram_link[0],
        help='link of archive with xmltv'
        )
parser.add_argument('--force_download', '-f',
        type=int,
        default = 0,
        help='force download archive even exist. 0 - disabled, 1 - enabled'
        )
parser.add_argument('--timezone', '-t',
        type=int,
        default = 3,
        help='timezone from GMT (wo +)',
        )
parser.add_argument('--target_minutes_ending', '-e',
        type=int,
        default = 5,
        help='minutes to end show'
        )
parser.add_argument('--target_minutes_begining', '-b',
        type=int,
        default = 10,
        help='minutes to begin show'
        )
parser.add_argument('--use_m3u', '-p',
        type=int,
        default=0,
        help='Use m3u playlist file. 0 - disabled, 1 - enabled'
        )
parser.add_argument('--html_out', '-ht',
        type=int,
        default=0,
        help='Use html out. 0 - disabled, 1 - enabled'
        )
args = parser.parse_args()

# defs
opts = {
        'xmltv_link_arch': args.xmltv_link_arch,
        'force_download': True if args.force_download == 1 else False,
        'timezone': int(args.timezone),
        'target_minutes_ending': int(args.target_minutes_ending),
        'target_minutes_begining': int(args.target_minutes_begining),
        'use_m3u': True if args.use_m3u == 1 else False,
        'html_out': True if args.html_out == 1 else False
}


if __name__ == "__main__":
    xmltv = XMLTV(opts)
    xmltv.start()
    xmltv.get_shows()