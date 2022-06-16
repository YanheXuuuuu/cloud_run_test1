#!/bin/sh
# to spin up this repo as a Cloud Run service on Google Cloud
# https://cloud.google.com/sdk/gcloud/reference/run/deploy

# navigate into the app 
cd app 

# GCP project ID
PROJECTID='development-329103'

# cloud run does not allow underscores (_), so use dashes '-'
SERVICENAME='flask-restfulapi-test1'

#################################################################
# CLOUD BUILD
gcloud builds submit --tag gcr.io/$PROJECTID/$SERVICENAME


#################################################################
# CLOUD RUN
gcloud run deploy \
$SERVICENAME \
--region us-west1 \
--concurrency 10 \
--cpu 1 \
--memory 512Mi \
--min-instances 0 \
--max-instances 1 \
--port 8080 \
--timeout 20 \
--allow-unauthenticated \
--ingress all \
--image gcr.io/$PROJECTID/$SERVICENAME --platform managed
