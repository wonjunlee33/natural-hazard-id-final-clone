#!/bin/bash

# Prompt the user to input a number

read -p "Please select what you want to run:
1. Run API Tests
2. Run Command Line Rules-Based Tests

Enter the corresponding number: " number

# Execute different commands based on the input
case $number in
    1)
        # Command for number 1
        echo "Running API Tests..."
        cd "$(dirname "$0")/api"
        npm install
        npm run test
        ;;
    2)
        # Command for number 2
        echo "Running Command Line Rules-Based Tests..."
        cd "$(dirname "$0")/tools/tests"
        bash run_test.sh
        ;;
    *)
        # Default case when the input is not recognized
        echo "Invalid input"
        ;;
esac