#!/bin/bash

# set -ex

# Author: Jan Pivarnik <jp002f@intl.att.com>


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
    if [ "$ADDITIONAL_PREBUILD_COMMANDS" == "prebuild_commands" ]; then
        prebuild_commands
    fi
    check_exit_status

    echo "Building container ${CONTAINER_NAME}:${CONTAINER_TAG}"
    docker build -t ${CONTAINER_NAME}:${CONTAINER_TAG} .
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
        -a|--all        Provision everything
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
        Configure everything together:
            $ ${0} -a
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
