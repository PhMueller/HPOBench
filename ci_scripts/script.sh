#!/usr/bin/env sh

if [[ "$RUN_TESTS" == "true" ]]; then
    if [[ "$USE_SINGULARITY" == "true" ]]; then
        echo "Run tests with singularity support"
        # Create the coverage report for the singularity example, since it covers more tests.
        pytest -sv --cov=hpolib tests/
        codecov
    else
        echo "Run tests without singularity support"
        pytest -sv tests/
    fi
fi

if [[ "$RUN_CODESTYLE" == "true" ]]; then
    echo "Run codestyle"
    chmod +x ci_scripts/codestyle.sh && source ./ci_scripts/codestyle.sh
fi

if [[ "$RUN_CONTAINER_EXAMPLES" == "true" ]]; then
    echo "Run containerized examples"
    chmod +x ci_scripts/container_examples.sh && source ./ci_scripts/container_examples.sh
fi

if [[ "$RUN_LOCAL_EXAMPLES" == "true" ]]; then
    echo "Run containerized examples"
    chmod +x ci_scripts/local_examples.sh && source ./ci_scripts/local_examples.sh
fi