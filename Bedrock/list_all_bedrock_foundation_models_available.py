#!/usr/bin/env python3
"""
List Bedrock LLM-capable foundation models supported in at least one scope:
- single region `ap-southeast-2` (ON_DEMAND),
- cross-region `AU`,
- cross-region `US`.

For models that also have an AU cross-region inference profile, this script
includes the AU profile id. AU-only models (i.e. those not present in the
ON_DEMAND list) are included as entries with `ap_southeast_2_model_id=None`.

It also detects US cross-region inference profiles (with `us.` prefix) and
sets `us_model_id` for the corresponding models.
"""

from __future__ import annotations

import argparse
import os
import csv
import re
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _iter_bedrock_pages(
    *, bedrock: Any, operation_name: str, operation_params: dict[str, Any]
) -> list[dict[str, Any]]:  # pragma: no cover (tested indirectly via CLI)
    """
    Yield pages for a Bedrock List* operation.

    Bedrock APIs support pagination via nextToken; paginator support differs
    between SDK versions and service endpoints. This helper tries botocore
    paginators first and falls back to manual `nextToken` loops.
    """

    # Prefer botocore paginator when available (it correctly handles token keys
    # for the specific operation).
    try:
        paginator = bedrock.get_paginator(operation_name)
        pages: list[dict[str, Any]] = []
        for page in paginator.paginate(**operation_params):
            pages.append(page)
        return pages
    except Exception:
        # Manual pagination fallback.
        pages = []
        next_token: str | None = None
        while True:
            params = dict(operation_params)
            if next_token:
                params["nextToken"] = next_token
            resp = getattr(bedrock, operation_name)(**params)
            pages.append(resp)
            next_token = resp.get("nextToken")
            if not next_token:
                break
        return pages


def list_bedrock_models_available(*, region: str) -> list[dict[str, Any]]:
    """
    Return a sorted list of dicts for Bedrock LLM-capable models, filtered to:
    - single-region ap-southeast-2 ON_DEMAND support, OR
    - cross-region AU support, OR
    - cross-region US support.

    Columns:
    - model_name
    - provider_name
    - output_modalities (comma-separated, e.g. TEXT, TEXT,IMAGE)
    - ap_southeast_2_model_id (set only if ON_DEMAND is supported in ap-southeast-2)
    - au_model_id (set if referenced by an AU cross-region inference profile)
    - us_model_id (set if referenced by a US cross-region inference profile)

    US cross-region support is detected from inference profiles whose
    `inferenceProfileId` starts with `us.`. Some Bedrock accounts expose the
    US cross-region profiles as `global.*` instead; in that case we map
    those `global.*` values into `us_model_id` (we do not expose them
    separately).
    """

    bedrock = boto3.client("bedrock", region_name=region)

    try:
        # 1) Collect all LLM-like foundation models from this region.
        #    We exclude embeddings by outputModalities == ['EMBEDDING'].
        models: list[dict[str, Any]] = []
        model_id_to_index: dict[str, int] = {}

        # list_foundation_models returns all models in a single response (no pagination).
        for model in bedrock.list_foundation_models().get("modelSummaries", []) or []:
            output_modalities = model.get("outputModalities", []) or []
            if "EMBEDDING" in output_modalities:
                continue
            if "TEXT" not in output_modalities:
                continue

            model_id = model.get("modelId")
            if not isinstance(model_id, str) or not model_id:
                continue

            inference_types = model.get("inferenceTypesSupported", []) or []
            input_modalities = model.get("inputModalities", []) or []
            models_entry = {
                "model_name": model.get("modelName"),
                "provider_name": model.get("providerName"),
                "input_modalities": ",".join(input_modalities),
                "output_modalities": ",".join(output_modalities),
                "ap_southeast_2_model_id": model_id if "ON_DEMAND" in inference_types else None,
                "au_model_id": None,
                "us_model_id": None,
            }
            model_id_to_index[model_id] = len(models)
            models.append(models_entry)

        # 2) Collect AU / US cross-region inference profiles and map their
        #    `models[].modelArn` to the foundation model id segment.
        au_profiles: list[dict[str, Any]] = []
        us_profiles: list[dict[str, Any]] = []
        # US inference profiles are expected to use `us.` prefixes.
        # In some accounts these appear as `global.*`; for output, we
        # rewrite `global.*` to `us.*` when populating `us_model_id`.

        # Cross-region inference profiles are SYSTEM_DEFINED.
        for page in _iter_bedrock_pages(
            bedrock=bedrock,
            operation_name="list_inference_profiles",
            operation_params={"typeEquals": "SYSTEM_DEFINED"},
        ):
            for p in page.get("inferenceProfileSummaries", []) or []:
                inference_profile_id = p.get("inferenceProfileId") or ""
                inference_profile_id_str = str(inference_profile_id)

                m = re.match(r"(?i)^(au|us|global)[.-]", inference_profile_id_str)
                if not m:
                    continue

                prefix = m.group(1).lower()
                if prefix == "au":
                    au_profiles.append(p)
                elif prefix == "us":
                    us_profiles.append(p)
                elif prefix == "global":
                    transformed_id = "us" + inference_profile_id_str[len("global"):]
                    p2 = dict(p)
                    p2["inferenceProfileId"] = transformed_id
                    us_profiles.append(p2)

        def _apply_profile(profile: dict[str, Any], *, target_field: str) -> None:
            inference_profile_id = profile.get("inferenceProfileId")
            if not isinstance(inference_profile_id, str) or not inference_profile_id:
                return

            models_list = profile.get("models", []) or []
            for model_ref in models_list:
                model_arn = (model_ref or {}).get("modelArn", "") or ""
                model_id_from_arn = model_arn.split("/")[-1] if "/" in model_arn else None
                if not isinstance(model_id_from_arn, str) or not model_id_from_arn:
                    continue

                idx = model_id_to_index.get(model_id_from_arn)
                if idx is None:
                    continue

                models[idx][target_field] = inference_profile_id

        for profile in au_profiles:
            _apply_profile(profile, target_field="au_model_id")
        for profile in us_profiles:
            _apply_profile(profile, target_field="us_model_id")

        # 3) Filter to models that match at least one inclusion criterion.
        filtered = [
            m
            for m in models
            if m.get("ap_southeast_2_model_id") or m.get("au_model_id") or m.get("us_model_id")
        ]

        # 4) Sort for stable output.
        def _sort_key(x: dict[str, Any]) -> tuple[str, str]:
            return (
                (x.get("provider_name") or ""),
                (x.get("model_name") or ""),
            )

        filtered.sort(key=_sort_key)
        return filtered

    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code", "Unknown")
        error_message = exc.response.get("Error", {}).get("Message", "Unknown error")
        raise RuntimeError(f"AWS ClientError ({error_code}): {error_message}") from exc
    except BotoCoreError as exc:
        raise RuntimeError("AWS BotoCoreError occurred while listing Bedrock models") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="List Bedrock LLM models supported in ap-southeast-2/AU/US")
    parser.add_argument(
        "--aws-region",
        default=os.getenv("AWS_DEFAULT_REGION", "ap-southeast-2"),
        help="AWS region (e.g. ap-southeast-2)",
    )
    parser.add_argument(
        "--output",
        default="bedrock-foundation-models.csv",
        help=(
            "Output file path. Default is a CSV file. "
            "If the filename ends with .tsv or .csv, output tab/CSV instead. "
            "Use \"\" to print to stdout."
        ),
    )
    args = parser.parse_args()

    models = list_bedrock_models_available(region=args.aws_region)

    fieldnames = [
        "model_name",
        "provider_name",
        "input_modalities",
        "output_modalities",
        "ap_southeast_2_model_id",
        "au_model_id",
        "us_model_id",
    ]

    def _to_row(m: dict[str, Any]) -> dict[str, str]:
        return {k: (str(m[k]) if m.get(k) is not None else "") for k in fieldnames}

    def _write_txt(f: Any) -> None:
        for m in models:
            row = _to_row(m)
            f.write(f"provider_name: {row['provider_name']}\n")
            f.write(f"model_name:    {row['model_name']}\n")
            f.write(f"input_modalities:  {row['input_modalities']}\n")
            f.write(f"output_modalities: {row['output_modalities']}\n")
            f.write(f"ap_southeast_2_model_id: {row['ap_southeast_2_model_id']}\n")
            f.write(f"au_model_id:   {row['au_model_id']}\n")
            f.write(f"us_model_id:   {row['us_model_id']}\n")
            f.write("\n")

    # Decide output format by extension; .csv is the default.
    out = args.output
    out_lower = out.lower() if out else ""
    if out_lower.endswith(".csv"):
        delimiter = ","
    elif out_lower.endswith(".tsv"):
        delimiter = "\t"
    else:
        delimiter = None

    if delimiter is None:
        import sys

        if out:
            with open(out, "w", encoding="utf-8") as f:
                _write_txt(f)
            print(f"[models] wrote {len(models)} entries to {out} (TXT)")
        else:
            _write_txt(sys.stdout)
    else:
        if out:
            with open(out, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                for m in models:
                    writer.writerow(_to_row(m))
            fmt = "CSV" if delimiter == "," else "TSV"
            print(f"[models] wrote {len(models)} entries to {out} ({fmt})")
        else:
            import sys

            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            for m in models:
                writer.writerow(_to_row(m))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

