# Traditional DevOps: Focus on functionality and performance
# FinOps-Enhanced DevOps: Add cost awareness to all decisions

class SmartDeploymentStrategy:
    def __init__(self):
        self.performance_targets = {
            'response_time_p95': 200,  # milliseconds
            'throughput_rps': 1000,    # requests per second
            'availability': 99.9       # percentage
        }

        # FinOps enhancement: Add cost constraints
        self.cost_constraints = {
            'max_cost_per_user': 0.10,    # dollars per month
            'max_infrastructure_cost': 5000,  # dollars per month
            'target_utilization': 70      # percentage
        }

    def select_deployment_configuration(self, expected_load):
        """Select optimal configuration balancing performance and cost"""

        configurations = [
            {
                'name': 'cost_optimized',
                'instances': self.calculate_minimum_instances(expected_load),
                'instance_type': 't3.medium',
                'estimated_cost': 450,
                'performance_score': 85
            },
            {
                'name': 'balanced',
                'instances': self.calculate_balanced_instances(expected_load),
                'instance_type': 'm5.large',
                'estimated_cost': 650,
                'performance_score': 95
            },
            {
                'name': 'performance_optimized',
                'instances': self.calculate_performance_instances(expected_load),
                'instance_type': 'm5.xlarge',
                'estimated_cost': 1200,
                'performance_score': 99
            }
        ]

        # FinOps decision framework: Choose based on cost-performance ratio
        best_config = self.optimize_cost_performance_ratio(configurations, expected_load)

        return best_config

    def optimize_cost_performance_ratio(self, configurations, expected_load):
        """Find the configuration with the best cost-performance ratio"""

        scored_configs = []

        for config in configurations:
            # Calculate cost per unit of performance
            cost_efficiency = config['performance_score'] / config['estimated_cost']

            # Check if it meets cost constraints
            cost_per_user = config['estimated_cost'] / expected_load
            meets_constraints = cost_per_user <= self.cost_constraints['max_cost_per_user']

            scored_configs.append({
                **config,
                'cost_efficiency': cost_efficiency,
                'meets_constraints': meets_constraints,
                'cost_per_user': cost_per_user
            })

        # Filter to only configurations that meet constraints
        valid_configs = [c for c in scored_configs if c['meets_constraints']]

        if not valid_configs:
            print("Warning: No configuration meets cost constraints!")
            return scored_configs[0]  # Return cheapest as fallback

        # Return the most cost-efficient valid configuration
        return max(valid_configs, key=lambda x: x['cost_efficiency'])

    def calculate_minimum_instances(self, expected_load):
        """Calculate minimum instances needed for the load"""
        # Simplified calculation - replace with actual capacity planning
        return max(2, expected_load // 500)

    def calculate_balanced_instances(self, expected_load):
        """Calculate balanced instance count with buffer"""
        return max(2, int(expected_load // 400 * 1.25))

    def calculate_performance_instances(self, expected_load):
        """Calculate instances for optimal performance"""
        return max(3, int(expected_load // 300 * 1.5))

# Example usage
strategy = SmartDeploymentStrategy()
optimal_config = strategy.select_deployment_configuration(expected_load=1000)

print(f"Selected configuration: {optimal_config['name']}")
print(f"Cost efficiency score: {optimal_config['cost_efficiency']:.3f}")
print(f"Monthly cost: ${optimal_config['estimated_cost']}")
print(f"Cost per user: ${optimal_config['cost_per_user']:.3f}")
