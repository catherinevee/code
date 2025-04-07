# ############################################################
# Set the URL to check the latest Terraform version
# ############################################################
$latestReleaseUrl = "https://api.github.com/repos/hashicorp/terraform/releases/latest"

# ############################################################
# Define the installation directory
# ############################################################
$installDir = "C:\Terraform"

# ############################################################
# Create the installation directory if it does not exist
# ############################################################
if (-Not (Test-Path -Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir
}

# ############################################################
# Check for the latest version
# ############################################################
Write-Output "Checking for the latest Terraform version..."
$latestVersionResponse = Invoke-RestMethod -Uri $latestReleaseUrl
$latestVersion = $latestVersionResponse.tag_name.TrimStart("v")

Write-Output "Latest Terraform version is $latestVersion"

# ############################################################
# Construct the download URL for the Windows 64-bit binary
# ############################################################
$downloadUrl = "https://releases.hashicorp.com/terraform/$latestVersion/terraform_${latestVersion}_windows_amd64.zip"

# ############################################################
# Define the paths for the downloaded zip file and the executable
# ############################################################
$zipPath = "$installDir\terraform.zip"
$exePath = "$installDir\terraform.exe"

# ############################################################
# Download the latest Terraform zip file
# ############################################################
Write-Output "Downloading Terraform $latestVersion..."
$client = New-Object System.Net.WebClient
$client.DownloadFile($downloadUrl, $zipPath)

# ############################################################
# Extract the Terraform executable
# ############################################################
Write-Output "Extracting Terraform executable..."
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $installDir)

# ############################################################
# Cleanup the zip file
# ############################################################
Remove-Item -Path $zipPath

# ############################################################
# Add Terraform to the system PATH environment variable
# ############################################################
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
# Add the new path to the current PATH
$newPath = "$currentPath;$installDir"
# Set the system PATH environment variable
[System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)

# ############################################################
Write-Output "Terraform $latestVersion installation completed."
# Write-Output "You may need to restart your terminal or system for the changes to take effect."