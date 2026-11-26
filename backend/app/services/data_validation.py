

import logging
from dataclasses import dataclass, field

import pandas as pd


logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = [
    "Ticket ID",
    "Customer Age",
    "Date of Purchase",
    "Ticket Description",
    "Ticket Type",
    "Ticket Status",
    "Ticket Priority",
    "Ticket Channel",
    "Customer Satisfaction Rating",
]

ALLOWED_VALUES = {
    "Ticket Type": {
        "Billing inquiry",
        "Cancellation request",
        "Refund request",
        "Technical issue",
        "Product inquiry",
    },
    "Ticket Status": {
        "Open",
        "Pending Customer Response",
        "Closed",
    },
    "Ticket Priority": {
        "Low",
        "Medium",
        "High",
        "Critical",
    },
    "Ticket Channel": {
        "Chat",
        "Social media",
        "Phone",
        "Email",
        "Web",
    },
}


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def validate_dataset(dataframe: pd.DataFrame) -> ValidationReport:
    report = ValidationReport()

    if dataframe.empty:
        report.errors.append("Dataset is empty.")
        return report

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        report.errors.append(
            f"Missing required columns: {missing_columns}"
        )
        return report

    # Check ticket IDs
    if dataframe["Ticket ID"].isna().any():
        report.errors.append("Ticket IDs contain missing values.")

    if dataframe["Ticket ID"].duplicated().any():
        report.errors.append("Duplicate ticket IDs found.")

    # Check customer age
    ages = pd.to_numeric(dataframe["Customer Age"], errors="coerce")

    if ages.isna().any():
        report.errors.append("Customer ages contain missing or invalid values.")

    if ((ages < 18) | (ages > 100)).any():
        report.errors.append("Customer ages must be between 18 and 100.")

    # Check satisfaction ratings
    ratings = pd.to_numeric(
        dataframe["Customer Satisfaction Rating"],
        errors="coerce",
    )

    invalid_ratings = (
        dataframe["Customer Satisfaction Rating"].notna()
        & (ratings.isna() | (ratings < 1) | (ratings > 5))
    )

    if invalid_ratings.any():
        report.errors.append(
            "Customer satisfaction ratings must be between 1 and 5."
        )

    if dataframe["Customer Satisfaction Rating"].isna().any():
        report.warnings.append(
            "Some customer satisfaction ratings are missing."
        )

    # Check purchase dates
    dates = pd.to_datetime(
        dataframe["Date of Purchase"],
        errors="coerce",
    )

    if dates.isna().any():
        report.errors.append(
            "Date of Purchase contains missing or invalid dates."
        )

    # Check ticket descriptions
    descriptions = dataframe["Ticket Description"].astype("string")

    if descriptions.isna().any() or descriptions.str.strip().eq("").any():
        report.errors.append(
            "Ticket descriptions contain missing or empty values."
        )

    # Check categorical values
    for column, allowed_values in ALLOWED_VALUES.items():
        unexpected_values = (
            set(dataframe[column].dropna().unique())
            - allowed_values
        )

        if unexpected_values:
            report.errors.append(
                f"Unexpected values in {column}: {unexpected_values}"
            )

    # Check operational fields that are entirely missing
    optional_columns = [
        "Resolution",
        "First Response Time",
        "Time to Resolution",
    ]

    for column in optional_columns:
        if column in dataframe.columns and dataframe[column].isna().all():
            report.warnings.append(
                f"{column} is completely empty and cannot support analysis."
            )

    if dataframe.duplicated().any():
        report.warnings.append(
            "The dataset contains duplicate rows."
        )

    logger.info(
        "Dataset validation completed | Valid: %s | Errors: %s | Warnings: %s",
        report.is_valid,
        len(report.errors),
        len(report.warnings),
    )

    return report
