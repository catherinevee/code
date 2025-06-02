# scripts/engineering_cost_dashboard.py
import boto3
import json
from datetime import datetime, timedelta
import pandas as pd

class EngineeringCostDashboard:
    def __init__(self):
        self.ce_client = boto3.client('ce')
        self.cloudwatch = boto3.client('cloudwatch')

    def get_feature_cost_analysis(self, feature_name, days_back=30):
        """Analyze costs for a specific feature or service"""

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        # Get costs by feature tag
        feature_costs = self.ce_client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            Filter={
                'Tags': {
                    'Key': 'feature',
                    'Values': [feature_name]
                }
            },
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )

        # Convert to engineering-friendly metrics
        metrics = self.calculate_engineering_metrics(feature_costs, feature_name)

        return metrics

    def calculate_engineering_metrics(self, cost_data, feature_name):
        """Convert cost data to metrics engineers care about"""

        total_cost = 0
        service_breakdown = {}

        for result in cost_data['ResultsByTime']:
            for group in result['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                total_cost += cost
                service_breakdown[service] = service_breakdown.get(service, 0) + cost

        # Calculate cost per user metrics (this would need user analytics integration)
        # For demo purposes, using placeholder data
        estimated_daily_users = 1000  # From analytics
        cost_per_user_per_day = total_cost / (estimated_daily_users * 30)

        # Calculate cost efficiency metrics
        metrics = {
            'feature_name': feature_name,
            'total_monthly_cost': total_cost,
            'cost_per_user_per_day': cost_per_user_per_day,
            'cost_per_user_per_month': cost_per_user_per_day * 30,
            'largest_cost_driver': max(service_breakdown, key=service_breakdown.get),
            'service_breakdown': service_breakdown,
            'efficiency_score': self.calculate_efficiency_score(total_cost, estimated_daily_users)
        }

        return metrics

    def calculate_efficiency_score(self, total_cost, daily_users):
        """Calculate an efficiency score that engineers can optimize"""

        # Simple efficiency calculation - lower cost per user = higher score
        cost_per_user = total_cost / (daily_users * 30) if daily_users > 0 else float('inf')

        if cost_per_user < 0.01:
            return 'A'
        elif cost_per_user < 0.05:
            return 'B'
        elif cost_per_user < 0.10:
            return 'C'
        else:
            return 'D'

    def generate_team_cost_summary(self, team_name):
        """Generate cost summary that relates to team's work"""

        print(f"\n🏗️  {team_name.upper()} TEAM COST SUMMARY")
        print("=" * 50)

        # Get team's total costs
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        team_costs = self.ce_client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            Filter={
                'Tags': {
                    'Key': 'team',
                    'Values': [team_name]
                }
            }
        )

        if team_costs['ResultsByTime']:
            monthly_cost = float(team_costs['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])

            # Convert to relatable metrics
            print(f"💰 Monthly Cost: ${monthly_cost:.2f}")
            print(f"☕ Coffee Equivalent: {monthly_cost / 4:.0f} cups/day")
            print(f"👨‍💻 Engineer Salary Equivalent: {monthly_cost / 8000:.1f}% of one engineer")
            print(f"🚀 Daily Deployment Budget: ${monthly_cost / 30:.2f}")

            # Get cost trend
            prev_start = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
            prev_end = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

            prev_costs = self.ce_client.get_cost_and_usage(
                TimePeriod={'Start': prev_start, 'End': prev_end},
                Granularity='MONTHLY',
                Metrics=['BlendedCost'],
                Filter={
                    'Tags': {
                        'Key': 'team',
                        'Values': [team_name]
                    }
                }
            )

            if prev_costs['ResultsByTime']:
                prev_monthly_cost = float(prev_costs['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
                trend = ((monthly_cost - prev_monthly_cost) / prev_monthly_cost) * 100

                trend_emoji = "📈" if trend > 5 else "📉" if trend < -5 else "➡️"
                print(f"{trend_emoji} Month-over-month: {trend:+.1f}%")

        print()

# Example dashboard usage
dashboard = EngineeringCostDashboard()

# Generate team summaries
teams = ['frontend', 'backend', 'data']
for team in teams:
    dashboard.generate_team_cost_summary(team)

# Analyze specific features
features = ['user-authentication', 'payment-processing', 'search-service']
for feature in features:
    metrics = dashboard.get_feature_cost_analysis(feature)
    print(f"🎯 {feature.upper()}")
    print(f"   Monthly Cost: ${metrics['total_monthly_cost']:.2f}")
    print(f"   Cost per User: ${metrics['cost_per_user_per_month']:.4f}/month")
    print(f"   Efficiency Score: {metrics['efficiency_score']}")
    print()
