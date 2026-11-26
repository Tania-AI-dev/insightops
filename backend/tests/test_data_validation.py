

import pandas as pd

from backend.app.services.data_validation import validate_dataset

def create_valid_dataset():
    """Create a small valid dataset for testing."""

    return pd.DataFrame({
        "Ticket ID": [101, 102],
        "Customer Age": [25, 35],
        "Date of Purchase": ["2024-01-15", "2024-02-20"],
        "Ticket Description": ["Payment issue", "Product issue"],
        "Ticket Type": ["Billing inquiry", "Product inquiry"],
        "Ticket Status": ["Open", "Closed"],
        "Ticket Priority": ["High", "Medium"],
        "Ticket Channel": ["Email", "Chat"],
        "Customer Satisfaction Rating": [4, 5],
    })

def test_valid_dataset_passes():
    dataframe = create_valid_dataset()

    report = validate_dataset(dataframe)

    assert report.is_valid is True
    assert report.errors == []

def test_duplicate_ticket_ids_are_rejected():
    dataframe = create_valid_dataset()
    dataframe.loc[1, "Ticket ID"] = 101

    report = validate_dataset(dataframe)

    assert report.is_valid is False
    assert "Duplicate ticket IDs found." in report.errors

def test_invalid_satisfaction_rating_is_rejected():
    dataframe = create_valid_dataset()
    dataframe.loc[0, "Customer Satisfaction Rating"] = 7

    report = validate_dataset(dataframe)

    assert report.is_valid is False
    assert any(
        "satisfaction ratings" in error
        for error in report.errors
    )

def test_missing_required_column_is_rejected():
    dataframe = create_valid_dataset()
    dataframe = dataframe.drop(columns=["Ticket Priority"])

    report = validate_dataset(dataframe)

    assert report.is_valid is False
    assert any(
        "Missing required columns" in error
        for error in report.errors
    )