# Bash script to stop non-production resources during off-hours
#!/bin/bash

# Stop development environment instances at 6 PM weekdays
if [[ $(date +%u) -le 5 ]] && [[ $(date +%H) -eq 18 ]]; then
    aws ec2 stop-instances --instance-ids \
        $(aws ec2 describe-instances \
            --filters "Name=tag:Environment,Values=development" \
                     "Name=instance-state-name,Values=running" \
            --query 'Reservations[].Instances[].InstanceId' \
            --output text)
fi

# Start development environment instances at 8 AM weekdays
if [[ $(date +%u) -le 5 ]] && [[ $(date +%H) -eq 8 ]]; then
    aws ec2 start-instances --instance-ids \
        $(aws ec2 describe-instances \
            --filters "Name=tag:Environment,Values=development" \
                     "Name=instance-state-name,Values=stopped" \
            --query 'Reservations[].Instances[].InstanceId' \
            --output text)
fi
