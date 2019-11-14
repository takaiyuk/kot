"""
wget -P ./chromedriver/ https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_{os}64.zip
cd chromedriver
unzip chromedriver_{os}64.zip
rm chromedriver_{os}64.zip
cd ..
"""

import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--os", help="your os (default is mac).",
                    type=str, choices=["mac", "linux"], default="mac")
args = parser.parse_args()

url = f"https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_{args.os}64.zip"
drivers_prefix = "drivers"

command = f"mkdir {drivers_prefix}".split(" ")
subprocess.call(command)
command = f"wget -P ./{drivers_prefix}/ {url}".split(" ")
subprocess.call(command)
command = f"unzip ./{drivers_prefix}/chromedriver_{args.os}64.zip -d ./{drivers_prefix}/".split(
    " "
)
subprocess.call(command)
command = f"rm ./{drivers_prefix}/chromedriver_{args.os}64.zip".split(" ")
subprocess.call(command)
