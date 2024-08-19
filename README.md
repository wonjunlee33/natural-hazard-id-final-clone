# natural-hazard-id-final
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![Meta](https://img.shields.io/badge/Meta-%230467DF.svg?style=for-the-badge&logo=Meta&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Express.js](https://img.shields.io/badge/express.js-%23404d59.svg?style=for-the-badge&logo=express&logoColor=%2361DAFB)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)


## Introduction
HazardID aims to use the power of Large Language Models (LLMs) to guide users towards accurately classifying hazards under the [ISC-UNDRR Hazard Taxonomy Scheme](https://www.preventionweb.net/drr-glossary/hips).

Try out our tool [here](https://hazard-id.streamlit.app/). Use the following credentials to log in:
```
username: demo
password: hazard
```

To learn more about our project, please consult the project portfolio website [here](https://students.cs.ucl.ac.uk/2023/group38/).

## 1. Table of Contents
1. [Table of Contents](#1-table-of-contents)
2. [Project Motivation and Goals](#2-project-motivation-and-goals)
3. [Deployment](#3-deployment-details)
4. [Directory Structure](#4-directory-structure)
5. [Overview of Project](#5-overview-of-project)
6. [Streamlit Frontend](#6-streamlit-description-frontend)
7. [Extra](#7-extra)
8. [Team Members](#8-team-members)
9. [Credits](#9-credits)
10. [License and Legal Statement](#10-license-and-legal-statement)

## 2. Project Motivation and Goals
Many factors, such as climate change, post-pandemic complications, and civil conflicts are driving a rise in hazard events around the world - many more people are affected each year. As thus, the importance of reporting on such hazard events and classifying them properly becomes increasingly evident: the more they are accurately scrutinised, the more they can be used as aggregate data to prevent casualties or property damage. However, different organisations report and classify hazards differently, making collaboration difficult and the collection of big data next to impossible.
<br>
<br>
To mitigate this rift, a 2018 collaboration between the United Nations Disaster Risk Reduction (UNDRR) and the International Science Council sought to unionise the hazard classification process. They proposed a detailed hazard taxonomy scheme with over 300 different hazard types. Unfortunately, almost no organisations have adopted the taxonomy scheme today despite rigorous planning and efforts. This is due to its complexity: even an expert on natural hazards would find it difficult to accurately classify every event report scenario. Reading through the 100+ pages of definitions is also a chore; a faster and easier way to classify hazards is necessary for the widespread adoption of this taxonomy scheme.
<br>
<br>
This project aims to build a lightweight tool that will guide users to quickly and accurately classify a hazard event report with respect to the full ISC-UNDRR taxonomy scheme. The tool will employ the use of a Large Language Model (LLM) to scan through the text and determine possible hazards that are present according to the report. The tool will then make sure that these events actually happened by surfacing clarification questions, so that the user can confirm that the hazard actually took place. In this way, the tool guides the user towards an accurate classification of the hazards involved in any event report. The tool also aims to cut down the time required to tag an event report by up to 90%. Through streamlining a rather tedious process, the project members hope that the tool incentivises the widespread adoption of the ISC-UNDRR taxonomy scheme.

## 3. Deployment Details
### 3.1 Deploying Tool Components
The granular details for deployment have been abstracted by our shell scripts `deploy.sh` and `run.sh`. To deploy any of our individual components, do the following steps:
- Run `deploy.sh`:
  ```bash
  bash deploy.sh
  ```
This will set up all virtual environments and install all necessary requirements. It will also prompt and guide you towards deploying the API on your own Google Cloud account.
- Run `run.sh`:
  ```bash
  bash run.sh
  ```
You should now be presented with an interactive command line interface that will guide you through deploying all other components, such as a local deployment of the frontend, the AssociationMatrix Generator, the ConfusionMatrix Generator, and the command line Rules-Based tool.

### 3.2 Running System Tests
TODO

## 4. Directory Structure
Unimportant files and irrelevant config files are not portrayed in this diagram.
```text
.
├── api/
│   ├── controllers/
│   │   └── classificationController.js
│   ├── routes/
│   │   └── classificationRoutes.js
│   ├── services/
│   │   ├── classificationService.js
│   │   └── hazardDefinitionService.js
│   ├── tests/
│   │   ├── classificationController.test.js
│   │   ├── classificationService.test.js
│   │   ├── hazardDefinitionService.test.js
│   │   └── integration.test.js
│   ├── app.js
│   └── setup_api.sh
├── frontend/
│   ├── app.py
│   ├── hazard_definitions.xlsx
│   ├── requirements.txt
│   └── setup_frontend.sh
├── tools/
│   ├── AssociationMatrix/
│   │   ├── AssociatedHazardExtractor.ipynb
│   │   ├── llamaAssocGenerator.ipynb
│   │   ├── llamaCTransformerAssocGenerator.ipynb
│   │   ├── llamaCTransformerAssocGenerator.py
│   │   └── run_assocMat.sh
│   ├── ConfusionMatrix/
│   │   ├── ConfusionMatrix.py
│   │   └── run_confMat.sh
│   ├── Reliefweb/
│   │   ├── ConversionRules.txt
│   │   ├── DataPicker.py
│   │   └── ReliefwebScraper.py
│   ├── RulesBased/
│   │   └── rules_based.py
│   ├── test_python/
│   │   └── test_RulesBased.py
│   ├── tests/
│   │   ├── run_coverage.py
│   │   └── run_test.sh
│   ├── data/
│   │   ├── ConvertXLSXToJSON.py
│   │   ├── confusion_matrix.xlsx
│   │   ├── eventReport.txt
│   │   ├── hazard_definitions.json
│   │   ├── hazard_definitions.xlsx
│   │   ├── heatmap.png
│   │   ├── scores.xlsx
│   │   └── synonym_extractor.py
│   ├── requirements.txt
│   └── setup_tools.sh
├── README.md
├── deploy.sh
└── run.sh
```
For details on every file and their functions, please consult the project portfolio website.

## 5. Overview of Project
![architecture drawio](https://github.com/SysEng-Group-38/natural-hazard-id-final/assets/67159793/9b4996f1-ef05-478b-bc4f-b0741e23d18c)

When the user inputs a hazard report into the website (front-end), the website forwards the report to the `startClassification` endpoint of the tool API. The next action in the program flow differs slightly depending on whether the machine learning or rules-based model is selected. <br>

If the machine learning model is selected, the tool API sends the report and hazard definitions to the OpenAI ChatGPT 3.5 Turbo to be processed. When ChatGPT finishes processing, it returns a JSON list of matching hazard ID’s back to the tool API. <br>

Conversely, if the rules-based model is selected, the API does not send the report to OpenAI. Instead, the `natural` framework for JavaScript is used to match keywords within the report. A list of matching hazard ID’s is then generated. <br>

The tool API then matches the hazard ID’s to its appropriate clarification questions as per the hazard definitions database (currently, an Excel spreadsheet), and acquires the necessary clarification questions. It then sends the matched hazard ID’s and questions back to the website, where it is surfaced back to the user. <br>

When the user submits the answers to the clarification questions, the website sends the results to `refineClassification`, another tool API endpoint. `refineClassification` then checks for any upstream hazards through the AssociationMatrix database. If any exist, it checks the Hazard Definition Database and returns a new JSON of matching upstream ID’s and clarification questions. This continues until there are no more upstream hazards remaining. <br>

Finally, `refineClassification` correlates the final list of identified hazards with the ConfusionMatrix database, and acquires a list of commonly confused hazards for each identified hazard (if any). These are then returned back to the website to be surfaced to the user. <br>

## 6. Streamlit Description (FrontEnd)

This Streamlit web application leverages Natural Language Processing (NLP) and Machine Learning (ML) models to classify natural hazards from textual reports. It offers a comprehensive interface for users to interact with different classification models, answer model-generated questions to refine hazard identification, and export the classification results.

### 6.1 Features

- **User Authentication:** Secure login interface for user authentication, ensuring that only authorized users can access the application.
- **Model Selection:** Users can choose between a rules-based model and a machine learning model for hazard classification, providing flexibility in approach.
- **Report Submission:** Users can submit reports for classification in three ways: typing directly into the app, uploading a text file, or using a pre-loaded default report.
- **Interactive Question-Answering:** The app generates questions based on the report content. Users can respond using text inputs or toggles to refine hazard classification.
- **Hazard Information:** Users can access definitions and detailed information about each hazard, including commonly associated and confused hazards.
- **Hazard Ranking and Export:** The application allows for the ranking of identified hazards by occurrence. Users can export the classification results and hazard rankings as JSON files.
- **Versatile Report Processing:** Users have the option to reprocess the report with the alternative classification model or restart the process with a new report.

### 6.2 Application Workflow

1. **Login (`login()`):** Authenticate using the login page.
2. **Model Selection (`classification_type()`):** Choose the classification model (rules-based or ML model).
3. **Report Submission (`user_report`):** Enter or upload the report for classification.
4. **Interactive Question-Answering (`question()`, `display_question()`, `process_answers()`):** Respond to questions generated from the report to refine hazard identification.
5. **Refinement and Additional Questions (`refined_question()`):** Answer a second set of questions for further classification refinement.
6. **Hazard Information and Ranking (`display_confirmed_hazards()`, `rank_hazards()`):** View classified hazards, access their definitions, and rank them by occurrence.
7. **Export and Restart Options (`export_hazard_data()`, `restart()`, `switch_model()`):** Export classification results and hazard rankings, reprocess the report with another model, or start with a new report.

### 6.3 Disclaimer

This application is designed for demonstration and educational purposes. It showcases the potential of integrating NLP and ML models in the classification of natural hazards from textual data.

## 7. Extra
### OpenAPI Specification
```yaml
openapi: 3.0.0
info:
  title: HazardID Classification API
  description: API for classifying reports based on hazard definitions and refining those classifications. Also provides hazard information based on UNDRR-ISC hazard codes.
  version: "1.0.0"
paths:
  /classify/startClassification:
    post:
      summary: Initiate report classification
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                report:
                  type: string
                  description: Report text to be classified.
              required:
                - report
      responses:
        '200':
          description: Classification questions based on report
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    question:
                      type: string
                    hazardCode:
                      type: string
        '400':
          description: Bad request if report is missing
  /classify/startGPTClassification:
    post:
      summary: Start classification using GPT for hazard identification
      requestBody:
        description: Same as /startClassification
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ClassificationRequest'
      responses:
        '200':
          description: GPT-identified hazards and questions based on report
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/QuestionsResponse'
  /classify/startCombinedClassification:
    post:
      summary: Combine standard and GPT classification methods
      requestBody:
        description: Initiate repor classification using GPT and rules based methods
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ClassificationRequest'
      responses:
        '200':
          description: Combined set of questions from both methods
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/QuestionsResponse'
  /classify/refineClassification:
    post:
      summary: Refine classification with confirmed and rejected hazards
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                confirmed:
                  type: array
                  items:
                    type: string
                rejected:
                  type: array
                  items:
                    type: string
              required:
                - confirmed
                - rejected
      responses:
        '200':
          description: Further refined questions
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    question:
                      type: string
                    hazardCode:
                      type: string
        '400':
          description: Bad request if confirmed or rejected hazards are missing
  /classify/getHazardsByCode:
    post:
      summary: Get hazard definitions by codes
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                hazardCodes:
                  type: array
                  items:
                    type: string
              required:
                - hazardCodes
      responses:
        '200':
          description: Hazard definitions for the provided codes
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    Hazard_Code:
                      type: string
                    Description:
                      type: string
components:
  schemas:
    ClassificationRequest:
      type: object
      properties:
        report:
          type: string
          description: Report text to be classified.
      required:
        - report
    QuestionsResponse:
      type: array
      items:
        type: object
        properties:
          question:
            type: string
          hazardCode:
            type: string
```

## 8. Team Members
2023/24 COMP0016 Systems Engineering Group 38 had the following group members:
- [Wonjun Lee](https://www.linkedin.com/in/wonjun-lee-55802b252/) (wonjun.lee.22@ucl.ac.uk)
- [Jasper Koenig](https://www.linkedin.com/in/jasper-koenig-42b027211/) (jasper.koenig.22@ucl.ac.uk)
- [Aryan Jain](https://www.linkedin.com/in/aryan--jain/) (aryan.jain.22@ucl.ac.uk)

## 9. Credits
All rights for frameworks and 3rd party tools used in this project go to their respective owners.

## 10. License and Legal Statement
COMP0016 Systems Engineering Team 38 agrees to adhere to any license that the IFRC set out, and agree to handover all rights
of the tool and any of its components to the IFRC as laid out by the COMP0016 Systems Engineering Contract.
