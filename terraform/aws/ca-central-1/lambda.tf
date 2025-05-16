data "archive_file" "lambda" {
  type        = "zip"
  source_file = "lambda/index.js"
  output_path = "lambda/lambda.zip"
}

resource "aws_lambda_function" "lambda" {
  filename      = data.archive_file.lambda.output_path
  function_name = "my-first-tf-lambda-function"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "nodejs18.x"

  timeout = 15
  memory_size = 1024
  environment {
    variables = {
      PRODUCTION = false
    }
}
}

resource "aws_lambda_function_url" "lambda" {
  function_name      = aws_lambda_function.lambda.function_name
  authorization_type = "NONE"
}