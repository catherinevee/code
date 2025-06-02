# scripts/cost_feedback_analyzer.py
import boto3
import json
from datetime import datetime, timedelta
from collections import defaultdict

class CostFeedbackAnalyzer:
    def __init__(self):
        self.ce_client = boto3.client('ce')

    def analyze_team_cost_trends(self, team_name, days_back=30):
        """Analyze cost trends and provide feedback"""

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        # Get daily costs for the team
        team_costs = self.ce_client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            Filter={
                'Tags': {
                    'Key': 'team',
                    'Values': [team_name]
                }
            },
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ]
        )

        # Analyze patterns
        service_trends = defaultdict(list)

        for result in team_costs['ResultsByTime']:
            date = result['TimePeriod']['Start']
            for group in result['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                service_trends[service].append({
                    'date': date,
                    'cost': cost
                })

        # Generate insights
        insights = self.generate_cost_insights(service_trends)

        # Create feedback report
        report = {
            'team': team_name,
            'analysis_period': f"{start_date} to {end_date}",
            'insights': insights,
            'recommendations': self.generate_recommendations(insights),
            'generated_at': datetime.now().isoformat()
        }

        return report

    def generate_cost_insights(self, service_trends):
        """Generate insights from cost trend data"""

        insights = []

        for service, costs in service_trends.items():
            if len(costs) < 7:  # Need at least a week of data
                continue

            # Calculate trend
            recent_avg = sum(c['cost'] for c in costs[-7:]) / 7
            older_avg = sum(c['cost'] for c in costs[:7]) / 7 if len(costs) >= 14 else recent_avg

            trend_percentage = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0

            if abs(trend_percentage) > 20:  # Significant change
                insights.append({
                    'service': service,
                    'trend': 'increasing' if trend_percentage > 0 else 'decreasing',
                    'percentage_change': trend_percentage,
                    'recent_daily_average': recent_avg,
                    'significance': 'high' if abs(trend_percentage) > 50 else 'medium'
                })

        return insights

    def generate_recommendations(self, insights):
        """Generate actionable recommendations based on insights"""

        recommendations = []

        for insight in insights:
            service = insight['service']
            trend = insight['trend']
            change = insight['percentage_change']

            if trend == 'increasing' and change > 30:
                if 'EC2' in service:
                    recommendations.append({
                        'priority': 'high',
                        'service': service,
                        'action': 'Review EC2 instance utilization and consider right-sizing',
                        'potential_savings': 'Up to 30% on compute costs'
                    })
                elif 'RDS' in service:
                    recommendations.append({
                        'priority': 'medium',
                        'service': service,
                        'action': 'Analyze database performance metrics and consider Aurora Serverless',
                        'potential_savings': 'Variable based on usage patterns'
                    })
                elif 'S3' in service:
                    recommendations.append({
                        'priority': 'low',
                        'service': service,
                        'action': 'Review S3 storage classes and implement lifecycle policies',
                        'potential_savings': 'Up to 60% on storage costs'
                    })

        # Add general recommendations if no specific ones
        if not recommendations:
            recommendations.append({
                'priority': 'low',
                'service': 'general',
                'action': 'Costs appear stable. Continue monitoring and consider implementing scheduled scaling for development resources.',
                'potential_savings': '10-20% on non-production environments'
            })

        return recommendations

# Generate weekly feedback report
if __name__ == "__main__":
    analyzer = CostFeedbackAnalyzer()

    # This would typically be called for each team
    teams = ['frontend', 'backend', 'data', 'devops']

    for team in teams:
        try:
            report = analyzer.analyze_team_cost_trends(team)

            print(f"\n=== Cost Feedback Report for {team.upper()} Team ===")
            print(f"Analysis Period: {report['analysis_period']}")

            if report['insights']:
                print("\nKey Insights:")
                for insight in report['insights']:
                    print(f"  • {insight['service']}: {insight['trend']} by {insight['percentage_change']:.1f}%")

            print("\nRecommendations:")
            for rec in report['recommendations']:
                print(f"  • [{rec['priority'].upper()}] {rec['action']}")
                print(f"    Potential savings: {rec['potential_savings']}")

            # In production, you'd send this report via email or Slack

        except Exception as e:
            print(f"Error analyzing costs for team {team}: {e}")
