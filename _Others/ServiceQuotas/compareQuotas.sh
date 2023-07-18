#!/bin/bash
# Source: https://aws.amazon.com/blogs/mt/service-quota-observability-across-regions-and-accounts/
#
# To run:
#     chmod +x compareQuotas.sh
#     ./compareQuotas.sh <profile1> <region1> <profile2> <region2>
#     ./compareQuotas.sh --help
#     ./compareQuotas.sh --cleanup
# Examples:
#     ./compareQuotas.sh dev us-east-1 dev us-east2      < This compares quotas between the dev profile in us-east-1 and us-east-2
#     ./compareQuotas.sh dev us-east-1 prod us-east-1    < This compares quotas between the dev account in us-east-1 to the prod account in us-east-1
#     ./compareQuotas.sh dev us-east-1 prod us-east-2    < This compares quotas between the dev account in us-east-1 and the prod account in us-east-1
#
# Differences are sent to the screen and put in a file called quota-differences-<profile1>-<region1>-<profile2>-<region2>-differences.txt
# For the example the output file would be: quota-differences-dev-us-east-1-prod-us-east-2-differencess.txt
# Change MAX_AGE_OF_DATA to non-negative value if you would like to cache quotas and re-use them for comparisons. Age unit is in days.
#
OUTPUT_DIRECTORY="./compareQuotasDataFiles"
ALL_AWS_SERVICES_FILE="$OUTPUT_DIRECTORY/all_aws_services"
MAX_AGE_OF_DATA="-1"

function show_help() {
    echo "Usage:"
    echo "    ./compareQuotas.sh <profileName1> <region1> <profileName2> <region2> "
    echo "    ./compareQuotas.sh --cleanup"
    echo "Examples:"
    echo "    ./compareQuotas.sh \"dev\" \"us-east-1\" \"prod\" \"us-east2\""
    echo "    ./compareQuotas.sh --cleanup"
    echo "    ./compareQuotas.sh --help"
    echo "    ./compareQuotas.sh"
}

function removeOldFile() {
    if [ -f $1 ]; then
        if [[ $(find "$1" -mtime +$MAX_AGE_OF_DATA -print) ]]; then
            echo "File $1 exists and is older than $MAX_AGE_OF_DATA days, removing file"
            rm -rf $1
        fi
    fi
}

function getQuotasForAccount() {
    SERVICES_FILE="$ALL_AWS_SERVICES_FILE-$1-$2.txt"
    aws service-quotas list-services --profile $1 --region $2 --query Services[*].ServiceCode --output text | tr '\t' '\n' > $SERVICES_FILE
    if [ $? -ne 0 ]; then
        echo "running command failed: aws service-quotas list-services --region $2 --query Services[*].ServiceCode --output text"
        rm $SERVICES_FILE
        exit
    fi

    QUOTAS_FILE="$OUTPUT_DIRECTORY/quotas-$1-$2.txt"
    FINAL_QUOTAS_FILE="$OUTPUT_DIRECTORY/final-quotas-$1-$2.txt"
    echo "QUOTAS_FILE: $QUOTAS_FILE"
    echo "FINAL_QUOTAS_FILE: $FINAL_QUOTAS_FILE"

    removeOldFile $QUOTAS_FILE
    if [ ! -f $QUOTAS_FILE ]; then
        for service in `cat $SERVICES_FILE`; do
            echo "Get Quotas for profile $1 region $2 service: $service"
            aws service-quotas list-service-quotas --profile $1 --service-code $service --region $2 --output text >> $QUOTAS_FILE
            if [ $? -ne 0 ]; then
                echo "running command failed: aws service-quotas list-service-quotas --service-code $service --region $1 --output text"
                rm $QUOTAS_FILE
                exit
            fi
        done

        # remove unwanted lines and choose the columns we are interested in
        grep -E '^(QUOTAS)' $QUOTAS_FILE | cut -d : -f 6- | sort > $FINAL_QUOTAS_FILE
    else
        echo "Use cached data for region $FINAL_QUOTAS_FILE"
    fi
}

function verifyValidRegionName() {
    if [[ "$1" == "" ]]; then
        echo "you must specify two regions"
        show_help
        exit -1
    fi

}

if [[ "$1" == "--cleanup" ]]; then
    echo "cleanup removing $OUTPUT_DIRECTORY"
    rm -rf $OUTPUT_DIRECTORY
    exit -1
fi

if [[ "$1" == "--help" ]]; then
    show_help
    exit -1
fi

if [[ "$4" == "" ]]; then
    echo "Must specify two profile names and two regions"
    show_help
    exit -1
fi

verifyValidRegionName $2
verifyValidRegionName $4

if [ ! -d "$OUTPUT_DIRECTORY" ]; then
    mkdir $OUTPUT_DIRECTORY
fi

# Create file for first profile/region:
getQuotasForAccount $1 $2

# Create file for second profile/region:
getQuotasForAccount $3 $4

# Find the differences
echo "========== FINAL DIFFERENCES OUTPUT ========="
diff -yb --suppress-common-lines -W 450 $OUTPUT_DIRECTORY/final-quotas-$1-$2.txt $OUTPUT_DIRECTORY/final-quotas-$3-$4.txt | tee $OUTPUT_DIRECTORY/quota-differences-$1-$2-$3-$4.txt
