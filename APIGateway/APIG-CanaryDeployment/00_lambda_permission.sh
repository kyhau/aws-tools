ACC_ID=1231456789012
APIG_ID=todo_apig_id
FUNCTION=K-SFN-Function-B
ALIAS=green

aws lambda add-permission \
  --function-name "arn:aws:lambda:ap-southeast-2:${ACC_ID}:function:${FUNCTION}:${ALIAS}" \
  --source-arn "arn:aws:execute-api:ap-southeast-2:${ACC_ID}:${APIG_ID}/*/GET/execution" \
  --principal apigateway.amazonaws.com --action lambda:InvokeFunction \
  --statement-id ${FUNCTION}-$ALIAS-1
