# NLP/LLM-Guided Natural Hazard Classification Web App

This Streamlit web application leverages Natural Language Processing (NLP) and Machine Learning (ML) models to classify natural hazards from textual reports. It offers a comprehensive interface for users to interact with different classification models, answer model-generated questions to refine hazard identification, and export the classification results.

## Features

- **User Authentication:** Secure login interface for user authentication, ensuring that only authorized users can access the application.
- **Model Selection:** Users can choose between a rules-based model and a machine learning model for hazard classification, providing flexibility in approach.
- **Report Submission:** Users can submit reports for classification in three ways: typing directly into the app, uploading a text file, or using a pre-loaded default report.
- **Interactive Question-Answering:** The app generates questions based on the report content. Users can respond using text inputs or toggles to refine hazard classification.
- **Hazard Information:** Users can access definitions and detailed information about each hazard, including commonly associated and confused hazards.
- **Hazard Ranking and Export:** The application allows for the ranking of identified hazards by occurrence. Users can export the classification results and hazard rankings as JSON files.
- **Versatile Report Processing:** Users have the option to reprocess the report with the alternative classification model or restart the process with a new report.

## Getting Started

### Access the Web App

The application is deployed online and can be accessed via [this link](https://hazard-id.streamlit.app).

### Run Locally

To run the application on your local machine, follow these steps:

1. **Clone the repository or download the source code.**

2. **Install the required dependencies:**

    ```bash
    pip install streamlit
    ```

3. **Launch the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

## Application Workflow

1. **Login (`login()`):** Authenticate using the login page.
2. **Model Selection (`classification_type()`):** Choose the classification model (rules-based or ML model).
3. **Report Submission (`user_report`):** Enter or upload the report for classification.
4. **Interactive Question-Answering (`question()`, `display_question()`, `process_answers()`):** Respond to questions generated from the report to refine hazard identification.
5. **Refinement and Additional Questions (`refined_question()`):** Answer a second set of questions for further classification refinement.
6. **Hazard Information and Ranking (`display_confirmed_hazards()`, `rank_hazards()`):** View classified hazards, access their definitions, and rank them by occurrence.
7. **Export and Restart Options (`export_hazard_data()`, `restart()`, `switch_model()`):** Export classification results and hazard rankings, reprocess the report with another model, or start with a new report.

## Note

This application is designed for demonstration and educational purposes. It showcases the potential of integrating NLP and ML models in the classification of natural hazards from textual data.
