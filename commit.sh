#!/bin/bash

# Define variables passed in from the pipeline call in GitHub Actions
AZ_USERNAME=$AZ_USERNAME
AZ_PAT=$AZ_PAT
AZ_ORG=$AZ_ORG
AZ_USERNAME=$AZ_USERNAME

AZ_URL="catherinevee/code/_git/code"
AZ_EMAIL="catherine.vee@outlook.com"

# Fully remove the .git directory
rm -rf code/.git

# Fetch the changes from Azure DevOps repo
git fetch --unshallow

# Pull changes from Azure DevOps repo
git pull https://$AZ_USERNAME:$AZ_PAT@dev.azure.com/$AZ_URL

# Set Git Global settings
git config --global user.email $AZ_EMAIL
git config --global user.name $AZ_USERNAME

# Add all changes into stage, commit, and push to Azure DevOps
git add .
git commit -m "Sync from GitHub to Azure DevOps"
git push --force https://$AZ_USERNAME:$AZ_PAT@dev.azure.com/$AZ_URL