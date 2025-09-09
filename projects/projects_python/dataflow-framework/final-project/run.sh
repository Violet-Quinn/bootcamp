#!/bin/bash
# This script simplifies common project commands for building, running,
# packaging, and cleaning your Level 8 -> Final file processor project.
# Usage:
# ./run.sh build-docker       # Build Docker image for containerized deployment
# ./run.sh run                # Run in watch mode: monitors folder continuously
# ./run.sh run-single file    # Run single file processing mode and exit
# ./run.sh build-package      # Build Python package (wheel/sdist) using uv
# ./run.sh clean              # Remove build artifacts and Python caches
set -e  # Exit immediately if a command exits with a non-zero status
COMMAND=$1  # First argument: command name
ARG=$2      # Second argument: optional command argument

function build_docker() {
    echo "Building Docker image..."
    docker build -t dataflow-framework:latest .
    echo "Docker image built successfully."
}

function run_watch() {
    echo "Starting application in watch mode (folder monitoring)..."
    python3 main.py --watch
}

function run_single() {
    if [ -z "$ARG" ]; then
        echo "Error: Please provide an input file for single file mode."
        exit 1
    fi
    echo "Processing single input file: $ARG"
    python3 main.py --input "$ARG"
}

function build_package() {
    echo "Building Python package using uv..."
    uv build
    echo "Package built successfully in dist/"
}

function clean_project() {
    echo "Cleaning project build artifacts and caches..."
    rm -rf dist/ build/ *.egg-info __pycache__ .pytest_cache
    echo "Clean complete."
}

# Main driver
case "$COMMAND" in
    build-docker)
        build_docker
        ;;
    run)
        run_watch
        ;;
    run-single)
        run_single
        ;;
    build-package)
        build_package
        ;;
    clean)
        clean_project
        ;;
    *)
        echo "Usage: $0 {build-docker|run|run-single|build-package|clean}"
        exit 1
        ;;
esac
