import boto3
import pandas as pd
from datetime import datetime, timedelta

def generate_team_cost_report(team_name, days_back=30):
    """Generate a cost report focused on actionable insights for a specific team"""

    ce_client = boto3.client('ce')

    # Get the date range for analysis
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    # Fetch cost data broken down by service
    team_costs = ce_client.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='DAILY',
        Metrics=['BlendedCost'],
        Filter={
            'Tags': {
                'Key': 'team',
                'Values': [team_name]
            }
        },
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    # Process the data into actionable insights
    insights = analyze_cost_patterns(team_costs, team_name)

    return insights

def analyze_cost_patterns(cost_data, team_name):
    """Convert raw cost data into actionable insights"""

    total_cost = 0
    service_breakdown = {}
    daily_costs = []

    # Process each day's costs
    for result in cost_data['ResultsByTime']:
        day_total = 0
        date = result['TimePeriod']['Start']

        for group in result['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['BlendedCost']['Amount'])

            total_cost += cost
            day_total += cost
            service_breakdown[service] = service_breakdown.get(service, 0) + cost

        daily_costs.append({'date': date, 'cost': day_total})

    # Generate insights that teams can act on
    insights = {
        'team_name': team_name,
        'period_days': len(daily_costs),
        'total_cost': total_cost,
        'average_daily_cost': total_cost / len(daily_costs) if daily_costs else 0,
        'top_cost_drivers': get_top_cost_drivers(service_breakdown),
        'optimization_opportunities': identify_optimization_opportunities(service_breakdown),
        'cost_trend': calculate_cost_trend(daily_costs)
    }

    return insights

def print_team_cost_summary(insights):
    """Print a human-readable summary of cost insights"""

    print(f"\n💰 COST SUMMARY: {insights['team_name'].upper()} TEAM")
    print("=" * 50)
    print(f"Total Cost (last {insights['period_days']} days): ${insights['total_cost']:.2f}")
    print(f"Average Daily Cost: ${insights['average_daily_cost']:.2f}")

    print(f"\n🔍 TOP COST DRIVERS:")
    for service, cost in insights['top_cost_drivers'][:3]:
        percentage = (cost / insights['total_cost']) * 100
        print(f"   • {service}: ${cost:.2f} ({percentage:.1f}%)")

    if insights['optimization_opportunities']:
        print(f"\n💡 OPTIMIZATION OPPORTUNITIES:")
        for opportunity in insights['optimization_opportunities'][:3]:
            print(f"   • {opportunity}")

    trend_emoji = "📈" if insights['cost_trend'] > 5 else "📉" if insights['cost_trend'] < -5 else "➡️"
    print(f"\n{trend_emoji} Cost Trend: {insights['cost_trend']:+.1f}% vs previous period")

insights = generate_team_cost_report('backend')
print_team_cost_summary(insights)
