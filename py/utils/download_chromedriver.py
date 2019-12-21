import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "--os",
    help="your os (default is mac).",
    type=str,
    choices=["mac", "linux"],
    default="mac",
)
args = parser.parse_args()

# https://chromedriver.chromium.org/downloads
url = f"https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_{args.os}64.zip"
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
