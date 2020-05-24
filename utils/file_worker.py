from pathlib import Path
import os
import logging

import pandas as pd


def write_to_file(
    data: pd.DataFrame, ext="csv", filename="result"
):
    save_data = {"csv": data.to_csv, "parquet": data.to_parquet}
    directory = Path(__file__).parents[1] / "datasets/all_datasets"
    if not os.path.exists(directory):
        os.makedirs(directory)
    if ext in save_data:
        file = os.path.join(directory, ".".join([filename, ext]))
        if os.path.exists(file):
            old_df = read_from_file(file, ext)
            new_df = old_df.append(data, ignore_index=True)
            save_new_df = {"csv": new_df.to_csv, "parquet": new_df.to_parquet}
            save_new_df[ext](file)
        else:
            save_data[ext](file)
    else:
        logging.error("Not supported extension for file")


def read_from_file(file: str, ext="csv"):
    file_extensions = {"csv": pd.read_csv, "parquet": pd.read_parquet}
    return file_extensions[ext](file).drop(columns=['Unnamed: 0'])
