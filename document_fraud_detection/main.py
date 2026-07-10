from engine.document_loader import load_documents
from engine.text_extractor import extract_text
from engine.field_extractor import extract_fields
from engine.validator import validate_document
from engine.database_lookup import find_user
from engine.comparator import compare_fields
from rules.document_rules import evaluate_document
from engine.classifier import classify_score


def main():

    documents = load_documents()

    print("\n========== DOCUMENT FRAUD DETECTION ==========\n")

    for document_type, file_path in documents.items():

        if file_path is None:
            print(f"{document_type} not found.\n")
            continue

        print("=" * 70)
        print(document_type.upper())
        print("=" * 70)

        # ------------------------------------------------
        # OCR
        # ------------------------------------------------

        text = extract_text(file_path)

        # ------------------------------------------------
        # Field Extraction
        # ------------------------------------------------

        fields = extract_fields(document_type, text)

        print("\nExtracted Fields")

        print(fields)

        # ------------------------------------------------
        # Validation
        # ------------------------------------------------

        validation = validate_document(document_type, fields)

        print("\nValidation")

        print("Valid :", validation["valid"])

        if validation["errors"]:

            print("Errors:")

            for error in validation["errors"]:
                print("-", error)

            continue

        else:

            print("No Validation Errors")

        # ------------------------------------------------
        # Database Lookup
        # ------------------------------------------------

        user = find_user(fields)

        print("\nDatabase Lookup")

        if user:

            print("User Found")

        else:

            print("User Not Found")

        # ------------------------------------------------
        # Comparator
        # ------------------------------------------------

        comparison = compare_fields(document_type, fields, user)

        print("\nComparison Result")

        for key, value in comparison.items():

            print(f"{key:20}: {value}")

        # ------------------------------------------------
        # Rule Engine
        # ------------------------------------------------

        result = evaluate_document(comparison)

        print("\nFraud Analysis")

        print("Risk Score :", result["risk_score"])

        print("Reasons :")

        if result["reasons"]:

            for reason in result["reasons"]:
                print("-", reason)

        else:

            print("No Issues Found")

        # ------------------------------------------------
        # Classification
        # ------------------------------------------------

        status = classify_score(result["risk_score"])

        print("\nFinal Classification")

        print("Status :", status)

        print("\n")


if __name__ == "__main__":
    main()