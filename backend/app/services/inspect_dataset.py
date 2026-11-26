
import pandas as pd
from pathlib import Path

from backend.app.services.data_ingestion import load_csv


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "customer_support_tickets.csv"
)


def inspect_dataset():
    dataframe = load_csv(str(DATASET_PATH))

    print("\n========== DATASET OVERVIEW ==========")

    print("\nFirst 5 records:")
    print(dataframe.head())

    print("\nDataset dimensions:")
    print(dataframe.shape)

    print("\nColumn names:")
    print(dataframe.columns.tolist())

    print("\nData types:")
    print(dataframe.dtypes)

    print("\nMissing values:")
    print(dataframe.isnull().sum())

    print("\nDuplicate records:")
    print(dataframe.duplicated().sum())

    print("\n========== DATA QUALITY INVESTIGATION ==========")

    print("\nUnique ticket IDs:")
    print(dataframe["Ticket ID"].nunique())

    print("\nTicket ID duplicates:")
    print(dataframe["Ticket ID"].duplicated().sum())

    print("\nCategorical column values:")

    categorical_columns = [
        "Ticket Type",
        "Ticket Status",
        "Ticket Priority",
        "Ticket Channel",
        "Customer Gender",
    ]

    for column in categorical_columns:
        print(f"\n{column}:")
        print(dataframe[column].value_counts(dropna=False))

    print("\nNumeric column statistics:")
    print(
        dataframe[
            [
                "Customer Age",
                "Customer Satisfaction Rating",
            ]
        ].describe()
    )

    print("\nPurchase date parsing:")

    parsed_dates = pd.to_datetime(
        dataframe["Date of Purchase"],
        errors="coerce",
    )

    print("Unparseable dates:", parsed_dates.isna().sum())
    print("Earliest date:", parsed_dates.min())
    print("Latest date:", parsed_dates.max())


if __name__ == "__main__":
    inspect_dataset()
