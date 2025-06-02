# scripts/cost_anomaly_detector.py
import boto3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

class CostAnomalyDetector:
    def __init__(self):
        self.ce_client = boto3.client('ce')
        self.cloudwatch = boto3.client('cloudwatch')

    def detect_anomalies(self, days_back=30, std_threshold=2):
        """Detect cost anomalies using statistical analysis"""

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        # Get daily costs
        daily_costs = self.ce_client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='DAILY',
            Metrics=['BlendedCost']
        )

        # Convert to pandas for analysis
        costs_data = []
        for result in daily_costs['ResultsByTime']:
            date = result['TimePeriod']['Start']
            cost = float(result['Total']['BlendedCost']['Amount'])
            costs_data.append({'date': date, 'cost': cost})

        df = pd.DataFrame(costs_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        # Calculate moving statistics
        df['mean_7d'] = df['cost'].rolling(window=7).mean()
        df['std_7d'] = df['cost'].rolling(window=7).std()
        df['z_score'] = (df['cost'] - df['mean_7d']) / df['std_7d']

        # Identify anomalies
        anomalies = df[abs(df['z_score']) > std_threshold].copy()

        if not anomalies.empty:
            self.investigate_anomalies(anomalies)

        return anomalies

    def investigate_anomalies(self, anomalies):
        """Investigate root causes of cost anomalies"""

        for _, anomaly in anomalies.iterrows():
            anomaly_date = anomaly['date'].strftime('%Y-%m-%d')
            next_date = (anomaly['date'] + timedelta(days=1)).strftime('%Y-%m-%d')

            # Get service breakdown for the anomaly day
            service_costs = self.ce_client.get_cost_and_usage(
                TimePeriod={'Start': anomaly_date, 'End': next_date},
                Granularity='DAILY',
                Metrics=['BlendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
            )

            # Find services with unusual costs
            suspicious_services = []
            for result in service_costs['ResultsByTime']:
                for group in result['Groups']:
                    service = group['Keys'][0]
                    cost = float(group['Metrics']['BlendedCost']['Amount'])

                    if cost > 100:  # Arbitrary threshold for investigation
                        suspicious_services.append((service, cost))

            # Check for operational events that might explain the anomaly
            operational_context = self.get_operational_context(anomaly_date)

            # Send alert with context
            self.send_anomaly_alert(anomaly, suspicious_services, operational_context)

    def get_operational_context(self, date):
        """Get operational context that might explain cost anomalies"""
        context = []

        try:
            # Check for deployment events (this would integrate with your deployment tracking)
            # For now, we'll use CloudWatch events as a proxy
            start_time = datetime.strptime(date, '%Y-%m-%d')
            end_time = start_time + timedelta(days=1)

            # Check for Auto Scaling events
            as_client = boto3.client('autoscaling')
            activities = as_client.describe_scaling_activities(
                MaxRecords=50
            )

            for activity in activities['Activities']:
                if start_time <= activity['StartTime'].replace(tzinfo=None) <= end_time:
                    context.append(f"Auto Scaling: {activity['Description']}")

        except Exception as e:
            context.append(f"Could not retrieve operational context: {str(e)}")

        return context

    def send_anomaly_alert(self, anomaly, suspicious_services, context):
        """Send detailed anomaly alert"""

        date = anomaly['date'].strftime('%Y-%m-%d')
        cost = anomaly['cost']
        z_score = anomaly['z_score']

        subject = f"Cost Anomaly Detected: ${cost:.2f} on {date}"

        body = f"""
        Cost Anomaly Detection Report

        Date: {date}
        Cost: ${cost:.2f}
        Z-Score: {z_score:.2f}

        Top Services on Anomaly Date:
        {chr(10).join([f"  • {service}: ${cost:.2f}" for service, cost in suspicious_services])}

        Operational Context:
        {chr(10).join([f"  • {event}" for event in context]) if context else "  • No significant operational events detected"}

        Recommended Actions:
        • Review resource utilization for the date in question
        • Check for any unplanned deployments or scaling events
        • Verify if this represents a legitimate business spike
        • Consider implementing additional cost controls if this is waste
        """

        print(f"ANOMALY ALERT: {subject}")
        print(body)

        # In production, send email or Slack notification
        # self.send_email(subject, body)

# Run anomaly detection
detector = CostAnomalyDetector()
anomalies = detector.detect_anomalies()

if anomalies.empty:
    print("No cost anomalies detected in the last 30 days.")
else:
    print(f"Detected {len(anomalies)} cost anomalies:")
    for _, anomaly in anomalies.iterrows():
        print(f"  {anomaly['date'].strftime('%Y-%m-%d')}: ${anomaly['cost']:.2f} (Z-score: {anomaly['z_score']:.2f})")
