
import logging

import pandas as pd


logger = logging.getLogger(__name__)


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file and return its contents as a Pandas DataFrame.
    """

    try:
        dataframe = pd.read_csv(file_path)

        logger.info(
            "Successfully loaded dataset: %s | Rows: %s | Columns: %s",
            file_path,
            dataframe.shape[0],
            dataframe.shape[1],
        )

        return dataframe

    except FileNotFoundError:
        logger.error("Dataset not found: %s", file_path)
        raise

    except pd.errors.EmptyDataError:
        logger.error("Dataset is empty: %s", file_path)
        raise