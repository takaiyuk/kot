"""
# https://qiita.com/nabehide/items/754eb7b7e9fff9a1047d 

serverless-chromiumのダウンロード
```
$ mkdir -p drivers/
$ curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
$ unzip headless-chromium.zip -d drivers/
$ rm headless-chromium.zip
```

chromedriverのダウンロード
```
$ curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
$ unzip chromedriver.zip -d drivers/
$ rm chromedriver.zip
```
"""

import subprocess


amazonlinux_drivers_prefix = "drivers/amazonlinux"


def python_run(cmd):
    subprocess.call(cmd.split(" "))


def load_serverless_chronium():
    cmd = f"mkdir -p ./{amazonlinux_drivers_prefix}/"
    python_run(cmd)
    cmd = f"wget -P ./{amazonlinux_drivers_prefix}/ https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip"
    python_run(cmd)
    cmd = f"unzip ./{amazonlinux_drivers_prefix}/stable-headless-chromium-amazonlinux-2017-03.zip -d ./{amazonlinux_drivers_prefix}/"
    python_run(cmd)
    cmd = f"rm ./{amazonlinux_drivers_prefix}/stable-headless-chromium-amazonlinux-2017-03.zip"
    python_run(cmd)


def load_chromedriver_linux():
    cmd = f"wget -P ./{amazonlinux_drivers_prefix}/ https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip"
    python_run(cmd)
    cmd = f"unzip ./{amazonlinux_drivers_prefix}/chromedriver_linux64.zip -d ./{amazonlinux_drivers_prefix}/"
    python_run(cmd)
    cmd = f"rm ./{amazonlinux_drivers_prefix}/chromedriver_linux64.zip"
    python_run(cmd)


if __name__ == "__main__":
    load_serverless_chronium()
    load_chromedriver_linux()
