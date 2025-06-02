# scripts/create_cost_alarm.py
import boto3
import argparse
import json
from datetime import datetime, timedelta

def create_deployment_cost_alarm(deployment_id, estimated_monthly_cost):
    """Create CloudWatch alarm to monitor actual vs estimated costs"""

    cloudwatch = boto3.client('cloudwatch')

    # Create alarm that triggers if actual costs exceed estimate by 25%
    threshold = estimated_monthly_cost * 1.25

    alarm_name = f"cost-overrun-{deployment_id}"

    cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='EstimatedCharges',
        Namespace='AWS/Billing',
        Period=86400,  # Daily
        Statistic='Maximum',
        Threshold=threshold,
        ActionsEnabled=True,
        AlarmActions=[
            # Replace with your SNS topic ARN
            'arn:aws:sns:us-west-2:123456789012:cost-alerts'
        ],
        AlarmDescription=f'Cost overrun alert for deployment {deployment_id}',
        Dimensions=[
            {
                'Name': 'Currency',
                'Value': 'USD'
            }
        ],
        Tags=[
            {
                'Key': 'DeploymentId',
                'Value': deployment_id
            },
            {
                'Key': 'EstimatedCost',
                'Value': str(estimated_monthly_cost)
            }
        ]
    )

    print(f"Created cost monitoring alarm: {alarm_name}")
    return alarm_name

def schedule_cost_review(deployment_id, review_date):
    """Schedule a cost review using EventBridge"""

    events = boto3.client('events')

    rule_name = f"cost-review-{deployment_id}"

    # Create EventBridge rule for the review date
    events.put_rule(
        Name=rule_name,
        ScheduleExpression=f"at({review_date}T09:00:00)",
        Description=f"Cost review for deployment {deployment_id}",
        State='ENABLED'
    )

    # Add target to trigger cost review Lambda
    events.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': '1',
                'Arn': 'arn:aws:lambda:us-west-2:123456789012:function:cost-review-handler',
                'Input': json.dumps({
                    'deployment_id': deployment_id,
                    'review_type': 'post_deployment'
                })
            }
        ]
    )

    print(f"Scheduled cost review for {review_date}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--deployment-id', required=True)
    parser.add_argument('--estimated-cost', type=float, required=True)
    args = parser.parse_args()

    create_deployment_cost_alarm(args.deployment_id, args.estimated_cost)

    # Schedule review in 7 days
    review_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    schedule_cost_review(args.deployment_id, review_date)
