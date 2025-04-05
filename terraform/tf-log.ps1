$env:TF_INPUT='0'
$env:TF_LOG='TRACE'
$env:TF_LOG_PATH="{1}/logs/{0}terraform.log" -f (Get-Date -Format yyyy-MM-dd-HH-mm-ss) $PSScriptRoot
$env:TF_CLI_ARGS=''
$env:TF_CLI_ARGS_plan=' -out apply.out'

terraform plan

terraform apply -auto-approve