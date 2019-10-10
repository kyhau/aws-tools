#!/bin/bash
# Set to fail script if any command fails.
set -e

# Change the following
declare -a PREFIXES=(
  "some-key-1"
  "some-key-2"
)
BUCKET_NAME="todo"
DAYS=10
GLACIER_RESTORE_LIST="glacier-restore.txt"


[[ -f "$GLACIER_RESTORE_LIST" ]] && rm "$GLACIER_RESTORE_LIST"

for key_prefix in "${PREFIXES[@]}"
do
  aws s3 ls "s3://${BUCKET_NAME}/${key_prefix}" --recursive | \
    awk '{print $4}' | sed 's#s3://${BUCKET_NAME}/##' >> "$GLACIER_RESTORE_LIST"
done

while IFS= read -r item
do
  echo "Restoring $item"
  aws s3api restore-object --bucket "$BUCKET_NAME" --key "$item" --restore-request Days="$DAYS"
done < "$GLACIER_RESTORE_LIST"
