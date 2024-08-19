#!/bin/bash

# Authenticate the current user
echo "Authenticating user..."
gcloud auth login

# Prompt the user for their billing account ID
read -p "Enter your billing account ID: " BILLING_ACCOUNT

# Set a variable for the project ID (it must be unique)
PROJECT_ID="hazardid-$(date +%s)"
BUCKET_NAME="hazard_definitions_bucket"

# Create a new project called HazardID
echo "Creating project: $PROJECT_ID"
gcloud projects create $PROJECT_ID --name="HazardID"

# Set the newly created project as the current project
echo "Setting project $PROJECT_ID as current project"
gcloud config set project $PROJECT_ID

# Enable billing on the project using the provided billing account ID
echo "Enabling billing for project $PROJECT_ID with billing account $BILLING_ACCOUNT..."
gcloud beta billing projects link $PROJECT_ID --billing-account=$BILLING_ACCOUNT

# Enable the Cloud Functions, Cloud Storage, and Secret Manager APIs
echo "Enabling APIs..."
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable storage-component.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Check if the APIs are enabled
echo "Checking if APIs are enabled..."
API_STATUS=$(gcloud services list --enabled --filter="NAME:cloudfunctions.googleapis.com OR NAME:storage-component.googleapis.com OR NAME:secretmanager.googleapis.com OR NAME:run.googleapis.com " --format="value(NAME)" | wc -l)

# Wait until all APIs are enabled
while [ $API_STATUS -lt 3 ]; do
    echo "Waiting for APIs to be enabled..."
    sleep 10
    API_STATUS=$(gcloud services list --enabled --filter="NAME:cloudfunctions.googleapis.com OR NAME:storage-component.googleapis.com OR NAME:secretmanager.googleapis.com" --format="value(NAME)" | wc -l)
done

echo "All APIs are enabled."

# Create a new bucket called hazard_definitions_bucket
echo "Creating bucket: $BUCKET_NAME"
gsutil mb -p $PROJECT_ID gs://$BUCKET_NAME/

# Upload a file called hazard_definitions.json to that bucket
echo "Uploading hazard_definitions.json to $BUCKET_NAME"
gsutil cp ../tools/data/hazard_definitions.json gs://$BUCKET_NAME/

# Prompt the user for the OpenAI API Key
read -sp "Enter your OpenAI API Key: " OPENAI_API_KEY
echo # Newline for better formatting

# Create a secret for the OpenAI API Key
echo "Creating secret for OpenAI API Key..."
echo -n $OPENAI_API_KEY | gcloud secrets create OPENAI_API_KEY --data-file=- --project=$PROJECT_ID

# Deploy the API
echo "Deploying API..."
gcloud functions deploy hazard-id --gen2 --region=europe-west2 --runtime=nodejs20 --entry-point=classify --trigger-http --allow-unauthenticated #--set-secrets='OPENAI_API_KEY=OPENAI_API_KEY:latest'
FUNCTION_URL=$(gcloud functions describe hazard-id --region=europe-west2 --format="value(url)")

# Create or overwrite the .env file with the new API URLs
cat > .env << EOF
USERNAMES="hamish,demo"
PASSWORD="hazard"
API_URL_ML="${FUNCTION_URL}/classify/startGPTClassification"
API_URL_RB="${FUNCTION_URL}/classify/startClassification"
API_URL_REFINE="${FUNCTION_URL}/classify/refineClassification"
API_URL_CONFUSION="${FUNCTION_URL}/classify/getHazardsByCode"
EOF

echo ".env file created with API URLs."

# Move the .env file up a level to the frontend directory
mv .env ../frontend/.env

# Tell the user to link the secret and bucket to the Cloud Run service
echo "Do the following through the Google Cloud Console:"
echo "Please link the OPENAI_API_KEY secret to the function as an environment variable."
echo "Please ensure that the cloud run agent has the necessary permissions to access the bucket."