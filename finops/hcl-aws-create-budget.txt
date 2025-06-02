# terraform/monitoring/budgets.tf

# Organization-level budget
resource "aws_budgets_budget" "organization_monthly" {
  name       = "organization-monthly-budget"
  budget_type = "COST"
  limit_amount = "50000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filters {
    dimension {
      key    = "LINKED_ACCOUNT"
      values = var.account_ids
    }
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                 = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = ["finance@company.com", "cto@company.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                 = 100
    threshold_type            = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = ["finance@company.com", "cto@company.com"]
  }
}

# Team-specific budgets using cost allocation tags
resource "aws_budgets_budget" "team_budgets" {
  for_each = var.team_budgets

  name        = "${each.key}-monthly-budget"
  budget_type = "COST"
  limit_amount = each.value.amount
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filters {
    tag {
      key    = "team"
      values = [each.key]
    }
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                 = 75
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = each.value.notification_emails
  }
}
