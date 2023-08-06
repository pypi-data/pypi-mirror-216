"""This is the cli of pyipify"""
import argparse
import asyncio
from .synchronous import find_ipv4 as sync_find_ipv4
from .synchronous import find_ipv6 as sync_find_ipv6
from .asynchronous import find_ipv4 as async_find_ipv4
from .asynchronous import find_ipv6 as async_find_ipv6

parser = argparse.ArgumentParser(description="The program to find the ipv4 "
                                             "and ipv6 address of the system.")

parser.add_argument("-v", "--version", choices=["ipv4", "ipv6"],
                    help="The version of the ip address to be found. "
                         "Default is ipv4 use ipv4 for ipv4 address and "
                         "ipv6 for ipv6 addresses",
                    default="ipv4")
parser.add_argument("-a", "--asynchronous", help="Use this flag to run the program asynchronously",
                    action="store_true",
                    default=False)
parser.add_argument("-s", "--synchronous", help="Use this flag to run the program synchronously",
                    action="store_true",
                    default=True)
parser.add_argument("-o", "--output", help="Use this flag to output the ip address to a file")
args = parser.parse_args()
if args.asynchronous:
    if args.version == "ipv4":
        ip = asyncio.run(async_find_ipv4())
    else:
        ip = asyncio.run(async_find_ipv6())
else:
    if args.version == "ipv4":
        ip = sync_find_ipv4()
    else:
        ip = sync_find_ipv6()
if args.output:
    with open(args.output, "w", encoding='utf-8') as file:
        file.write(ip)
print(ip)
