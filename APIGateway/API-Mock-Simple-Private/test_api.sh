
# Make sure that your VPC has
# - "EnableDnsSupport" : "true",
# - "EnableDnsHostnames" : "true",

# If the Lambda is attached to a public subnet with internet access, then call

aws lambda invoke --function-name FUNCTION_NAME

# else
# Login in to Lambda console and use the Test button instead
