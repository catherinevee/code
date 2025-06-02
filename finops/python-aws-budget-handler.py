# lambda/budget_alert_handler.py
import json
import boto3
import requests
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Enhanced budget alert handler with cost breakdown and recommendations"""

    # Parse SNS message
    message = json.loads(event['Records'][0]['Sns']['Message'])
    budget_name = message['BudgetName']
    threshold = message['ThresholdBreached']

    # Get detailed cost breakdown
    ce_client = boto3.client('ce')

    # Analyze recent cost trends
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    # Get service breakdown for the affected budget
    cost_by_service = ce_client.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='DAILY',
        Metrics=['BlendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}],
        Filter={
            'Tags': {
                'Key': 'team',
                'Values': [budget_name.replace('-monthly-budget', '')]
            }
        }
    )

    # Identify top cost drivers
    service_costs = {}
    for result in cost_by_service['ResultsByTime']:
        for group in result['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['BlendedCost']['Amount'])
            service_costs[service] = service_costs.get(service, 0) + cost

    # Sort by cost descending
    top_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)[:5]

    # Generate recommendations based on top services
    recommendations = generate_recommendations(top_services)

    # Create enhanced Slack alert
    slack_payload = {
        "text": f"🚨 Budget Alert: {budget_name}",
        "attachments": [
            {
                "color": "danger" if threshold > 100 else "warning",
                "fields": [
                    {
                        "title": "Threshold Breached",
                        "value": f"{threshold}%",
                        "short": True
                    },
                    {
                        "title": "Budget Period",
                        "value": "Current Month",
                        "short": True
                    },
                    {
                        "title": "Top Cost Drivers (Last 7 Days)",
                        "value": "\n".join([f"• {service}: ${cost:.2f}" for service, cost in top_services]),
                        "short": False
                    },
                    {
                        "title": "Recommendations",
                        "value": "\n".join([f"• {rec}" for rec in recommendations]),
                        "short": False
                    }
                ]
            }
        ]
    }

    # Send to Slack
    slack_webhook = os.environ['SLACK_WEBHOOK_URL']
    response = requests.post(slack_webhook, json=slack_payload)

    return {
        'statusCode': 200,
        'body': json.dumps('Alert sent successfully')
    }

def generate_recommendations(top_services):
    """Generate optimization recommendations based on service usage"""
    recommendations = []

    for service, cost in top_services:
        if 'EC2' in service and cost > 100:
            recommendations.append("Review EC2 instance utilization - consider right-sizing or scheduling")
        elif 'RDS' in service and cost > 50:
            recommendations.append("Check RDS instance utilization - consider Aurora Serverless for variable workloads")
        elif 'S3' in service and cost > 25:
            recommendations.append("Review S3 storage classes - move infrequently accessed data to IA or Glacier")
        elif 'Lambda' in service and cost > 20:
            recommendations.append("Optimize Lambda memory allocation and execution time")

    if not recommendations:
        recommendations.append("Costs appear normal - continue monitoring trends")

    return recommendations
