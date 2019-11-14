"""
wget -P ./chromedriver/ https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_mac64.zip
cd chromedriver
unzip chromedriver_mac64.zip
rm chromedriver_mac64.zip
cd ..
"""

import subprocess


url = "https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_mac64.zip"
drivers_prefix = "drivers"

command = f"mkdir {drivers_prefix}".split(" ")
subprocess.call(command)
command = f"wget -P ./{drivers_prefix}/ {url}".split(" ")
subprocess.call(command)
command = f"unzip ./{drivers_prefix}/chromedriver_mac64.zip -d ./{drivers_prefix}/".split(
    " "
)
subprocess.call(command)
command = f"rm ./{drivers_prefix}/chromedriver_mac64.zip".split(" ")
subprocess.call(command)
