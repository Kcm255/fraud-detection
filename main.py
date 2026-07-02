from engine.parser import read_json_logs
from engine.validator import validate_records
from engine.feature_engineering import extract_features
from engine.classifier import classify_score
from engine.report_generator import generate_reports
from rules.fraud_rules import evaluate_record


def main():

    # -----------------------------
    # Read Logs
    # -----------------------------

    records = read_json_logs()

    print(f"Total Records Read : {len(records)}")

    # -----------------------------
    # Validate
    # -----------------------------

    valid_records, invalid_records = validate_records(records)

    print(f"Valid Records      : {len(valid_records)}")
    print(f"Invalid Records    : {len(invalid_records)}")

    # -----------------------------
    # Feature Engineering
    # -----------------------------

    features = extract_features(valid_records)

    # -----------------------------
    # Fraud Detection
    # -----------------------------

    results = []

    print("\n========== FRAUD ANALYSIS ==========\n")

    for record in valid_records:

        result = evaluate_record(record, features)

        status = classify_score(result["risk_score"])

        output = {
            "timestamp": record["timestamp"],
            "Txn": record["Txn"],
            "risk_score": result["risk_score"],
            "status": status,
            "reasons": result["reasons"]
        }

        results.append(output)

        print("----------------------------------")
        print("Timestamp  :", output["timestamp"])
        print("Transaction:", output["Txn"])
        print("Risk Score :", output["risk_score"])
        print("Status     :", output["status"])
        print("Reasons    :", output["reasons"])
        print()

    # -----------------------------
    # Generate Reports
    # -----------------------------

    generate_reports(results)


if __name__ == "__main__":
    main()