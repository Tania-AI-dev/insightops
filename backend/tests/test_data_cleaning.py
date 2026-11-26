

import pandas as pd

from backend.app.services.data_cleaning import clean_dataset


def create_sample_dataset():
    return pd.DataFrame({
        "Ticket ID": ["101", "102"],
        "Customer Age": ["25", "35"],
        "Customer Name": [" Alice ", " Bob "],
        "Ticket Description": [" Payment issue ", " Product issue "],
        "Ticket Type": ["Billing inquiry", "Product inquiry"],
        "Ticket Status": ["Open", "Closed"],
        "Ticket Priority": ["High", "Medium"],
        "Ticket Channel": ["Email", "Chat"],
        "Date of Purchase": ["2024-01-15", "2024-02-20"],
        "Customer Satisfaction Rating": [4, None],
        "First Response Time": [None, None],
        "Time to Resolution": [None, None],
    })


def test_cleaning_converts_dates():
    dataframe = create_sample_dataset()

    cleaned = clean_dataset(dataframe)

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned["Date of Purchase"]
    )


def test_cleaning_removes_text_whitespace():
    dataframe = create_sample_dataset()

    cleaned = clean_dataset(dataframe)

    assert cleaned.loc[0, "Customer Name"] == "Alice"
    assert cleaned.loc[0, "Ticket Description"] == "Payment issue"


def test_cleaning_converts_numeric_columns():
    dataframe = create_sample_dataset()

    cleaned = clean_dataset(dataframe)

    assert pd.api.types.is_numeric_dtype(cleaned["Ticket ID"])
    assert pd.api.types.is_numeric_dtype(cleaned["Customer Age"])


def test_cleaning_preserves_original_data_and_rows():
    dataframe = create_sample_dataset()
    original_dataframe = dataframe.copy(deep=True)

    cleaned = clean_dataset(dataframe)

    pd.testing.assert_frame_equal(dataframe, original_dataframe)
    assert len(cleaned) == len(dataframe)
    assert cleaned["Customer Satisfaction Rating"].isna().sum() == 1
