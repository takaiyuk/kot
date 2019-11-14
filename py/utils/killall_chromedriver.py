import subprocess

command = ["killall", "chromedriver"]
ret = subprocess.call(command)
print(f"return: {ret}")
