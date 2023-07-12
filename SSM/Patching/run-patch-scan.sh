
aws ssm send-command \
    --document-name "AWS-RunPatchBaseline" \
    --parameters '{"Operation":["Scan"]}' \
    --targets "Key=tag:Maintenance Window,Values=Every 15min"

# --targets "Key=instanceids,Values=i-123example456" \
