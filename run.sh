#!/bin/bash

# Prompt the user to input a number
read -p "Please select what you want to run:
1. Run the frontend locally
2. Association Matrix Generator
3. Confusion Matrix Generator
4. Rules-based Hazard Identification

Enter the corresponding number: " number

# Execute different commands based on the input
case $number in
    1)
        # Command for number 1
        echo "Running the frontend locally..."
        cd "$(dirname "$0")/frontend"
        source .venv/bin/activate
        streamlit run app.py
        ;;
    2)
        # Command for number 2
        echo "Generating Association Matrix..."
        cd "$(dirname "$0")/tools"
        source .venv/bin/activate
        cd AssociationMatrix
        bash run_assocMat.sh
        ;;
    3)
        # Command for number 3
        echo "Generating Confusion Matrix..."
        cd "$(dirname "$0")/tools"
        source .venv/bin/activate
        cd ConfusionMatrix
        bash run_confMat.sh
        ;;
    4)
        # Command for number 4
        echo "Running Rules-based Hazard Identification..."
        cd "$(dirname "$0")/tools"
        source .venv/bin/activate
        cd RulesBased
        python3 rules_based.py
        ;;
    *)
        # Default case when the input is not recognized
        echo "Invalid input"
        ;;
esac