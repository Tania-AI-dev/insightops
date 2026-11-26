
import logging
from pathlib import Path

from backend.app.services.data_ingestion import load_csv
from backend.app.services.data_validation import validate_dataset
from backend.app.services.data_cleaning import clean_dataset


logger = logging.getLogger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "customer_support_tickets.csv"
)

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_support_tickets_cleaned.csv"
)


def process_dataset():
    # Step 1: Load raw data
    dataframe = load_csv(str(RAW_DATA_PATH))

    # Step 2: Validate raw data
    validation_report = validate_dataset(dataframe)

    if not validation_report.is_valid:
        for error in validation_report.errors:
            logger.error("Validation error: %s", error)

        raise ValueError(
            "Dataset validation failed. Processing stopped."
        )

    for warning in validation_report.warnings:
        logger.warning("Validation warning: %s", warning)

    # Step 3: Clean validated data
    cleaned_dataframe = clean_dataset(dataframe)

    # Step 4: Save processed data
    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    cleaned_dataframe.to_csv(
        PROCESSED_DATA_PATH,
        index=False,
    )

    logger.info(
        "Processed dataset saved to: %s",
        PROCESSED_DATA_PATH,
    )

    print(f"Processed dataset saved: {PROCESSED_DATA_PATH}")
    print(f"Total records: {len(cleaned_dataframe)}")

    return cleaned_dataframe


if __name__ == "__main__":
    process_dataset()
