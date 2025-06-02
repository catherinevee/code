# scripts/performance_cost_analyzer.py

class PerformanceCostAnalyzer:
    def __init__(self):
        self.instance_specs = {
            't3.small': {'vcpu': 2, 'memory': 2, 'cost_per_hour': 0.0208},
            't3.medium': {'vcpu': 2, 'memory': 4, 'cost_per_hour': 0.0416},
            't3.large': {'vcpu': 2, 'memory': 8, 'cost_per_hour': 0.0832},
            'm5.large': {'vcpu': 2, 'memory': 8, 'cost_per_hour': 0.096},
            'm5.xlarge': {'vcpu': 4, 'memory': 16, 'cost_per_hour': 0.192},
            'm5.2xlarge': {'vcpu': 8, 'memory': 32, 'cost_per_hour': 0.384}
        }

    def analyze_performance_cost_options(self, workload_requirements):
        """Analyze different instance options for a workload"""

        print("🔍 PERFORMANCE vs COST ANALYSIS")
        print("=" * 50)

        suitable_instances = []

        for instance_type, specs in self.instance_specs.items():
            if (specs['vcpu'] >= workload_requirements.get('min_vcpu', 1) and
                specs['memory'] >= workload_requirements.get('min_memory', 1)):

                monthly_cost = specs['cost_per_hour'] * 24 * 30

                # Calculate efficiency metrics
                cost_per_vcpu = monthly_cost / specs['vcpu']
                cost_per_gb_memory = monthly_cost / specs['memory']

                suitable_instances.append({
                    'instance_type': instance_type,
                    'vcpu': specs['vcpu'],
                    'memory': specs['memory'],
                    'monthly_cost': monthly_cost,
                    'cost_per_vcpu': cost_per_vcpu,
                    'cost_per_gb_memory': cost_per_gb_memory,
                    'efficiency_score': self.calculate_efficiency_score(specs, monthly_cost)
                })

        # Sort by cost
        suitable_instances.sort(key=lambda x: x['monthly_cost'])

        print(f"{'Instance':<12} {'vCPU':<6} {'Memory':<8} {'Monthly Cost':<14} {'Efficiency'}")
        print("-" * 60)

        for instance in suitable_instances:
            efficiency_emoji = self.get_efficiency_emoji(instance['efficiency_score'])
            print(f"{instance['instance_type']:<12} {instance['vcpu']:<6} "
                  f"{instance['memory']:<8} ${instance['monthly_cost']:<13.2f} {efficiency_emoji}")

        print()

        # Provide recommendations
        if suitable_instances:
            cheapest = suitable_instances[0]
            most_efficient = max(suitable_instances, key=lambda x: x['efficiency_score'])

            print("💡 RECOMMENDATIONS:")
            print(f"   💰 Lowest Cost: {cheapest['instance_type']} (${cheapest['monthly_cost']:.2f}/month)")
            print(f"   ⚡ Best Efficiency: {most_efficient['instance_type']} (score: {most_efficient['efficiency_score']:.2f})")

            if cheapest != most_efficient:
                cost_difference = most_efficient['monthly_cost'] - cheapest['monthly_cost']
                print(f"   📊 Efficiency Premium: ${cost_difference:.2f}/month ({cost_difference/cheapest['monthly_cost']*100:.1f}%)")

        return suitable_instances

    def calculate_efficiency_score(self, specs, monthly_cost):
        """Calculate efficiency score (performance per dollar)"""
        # Simple efficiency: (vCPU + memory/4) / monthly_cost * 100
        performance_score = specs['vcpu'] + (specs['memory'] / 4)
        return (performance_score / monthly_cost) * 100

    def get_efficiency_emoji(self, score):
        """Get emoji representation of efficiency score"""
        if score > 20:
            return "🟢 Excellent"
        elif score > 15:
            return "🟡 Good"
        elif score > 10:
            return "🟠 Fair"
        else:
            return "🔴 Poor"

# Example usage
analyzer = PerformanceCostAnalyzer()

# Analyze options for a web application
web_app_requirements = {
    'min_vcpu': 2,
    'min_memory': 4,
    'workload_type': 'web_application'
}

suitable_options = analyzer.analyze_performance_cost_options(web_app_requirements)
