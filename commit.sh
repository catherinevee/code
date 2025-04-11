#!/bin/bash

AZ_USERNAME = ${{secrets.AZ_USERNAME}}

# Remove Git information (for fresh git start)
rm -rf code/.git

# Fetch the changes from Azure DevOps to ensure we have latest
git fetch --unshallow

# Pull changes from Azure DevOps if its exiting branch and have commits on it
git pull "https://$AZ_USERNAME:${{secrets.AZURE_CLIENT_SECRET}}@dev.azure.com/${{secrets.AZ_ORG}}/code.git"

#git checkout -b $github_to_azure_sync

# Set Git user identity
git config --global user.email "catherine.vee@outlook.com"
git config --global user.name "${{secrets.AZ_USERNAME}}"

# Add all changes into stage, commit, and push to Azure DevOps
git add .
git commit -m "Sync from GitHub to Azure DevOps"
git push --force "https://${{secrets.AZ_USERNAME}}:${{secrets.AZURE_CLIENT_SECRET}}@dev.azure.com/${{secrets.AZ_ORG}}/code.git"
"