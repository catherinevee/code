# scripts/pr_cost_attribution.py
import subprocess
import json
import re
from datetime import datetime, timedelta

class PRCostAnalyzer:
    def __init__(self):
        self.cost_per_resource = {
            'aws_instance': {
                't3.micro': 8.76,    # Monthly cost
                't3.small': 17.52,
                't3.medium': 35.04,
                'm5.large': 70.08,
                'm5.xlarge': 140.16
            },
            'aws_db_instance': {
                'db.t3.micro': 13.14,
                'db.t3.small': 26.28,
                'db.t3.medium': 52.56,
                'db.r5.large': 158.40
            },
            'aws_s3_bucket': 0.023,  # Per GB per month
            'aws_lb': 16.43  # Monthly for ALB
        }

    def analyze_pr_cost_impact(self, pr_diff):
        """Analyze the cost impact of a pull request"""

        added_resources = self.extract_added_resources(pr_diff)
        removed_resources = self.extract_removed_resources(pr_diff)
        modified_resources = self.extract_modified_resources(pr_diff)

        cost_impact = {
            'added_monthly_cost': self.calculate_resource_costs(added_resources),
            'removed_monthly_cost': self.calculate_resource_costs(removed_resources),
            'modified_cost_delta': self.calculate_modification_costs(modified_resources),
            'resources_summary': {
                'added': len(added_resources),
                'removed': len(removed_resources),
                'modified': len(modified_resources)
            }
        }

        cost_impact['net_monthly_change'] = (
            cost_impact['added_monthly_cost'] -
            cost_impact['removed_monthly_cost'] +
            cost_impact['modified_cost_delta']
        )

        return cost_impact

    def extract_added_resources(self, diff_text):
        """Extract newly added resources from git diff"""
        added_resources = []

        # Look for added resource blocks
        resource_pattern = r'\+resource\s+"([^"]+)"\s+"([^"]+)"'
        matches = re.findall(resource_pattern, diff_text)

        for resource_type, resource_name in matches:
            # Extract configuration from the diff
            config = self.extract_resource_config(diff_text, resource_type, resource_name, '+')
            added_resources.append({
                'type': resource_type,
                'name': resource_name,
                'config': config
            })

        return added_resources

    def extract_removed_resources(self, diff_text):
        """Extract removed resources from git diff"""
        removed_resources = []

        # Look for removed resource blocks
        resource_pattern = r'\-resource\s+"([^"]+)"\s+"([^"]+)"'
        matches = re.findall(resource_pattern, diff_text)

        for resource_type, resource_name in matches:
            config = self.extract_resource_config(diff_text, resource_type, resource_name, '-')
            removed_resources.append({
                'type': resource_type,
                'name': resource_name,
                'config': config
            })

        return removed_resources

    def extract_resource_config(self, diff_text, resource_type, resource_name, prefix):
        """Extract resource configuration from diff"""
        # Simplified config extraction - in practice, you'd use a proper HCL parser
        config = {}

        if resource_type == 'aws_instance':
            instance_type_pattern = f'{prefix}\\s*instance_type\\s*=\\s*"([^"]+)"'
            match = re.search(instance_type_pattern, diff_text)
            if match:
                config['instance_type'] = match.group(1)

        elif resource_type == 'aws_db_instance':
            instance_class_pattern = f'{prefix}\\s*instance_class\\s*=\\s*"([^"]+)"'
            match = re.search(instance_class_pattern, diff_text)
            if match:
                config['instance_class'] = match.group(1)

        return config

    def calculate_resource_costs(self, resources):
        """Calculate monthly cost for a list of resources"""
        total_cost = 0

        for resource in resources:
            resource_type = resource['type']
            config = resource['config']

            if resource_type == 'aws_instance' and 'instance_type' in config:
                instance_type = config['instance_type']
                if instance_type in self.cost_per_resource[resource_type]:
                    total_cost += self.cost_per_resource[resource_type][instance_type]

            elif resource_type == 'aws_db_instance' and 'instance_class' in config:
                instance_class = config['instance_class']
                if instance_class in self.cost_per_resource[resource_type]:
                    total_cost += self.cost_per_resource[resource_type][instance_class]

            elif resource_type in ['aws_s3_bucket', 'aws_lb']:
                total_cost += self.cost_per_resource.get(resource_type, 0)

        return total_cost

    def calculate_modification_costs(self, modified_resources):
        """Calculate cost delta for modified resources"""
        # Simplified - would need before/after comparison
        return 0  # Placeholder

    def generate_pr_cost_comment(self, cost_impact, pr_number):
        """Generate a cost impact comment for the PR"""

        net_change = cost_impact['net_monthly_change']
        emoji = "💰" if net_change > 0 else "💚" if net_change < 0 else "➡️"

        comment = f"## {emoji} Cost Impact Analysis\n\n"

        if abs(net_change) < 0.01:
            comment += "✅ **No significant cost impact detected**\n\n"
        else:
            comment += f"**Net Monthly Cost Change: ${net_change:+.2f}**\n\n"

            if cost_impact['added_monthly_cost'] > 0:
                comment += f"📈 **Added Resources**: +${cost_impact['added_monthly_cost']:.2f}/month\n"

            if cost_impact['removed_monthly_cost'] > 0:
                comment += f"📉 **Removed Resources**: -${cost_impact['removed_monthly_cost']:.2f}/month\n"

            comment += "\n"

            # Add context
            if net_change > 100:
                comment += "⚠️ **High Impact**: This change adds significant monthly costs. "
                comment += "Please ensure this aligns with project budget.\n\n"
            elif net_change > 50:
                comment += "📊 **Medium Impact**: Notable cost increase. "
                comment += "Consider if all resources are necessary.\n\n"

            # Add cost-saving suggestions
            if cost_impact['resources_summary']['added'] > 0:
                comment += "💡 **Cost Optimization Tips**:\n"
                comment += "- Consider using smaller instance types for development environments\n"
                comment += "- Review if all resources need to run 24/7\n"
                comment += "- Check if spot instances are suitable for non-critical workloads\n\n"

        comment += "---\n"
        comment += "*Cost estimates are based on list prices and may vary based on usage patterns and discounts.*"

        return comment

# Example usage in CI/CD
if __name__ == "__main__":
    # Get the diff for current PR
    diff_command = ["git", "diff", "origin/main...HEAD", "--", "*.tf"]
    diff_output = subprocess.check_output(diff_command, text=True)

    analyzer = PRCostAnalyzer()
    cost_impact = analyzer.analyze_pr_cost_impact(diff_output)

    comment = analyzer.generate_pr_cost_comment(cost_impact, "123")
    print(comment)
