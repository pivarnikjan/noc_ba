#!/bin/bash

#set -ex

# Author: Jan Pivarnik <jp002f@intl.att.com>
# v1.0                  Init script
# v1.1                  Adding SSH key option when cloning repository
# v1.2                  Fixed wrong closing
# v1.3                  Added temporary directory for cloning rep into existing one
# v1.4                  Added option to build and run container
# v1.5                  Added validation for checking if container is running
# v2.0                  Extracted variable strings for speciffic projects into header file
# v2.1                  Fixed exit status of script, now in case of failure returns 1
# v2.2                  Fixed checking exit code of cleaning container
# v2.3                  Added option for additional prebuild commands
# v2.4                  Proxy http address is now dynamically generated
# v2.5                  Fixed success status if starting container has failed - added function check_running_container, copying oracle_client is no longer support by deploy.sh
# v2.6                  Fixed timing for sleep
# v2.7                  Added checking exit code of running app inside container
# v2.8                  Fixed wrong position of testing running web app
# v2.9                  Added support for more verbose prebuild commands
# v2.10                 Added option for more complex docker start command
# v2.11                 Fixed checking of exit status on docker run command
# v2.12   09/05/2017    Added timestamp, if someone want to use complex prebuild commands, explicit string is required
# v2.13   09/26/2017    Added option for unittests, added test option in documentation

MY_DIR="$(dirname "$0")"
source "$MY_DIR/header.sh"

PATH_TO_SSH="/jenkins_home/id_rsa"

function check_exit_status() {
    if [ $? -ne 0 ]; then
        echo $(fc -ln -1)
        exit 1
    fi
}

function check_running_container() {
    local container_id=$(docker ps -a | grep ${CONTAINER_NAME}:${CONTAINER_TAG} | awk '/Exited/ || /Restarting/ || /Dead/ || /Created/' | awk '{print $1}')
    if [ "$container_id" != "" ]; then
        echo "Check your running script - container was not able to start"
        exit 1
    fi
}

function build_container() {
    local proxy='one.proxy.att.com'
    local ip=$(nslookup ${proxy} | tail -2 | head -1 | awk '{print $2}')
    local addr="http://${ip}:8888"
    
    if [ "$ADDITIONAL_PREBUILD_COMMANDS" == "prebuild_commands" ]; then
        prebuild_commands
    fi
    check_exit_status

    echo "Building container ${CONTAINER_NAME}:${CONTAINER_TAG}"
    docker build -t ${CONTAINER_NAME}:${CONTAINER_TAG} --build-arg http_proxy=${addr} --build-arg https_proxy=${addr} --build-arg ftp_proxy=${addr}  .
    check_exit_status 
}

function run_container() {
    local output=$(docker ps -a | grep ${CONTAINER_NAME} | awk '{print $1}')
    
    if [ "$output" != "" ]; then
        echo "Container ${CONTAINER_NAME} is running "
        clean_container
    else
        echo "Container ${CONTAINER_NAME} is not running "
    fi

    echo "Starting container ${CONTAINER_NAME} (version: ${CONTAINER_TAG})"
    if [ "$ADDITIONAL_DOCKER_RUN_PARAMS" == "complex_start" ]; then
        echo "Running container ${CONTAINER_NAME} with complex starting parameters"
        complex_start
        check_exit_status
    else
        docker run -d --name ${CONTAINER_NAME} ${ADDITIONAL_DOCKER_RUN_PARAMS} ${CONTAINER_NAME}:${CONTAINER_TAG}
        check_exit_status
    fi

    sleep 2
    check_running_container
    ${TEST_APP_EXIT_CODE}
}

function clean_install_app() {
    echo "Cleaning everything inside directory"
    rm -rf *
    echo "Adding your SSH key (location: ${PATH_TO_SSH}) and cloning repository ${REPOSITORY_URL}"
    ssh-agent bash -c "ssh-add ${PATH_TO_SSH}; git clone ${REPOSITORY_URL} ${CONTAINER_NAME}"
    check_exit_status
}

function update_app() {
    echo "Pulling latest changes from repository ${REPOSITORY_URL}"
    ssh-agent bash -c "ssh-add ${PATH_TO_SSH}; git pull"
    check_exit_status
}

function clean_container() {
    echo "Stoping and removing container ${CONTAINER_NAME}"
    docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}
}

function test_container() {
    if [ -z "$TEST_CMD" ]; then
        echo "No tests are set for execution.";
        return 0
    fi

    echo "Testing image ${CONTAINER_NAME}:${CONTAINER_TAG}"
    docker run --rm ${CONTAINER_NAME}:${CONTAINER_TAG} ${TEST_CMD}

    if [ $? == 0 ]; then
        echo "Tests passed."
    else
        echo "Tests failed."
        exit 1
    fi
}

function provision_server () {
  build_container
  echo "---"
  test_container
  echo "---"
  run_container
  echo "---"
}

function help_menu () {
    cat << EOF
    Usage: ${0} (-b | -r | -i | -u | -a | -c)

    OPTIONS:
        -h|--help       Show this message
        -b|--build      Build container 
        -r|--run        Run container
        -i|--install	Clone repository
        -u|--update     Pull latest version
        -a|--all        Provision everything
        -c|--clean      Clean container
        -t|--test       Run test suite

    ENVIRONMENT VARIABLES:
       CONTAINER_NAME   Name of container we would like to build and run with
                        Defaulting to ${CONTAINER_NAME}

       CONTAINER_TAG    Tag for container we would like to build and run with
                        Defaulting to ${CONTAINER_TAG}

       REPOSITORY_URL   Repository URL
                        Defaulting to ${REPOSITORY_URL}

    EXAMPLES:
        Build container:
            $ ${0} -b
        Run container:
            $ ${0} -r
        Clone repository:
            $ ${0} -i
        Pull latest changes:
            $ ${0} -u
        Configure everything together:
            $ ${0} -a
        Remove container:
            $ ${0} -c
        Run unittests:
            $ ${0} -t

EOF
}

case "${1}" in
  -b|--build)
  build_container
  ;;
  -r|--run)
  run_container
  ;;
  -i|--install)
  clean_install_app
  ;;
  -u|--update)
  update_app
  ;;
  -a|--all)
  provision_server
  ;;
  -c|--clean)
  clean_container
  ;;
  -t|--test)
  test_container
  ;;
  -h|--help)
  help_menu
  ;;
  *)
  echo "${1} is not a valid flag, try running: ${0} --help"
  ;;
esac
