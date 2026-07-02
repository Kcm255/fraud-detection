import json
import csv
import os

from config import (
    OUTPUT_FOLDER,
    JSON_REPORT,
    CSV_REPORT
)


def generate_json_report(results):
    """
    Saves fraud detection results as a JSON file.
    """

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    json_path = os.path.join(OUTPUT_FOLDER, JSON_REPORT)

    with open(json_path, "w") as file:
        json.dump(results, file, indent=4)

    print(f"JSON report saved to: {json_path}")


def generate_csv_report(results):
    """
    Saves fraud detection results as a CSV file.
    """

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    csv_path = os.path.join(OUTPUT_FOLDER, CSV_REPORT)

    with open(csv_path, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Timestamp",
            "Transaction",
            "Risk Score",
            "Status",
            "Reasons"
        ])

        for result in results:

            writer.writerow([
                result["timestamp"],
                result["Txn"],
                result["risk_score"],
                result["status"],
                ", ".join(result["reasons"])
            ])

    print(f"CSV report saved to: {csv_path}")


def generate_reports(results):
    """
    Generates all project reports.
    """

    generate_json_report(results)
    generate_csv_report(results)