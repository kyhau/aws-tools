import { Handler, SQSEvent, SQSRecord } from "aws-lambda"
import { Segment, setSegment, utils } from "aws-xray-sdk"

function createLambdaSegment(
    sqsRecord: SQSRecord,
    lambdaExecStartTime: number,
    functionName: string,
    functionArn: string,
    awsRequestId: string
): Segment {
    const traceHeaderStr = sqsRecord.attributes.AWSTraceHeader
    const traceData = utils.processTraceData(traceHeaderStr)
    const sqsSegmentEndTime = Number(sqsRecord.attributes.ApproximateFirstReceiveTimestamp) / 1000
    const lambdaSegment = new Segment(
        functionName,
        traceData.root,
        traceData.parent
    )
    lambdaSegment.origin = "AWS::Lambda::Function"
    lambdaSegment.start_time = lambdaExecStartTime - (lambdaExecStartTime - sqsSegmentEndTime)
    lambdaSegment.addPluginData({
        function_arn: functionArn,
        region: sqsRecord.awsRegion,
        request_id: awsRequestId
    })
    return lambdaSegment
}

export const handler: Handler<SQSEvent, void> = async (event, context): Promise<void> => {
    const lambdaExecStartTime = new Date().getTime() / 1000

    for (const sqsRecord of event.Records) {
        const lambdaSegment = createLambdaSegment(
            sqsRecord,
            lambdaExecStartTime,
            context.functionName,
            context.invokedFunctionArn,
            context.awsRequestId
        )
        setSegment(lambdaSegment)

        try {
            // Do something
        } finally {
            lambdaSegment.close()
        }
    }
}
