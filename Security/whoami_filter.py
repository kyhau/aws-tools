"""
Given a output file of whoami.py, check if any rule statement matching the keywords in the given filter file.
A keyword starting with "/" means match the whole keyword.
"""
import click
import json
import logging
from os.path import basename

from arki_common import init_logging

APP_NAME = basename(__file__).split(".")[0]
OUTPUT_FILE = f"{APP_NAME}.json"
LOG_FILE = None    # or LOG_FILE = f"{APP_NAME}.log"

logger = init_logging(name=APP_NAME, log_level=logging.INFO, log_file=LOG_FILE)


@click.command()
@click.option("--whoami-file", "-w", default="whoami.json", help="The output file of the whoami script")
@click.option("--filter-file", "-f", required=True, help="Filter file")
def main(whoami_file, filter_file):

    # Load the output file of whoami.py
    with open(whoami_file) as f:
        data = json.load(f)

    # Load the filter-file
    with open(filter_file) as f:
        filters = [line.strip() for line in f.readlines()]

    logger.info(f"Filters: {filters}")

    for account_id, id_arn_block in data.items():
        for id_arn, id_content in id_arn_block.items():
            for topic, content in id_content.items():
                if not topic.startswith("Attached"):
                    continue
                for policy_arn, policy_list in content.items():
                    for statement in policy_list:
                        # Only check "Allow" rules
                        if statement["Effect"] != "Allow":
                            continue
                        statement["Action"] = [
                            rule for rule in statement["Action"]
                            if rule in [
                                rule for f in filters if
                                  (f.startswith("/") and f[1:] == rule) or
                                  (not f.startswith("/") and f in rule)
                            ]
                        ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)

    logger.info(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__": main()
