import boto3
from datetime import datetime, timedelta

def find_zombie_instances():
    """Find EC2 instances that might be zombies based on age and low utilization"""
    ec2 = boto3.client('ec2')
    cloudwatch = boto3.client('cloudwatch')

    # Get all running instances
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )

    zombies = []

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            launch_time = instance['LaunchTime']

            # Check if instance is older than 30 days
            days_running = (datetime.now(launch_time.tzinfo) - launch_time).days
            if days_running > 30:

                # Check average CPU over the last week
                avg_cpu = get_average_cpu_utilization(cloudwatch, instance_id)

                # Flag as potential zombie if very low CPU usage
                if avg_cpu is not None and avg_cpu < 5:
                    zombies.append({
                        'InstanceId': instance_id,
                        'DaysRunning': days_running,
                        'AvgCPU': avg_cpu
                    })

    return zombies

def get_average_cpu_utilization(cloudwatch, instance_id):
    """Get average CPU utilization for an instance over the last 7 days"""
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=datetime.now() - timedelta(days=7),
            EndTime=datetime.now(),
            Period=3600,  # 1 hour periods
            Statistics=['Average']
        )

        if response['Datapoints']:
            return sum(dp['Average'] for dp in response['Datapoints']) / len(response['Datapoints'])
        return None
    except Exception as e:
        print(f"Could not get metrics for {instance_id}: {e}")
        return None
