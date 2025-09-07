#!/usr/bin/env bash


# Functions
function help() {
  echo "Usage: ./run.sh [command]"
  echo "Commands:"
  echo "  install       Install Python dependencies"
  echo "  build-docker  Build Docker image named dataflow-pipeline"
  echo "  run           Run the project locally with folder monitor and dashboard"
  echo "  clean         Remove Python .pyc files and __pycache__ folders"
  echo "  help          Show this help message"
}

function install() {
  echo "Installing Python dependencies..."
  pip install -r requirements.txt
}

function build_docker() {
  echo "Building Docker image..."
  docker build -t dataflow-pipeline .
}

function run_project() {
  echo "Starting folder monitor with observability dashboard..."
  python3 main.py --watch-dir watch_dir --trace
}

function clean() {
  echo "Cleaning up __pycache__ and .pyc files..."
  find . -type f -name "*.pyc" -delete
  find . -type d -name "__pycache__" -exec rm -rf {} +
}

# Main
if [ $# -eq 0 ]; then
  help
  exit 1
fi

case "$1" in
  install)
    install
    ;;
  build-docker)
    build_docker
    ;;
  run)
    run_project
    ;;
  clean)
    clean
    ;;
  help|*)
    help
    ;;
esac
