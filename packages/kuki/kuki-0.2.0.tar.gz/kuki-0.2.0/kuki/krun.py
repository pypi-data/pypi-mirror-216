import argparse
import logging

from . import profile_util

FORMAT = "%(asctime)s %(levelname)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATE_FORMAT)

logger = logging.getLogger()

parser = argparse.ArgumentParser(description="K RUN CLI")

group = parser.add_mutually_exclusive_group()

group.add_argument(
    "--profile",
    nargs="?",
    default="default",
    help="start kdb process using profile",
)

group.add_argument(
    "--config",
    nargs="?",
    default="default",
    help="config kdb process",
)

parser.add_argument(
    "-b",
    "--blocked",
    action="store_true",
    default=False,
    help="block write-access for any handle context",
)

parser.add_argument(
    "-r",
    "--replicate",
    default="",
    help="replicate from :host:port",
)

parser.add_argument(
    "-u",
    "--disableSystemCmd",
    dest="disable_system_cmd",
    type=int,
    default=0,
    choices=[1],
    help="blocks system functions and file access",
)

parser.add_argument(
    "-i",
    "--init",
    action="store_true",
    default=False,
    help="initialize kest.json",
)

parser.add_argument(
    "-c",
    "--consoleSize",
    dest="console_size",
    nargs=2,
    default=[50, 160],
    type=int,
    help="console maximum rows and columns",
)


parser.add_argument(
    "-e",
    "--errorTraps",
    dest="error_traps",
    type=str,
    default="none",
    choices=["none", "suspend", "dump"],
    help="error-trapping mode",
)

parser.add_argument(
    "--tls",
    type=str,
    default="plain",
    choices=["plain", "mixed", "tls"],
    help="TLS server mode",
)

parser.add_argument(
    "-g",
    "--gc",
    dest="garbage_collection",
    type=str,
    default="deferred",
    choices=["deferred", "immediate"],
    help="garbage collection mode",
)

parser.add_argument(
    "-o",
    "--offsetTime",
    dest="offset_time",
    type=int,
    default=0,
    help="offset from UTC",
)

parser.add_argument(
    "-p",
    "--port",
    type=int,
    default=31800,
    help="listening port",
)

parser.add_argument(
    "-P",
    "--precision",
    type=int,
    default=7,
    help="display precision",
)

parser.add_argument(
    "-q",
    "--quiet",
    action="store_true",
    default=False,
    help="quiet mode",
)

parser.add_argument(
    "-s",
    "--threads",
    type=int,
    default=0,
    help="number of threads or processes available for parallel processing",
)

parser.add_argument(
    "-t",
    "--timerPeriod",
    dest="timer_period",
    type=int,
    default=0,
    help="timer period in milliseconds",
)

parser.add_argument(
    "--timeout",
    type=int,
    default=0,
    help="timeout in seconds for client queries",
)

parser.add_argument(
    "-w",
    "--memoryLimit",
    dest="memory_limit",
    type=int,
    default=0,
    help="memory limit in MB",
)


def krun(args):
    if args.config:
        profile_util.config(args.config)
    elif args.profile:
        profile_util.start(args.profile)


def main():
    args = parser.parse_args()
    krun(args)
