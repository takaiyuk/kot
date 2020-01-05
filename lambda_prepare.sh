#!/bin/sh

function mkdirs() {
    mkdir -p drivers/
    mkdir -p drivers/amazonlinux
}

function load_serverless_chronium() {
    FILE="drivers/amazonlinux/headless-chromium"

    if [ ! -e $FILE ];then
        curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
        unzip headless-chromium.zip -d drivers/amazonlinux/
        rm headless-chromium.zip
    fi
}

function load_chromedriver_linux() {
    FILE="drivers/amazonlinux/chromedriver"

    if [ ! -e $FILE ];then
        curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
        unzip chromedriver.zip -d drivers/amazonlinux/
        rm chromedriver.zip
    fi
}

function copy_files() {
    rsync -ar ./* ./deploy_package --exclude 'deploy_package' --exclude 'drivers/chromedriver' --exclude 'Dockerfile'
}

mkdirs
load_serverless_chronium
load_chromedriver_linux
copy_files
