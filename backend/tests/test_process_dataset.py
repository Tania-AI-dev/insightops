

import pandas as pd
import pytest

from backend.app.services import process_dataset


def test_pipeline_stops_when_validation_fails(tmp_path, monkeypatch):
    # Create an invalid dataset with missing required columns
    invalid_dataframe = pd.DataFrame({
        "Ticket ID": [101],
        "Customer Age": [25],
    })

    output_path = tmp_path / "processed_dataset.csv"

    # Replace the real CSV loader with our test dataset
    monkeypatch.setattr(
        process_dataset,
        "load_csv",
        lambda file_path: invalid_dataframe,
    )

    # Redirect output to a temporary test directory
    monkeypatch.setattr(
        process_dataset,
        "PROCESSED_DATA_PATH",
        output_path,
    )

    # The pipeline should reject the invalid dataset
    with pytest.raises(ValueError, match="Dataset validation failed"):
        process_dataset.process_dataset()

    # No processed file should be created
    assert not output_path.exists()
