"""
This script exports a DynamoDB table to S3 bucket.
It exports the table to a point in time (PITR) which is the current time minus the number of days specified.
The export is in DYNAMODB_JSON format and is a FULL_EXPORT.
The script waits for the export to complete and writes the export manifest to a file.
The script also downloads the exported data from S3, unzips the files, and merges the data into a single JSON file, then upload back to S3.
"""
import json
import os
import time
from datetime import datetime, timedelta

import boto3

TABLES = {
    "TODO-ddb-table-name": {
        "earliest_pitr": datetime(2024, 10, 2, 10, 11),  # UTC, TODO
    },
}

S3_BUCKET_NAME = "TODO"
SLEEP_TIME = 10  # seconds
MAX_ITERATION = int(30 * 60 / SLEEP_TIME)  # 30 minutes

TABLE_NAME = os.environ.get("TABLE_NAME")
TABLE_ARN = os.environ.get("TABLE_ARN")
DAYS = os.environ.get("DAYS", 1)
DAYS = int(DAYS) if DAYS else 1
S3_PREFIX = os.environ.get("S3_PREFIX", "default-backup")

CURRENT_TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M%S")

ddb_client = boto3.client("dynamodb")
s3_client = boto3.client("s3")


class DynamoDBExporter:
    def __init__(self, table_name: str, table_arn: str, bucket_name: str):
        self.table_name = table_name
        self.table_arn = table_arn
        self.bucket_name = bucket_name

    def export_ddb_to_s3(self, days: int, s3_prefix: str) -> str:
        # Cannot be earlier than the earliest point in time recovery (PITR) for the table
        export_time = max(
            datetime.now() - timedelta(days=days),
            TABLES[self.table_name]["earliest_pitr"],
        )
        export_arn = self._export_ddb_to_s3(
            table_arn=self.table_arn,
            s3_bucket_name=self.bucket_name,
            export_time=export_time,
            s3_prefix=s3_prefix,
        )
        if export_arn:
            return self._wait_for_export(export_arn)

    def _export_ddb_to_s3(
        self, table_arn: str, s3_bucket_name: str, export_time: datetime, s3_prefix: str
    ) -> str:
        try:
            print(f"Export Time: {export_time}")
            resp = ddb_client.export_table_to_point_in_time(
                TableArn=table_arn,
                S3Bucket=s3_bucket_name,
                ExportFormat="DYNAMODB_JSON",
                ExportTime=export_time,
                ExportType="FULL_EXPORT",
                S3Prefix=s3_prefix,
            )
            return resp.get("ExportDescription", {}).get("ExportArn")
        except Exception as e:
            print(e)

    def _wait_for_export(self, export_arn: str) -> str:
        print(f"Export ARN: {export_arn}")
        export_manifest = None
        try:
            for i in range(MAX_ITERATION):
                resp = ddb_client.describe_export(ExportArn=export_arn)
                export_status = resp.get("ExportDescription", {}).get("ExportStatus")

                if export_manifest is None:
                    export_manifest = resp.get("ExportDescription", {}).get(
                        "ExportManifest"
                    )

                print("Export Status: ", export_status)
                if export_status in ["COMPLETED", "FAILED"]:
                    print(f"Export {export_status} in {(i+1)*SLEEP_TIME} seconds.")
                    break
                print(
                    f"Waiting for {SLEEP_TIME} seconds... ({i + 1}/{MAX_ITERATION})\n"
                )
                time.sleep(SLEEP_TIME)
        except Exception as e:
            print(e)
        return export_manifest


"""
This script downloads the exported data from S3, unzips the files, and merges the data into a single JSON file, then upload back to S3.
"""
class DataMerger:
    def __init__(
        self,
        bucket_name: str,
        file_extension: str,
        input_s3_prefix: str,
        output_s3_folder: str,
    ):
        self.bucket_name = bucket_name
        self.file_extension = file_extension
        self.input_s3_prefix = input_s3_prefix
        self.output_s3_filename = f"{output_s3_folder}/{CURRENT_TIMESTAMP}.json"

    def merge_data(self) -> list:
        gz_file_list = self._list_s3_files_with_prefix(self.input_s3_prefix)
        lines = self._download_files_from_s3_and_retrieve_contents(gz_file_list)
        data = []
        for line in lines:
            data.append(json.loads(line))
        self.write_json_to_file("merged_data.json", data)
        self._upload_file_to_s3("merged_data.json")

    def _list_s3_files_with_prefix(self, key_prefix: str) -> list:
        files = []
        for items in (
            s3_client.get_paginator("list_objects_v2")
            .paginate(Bucket=self.bucket_name, Prefix=key_prefix)
            .result_key_iters()
        ):
            for item in items:
                if item["Key"].endswith(self.file_extension):
                    files.append(item["Key"])
        return files

    def _download_files_from_s3_and_retrieve_contents(self, file_list: list) -> None:
        lines = []
        for file in file_list:
            file_name = file.rsplit("/", 1)[-1]
            s3_client.download_file(self.bucket_name, file, file_name)
            os.system(f"gzip -d {file_name}")
            print(f"Downloaded {file_name} and unzip")
            json_filename = file_name.rsplit(".", 1)[0]
            lines.extend(self.read_file(json_filename))
        return lines

    def _upload_file_to_s3(self, file_name: str) -> None:
        s3_client.upload_file(file_name, self.bucket_name, self.output_s3_filename)

    @staticmethod
    def read_file(file_name):
        with open(file_name, "r") as f:
            return f.readlines()

    @staticmethod
    def write_json_to_file(file_name, data):
        with open(file_name, "w") as f:
            json.dump(data, f)


def main():
    if TABLE_NAME not in TABLES:
        raise ValueError(f"Table {TABLE_NAME} not found in TABLES")

    manifest = DynamoDBExporter(
        table_name=TABLE_NAME, table_arn=TABLE_ARN, bucket_name=S3_BUCKET_NAME
    ).export_ddb_to_s3(days=DAYS, s3_prefix=S3_PREFIX)

    if manifest:
        export_data_prefix = manifest.rsplit("/", 1)[0]
        print(export_data_prefix)

        DataMerger(
            bucket_name=S3_BUCKET_NAME,
            file_extension="gz",
            input_s3_prefix=export_data_prefix,
            output_s3_folder=TABLE_NAME,
        ).merge_data()


if __name__ == "__main__":
    main()
