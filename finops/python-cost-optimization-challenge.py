# scripts/cost_optimization_challenges.py
from datetime import datetime, timedelta
import random

class CostOptimizationChallenges:
    def __init__(self):
        self.challenges = [
            {
                'name': 'Right-Size October',
                'description': 'Identify and right-size over-provisioned resources',
                'target_savings': 15,  # Percentage
                'duration_days': 30,
                'difficulty': 'medium',
                'points': 500
            },
            {
                'name': 'Zombie Resource Hunt',
                'description': 'Find and eliminate unused resources',
                'target_savings': 10,
                'duration_days': 14,
                'difficulty': 'easy',
                'points': 300
            },
            {
                'name': 'Spot Instance Champion',
                'description': 'Convert appropriate workloads to spot instances',
                'target_savings': 25,
                'duration_days': 21,
                'difficulty': 'hard',
                'points': 750
            },
            {
                'name': 'Storage Optimization Specialist',
                'description': 'Implement S3 lifecycle policies and optimize storage',
                'target_savings': 20,
                'duration_days': 14,
                'difficulty': 'medium',
                'points': 400
            }
        ]

    def start_monthly_challenge(self):
        """Start a new monthly cost optimization challenge"""

        current_challenge = random.choice(self.challenges)

        print(f"🎯 NEW CHALLENGE: {current_challenge['name']}")
        print("=" * 50)
        print(f"📝 Description: {current_challenge['description']}")
        print(f"🎯 Target: {current_challenge['target_savings']}% cost reduction")
        print(f"⏰ Duration: {current_challenge['duration_days']} days")
        print(f"🔥 Difficulty: {current_challenge['difficulty'].title()}")
        print(f"🏆 Reward: {current_challenge['points']} points")
        print()

        # Generate specific tasks based on challenge type
        tasks = self.generate_challenge_tasks(current_challenge)

        print("📋 CHALLENGE TASKS:")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task}")

        print()
        print("🚀 Ready to start? Use these commands to begin:")
        print("  • Run cost analysis: python scripts/cost_analyzer.py")
        print("  • Generate optimization report: python scripts/optimization_finder.py")
        print("  • Track progress: python scripts/challenge_tracker.py")

        return current_challenge

    def generate_challenge_tasks(self, challenge):
        """Generate specific tasks for each challenge type"""

        task_templates = {
            'Right-Size October': [
                'Analyze EC2 instance utilization for the last 30 days',
                'Identify instances with <40% average CPU utilization',
                'Create right-sizing recommendations with cost impact',
                'Implement changes in development environment first',
                'Measure actual cost savings after optimization'
            ],
            'Zombie Resource Hunt': [
                'Scan for resources without recent activity',
                'Identify unattached EBS volumes and snapshots',
                'Find load balancers with no healthy targets',
                'Locate unused security groups and network interfaces',
                'Clean up test resources older than 30 days'
            ],
            'Spot Instance Champion': [
                'Identify fault-tolerant workloads suitable for spot instances',
                'Set up spot instance configurations with proper diversification',
                'Implement spot instance termination handling',
                'Migrate development/testing workloads to spot instances',
                'Monitor spot instance savings and availability'
            ],
            'Storage Optimization Specialist': [
                'Analyze S3 storage usage patterns',
                'Implement lifecycle policies for infrequently accessed data',
                'Optimize EBS volume types based on IOPS requirements',
                'Set up intelligent tiering for S3 buckets',
                'Review and optimize backup retention policies'
            ]
        }

        return task_templates.get(challenge['name'], ['Complete the challenge objectives'])

    def track_challenge_progress(self, team_name, completed_tasks):
        """Track team progress on current challenge"""

        total_tasks = 5  # Standard number of tasks per challenge
        completion_percentage = (completed_tasks / total_tasks) * 100

        print(f"📊 CHALLENGE PROGRESS: {team_name.upper()} TEAM")
        print("=" * 40)
        print(f"Tasks Completed: {completed_tasks}/{total_tasks}")
        print(f"Progress: {completion_percentage:.1f}%")

        # Progress bar
        filled = int(completion_percentage // 10)
        bar = "█" * filled + "░" * (10 - filled)
        print(f"[{bar}] {completion_percentage:.1f}%")

        if completion_percentage >= 100:
            print("🎉 CHALLENGE COMPLETED! 🎉")
            print("Calculating final savings and awarding points...")
        elif completion_percentage >= 75:
            print("🔥 Almost there! Just a few more tasks to go!")
        elif completion_percentage >= 50:
            print("💪 Great progress! You're halfway done!")
        else:
            print("🚀 Keep going! Every task completed gets you closer!")

        return completion_percentage

# Example usage
challenges = CostOptimizationChallenges()

# Start a new challenge
current_challenge = challenges.start_monthly_challenge()

# Track progress for a team
progress = challenges.track_challenge_progress('backend', 3)
