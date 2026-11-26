

import logging

import pandas as pd


logger = logging.getLogger(__name__)


TEXT_COLUMNS = [
    "Customer Name",
    "Customer Email",
    "Customer Gender",
    "Product Purchased",
    "Ticket Type",
    "Ticket Subject",
    "Ticket Description",
    "Ticket Status",
    "Ticket Priority",
    "Ticket Channel",
]


NUMERIC_COLUMNS = [
    "Ticket ID",
    "Customer Age",
    "Customer Satisfaction Rating",
    "First Response Time",
    "Time to Resolution",
]


def clean_dataset(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardise customer support ticket data.

    Returns a cleaned copy without modifying the original DataFrame.
    """

    cleaned_dataframe = dataframe.copy()

    # Standardise whitespace in text columns
    for column in TEXT_COLUMNS:
        if column in cleaned_dataframe.columns:
            cleaned_dataframe[column] = (
                cleaned_dataframe[column]
                .astype("string")
                .str.strip()
            )

    # Convert numeric columns
    for column in NUMERIC_COLUMNS:
        if column in cleaned_dataframe.columns:
            cleaned_dataframe[column] = pd.to_numeric(
                cleaned_dataframe[column],
                errors="coerce",
            )

    # Convert purchase dates into datetime format
    if "Date of Purchase" in cleaned_dataframe.columns:
        cleaned_dataframe["Date of Purchase"] = pd.to_datetime(
            cleaned_dataframe["Date of Purchase"],
            errors="coerce",
        )

    logger.info(
        "Dataset cleaning completed | Rows: %s | Columns: %s",
        cleaned_dataframe.shape[0],
        cleaned_dataframe.shape[1],
    )

    return cleaned_dataframe
