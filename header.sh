#!/bin/bash

# set -ex

CONTAINER_NAME="demo_nightofchances"
CONTAINER_TAG="1.0"
REPOSITORY_URL="ssh://git@codecloud.web.att.com:7999/~jp002f/demo_jobfairs.git"
ADDITIONAL_DOCKER_RUN_PARAMS="complex_start"
ADDITIONAL_PREBUILD_COMMANDS="prebuild_commands"
TEST_CMD="python3 manage.py test -v 2"

APP_NAME="scrapping_api"

function complex_start(){
    local fqdn=`python -c "exec(\"import socket\\nprint(socket.getfqdn())\")"`
    echo FQDN is ${fqdn}
    echo "Running container with complex start"
    docker run -d -h ${fqdn} --name ${CONTAINER_NAME} -p 8444:8000 --dns=135.76.169.248 ${CONTAINER_NAME}:${CONTAINER_TAG}
}

function copy_conf_file(){
    echo "Replacing old configuration file"
    cp /jenkins_home/credentials/${CONTAINER_NAME}/.conf.ini .
}

function prebuild_commands(){
    install_phantomjs
    copy_conf_file
}

function install_phantomjs(){
    echo "Installing phantomjs dependencies"

    if [[ $EUID -ne 0 ]]; then
        echo "This script must be run as root" 1>&2
        exit 1
    fi

    PHANTOM_VERSION="phantomjs-2.1.1"
    ARCH=$(uname -m)

    if ! [ $ARCH = "x86_64" ]; then
        $ARCH="i686"
    fi

    PHANTOM_JS="$PHANTOM_VERSION-linux-x86_64"
    PHANTOM_JS_FILE="$PHANTOM_VERSION-linux-$ARCH"

    tar xvjf /jenkins_home/${APP_NAME}/${PHANTOM_JS_FILE}.tar.bz2 -C .
}
