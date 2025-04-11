#!/bin/bash

# Define variables passed in from the pipeline call in GitHub Actions
AZ_USERNAME=$AZ_USERNAME
AZ_PAT=$AZ_PAT
AZ_ORG=$AZ_ORG
AZ_USERNAME=$AZ_USERNAME

AZ_URL="catherinevee/code/_git/code"

# Fully remove the .git directory
rm -rf code/.git

# Fetch the changes from Azure DevOps to ensure we have latest
git fetch --unshallow

# Pull changes from Azure DevOps if its exiting branch and have commits on it
git pull https://catherinevee:$AZ_PAT@dev.azure.com/$AZ_URL

# Set Git user identity
git config --global user.email "catherine.vee@outlook.com"
git config --global user.name $AZ_USERNAME

# Add all changes into stage, commit, and push to Azure DevOps
git add .
git commit -m "Sync from GitHub to Azure DevOps"
git push --force https://catherinevee:$AZ_PAT@dev.azure.com/catherinevee/code/_git/code