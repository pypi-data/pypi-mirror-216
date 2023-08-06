import pandas as pd
import streamlit as st
import numpy as np

from lib.snapshot_utils import get_metric_by_month, get_snapshot_as_of_date
import matplotlib.pyplot as plt
from argparse import ArgumentParser


def run(df: pd.DataFrame):
    st.markdown("# Snapshot Analytics")

    # User should update the metric column to be the metric you want to use for your snapshot
    df["metric_value"] = df["mrr"]  # Update here
    df["metric_date"] = df["started_at"]  # Update here

    # Filter out rows with null values in metric_date or metric_value
    df = df[(df["metric_date"].notnull()) & (df["metric_value"].notnull())]

    # format dates
    try:
        df["dbt_valid_from"] = pd.to_datetime(df["dbt_valid_from"], unit="s")
        now = pd.Timestamp.now().timestamp()
        df["dbt_valid_to"] = df["dbt_valid_to"].fillna(now)
        df["dbt_valid_to"] = pd.to_datetime(df["dbt_valid_to"], unit="s")
    except ValueError as e:
        invalid_row_index = int(str(e).split(" ")[-1])
        print(f"Invalid row index: {invalid_row_index}")

    print(f"Number of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")

    if st.checkbox("Show dataframe"):
        st.write(df)

    unique_ids = df.groupby("id").size()
    print(f"Number of unique ids: {unique_ids.shape[0]}")
    versions_per_id = df.groupby("id").size().reset_index(name="num_versions")
    versions_count = versions_per_id["num_versions"].value_counts().sort_index()

    st.markdown("## Distribution of versions per ID")
    st.bar_chart(versions_count)

    df["lifespan"] = df["dbt_valid_to"] - df["dbt_valid_from"]
    print(df["lifespan"].describe())
    df["lifespan_numeric"] = pd.to_numeric(df["lifespan"], errors="coerce")
    df["lifespan_days"] = df["lifespan_numeric"] / 86400

    # st.bar_chart(df["lifespan_days"])

    min_date = df["dbt_valid_from"].min()
    max_date = df["dbt_valid_from"].max()
    date_range = pd.date_range(start=min_date, end=max_date)
    all_results = pd.DataFrame()
    for day in date_range:
        current_df = get_snapshot_as_of_date(df, day)
        metric_by_month = get_metric_by_month(
            current_df, "metric_value", "metric_date", "%Y-%m"
        )
        metric_by_month["computation_day"] = day.date()
        all_results = pd.concat([all_results, metric_by_month], ignore_index=True)

    grouped_df = all_results.groupby("metric_date")

    st.set_option("deprecation.showPyplotGlobalUse", False)

    for metric_name, group in grouped_df:
        plt.plot(group["computation_day"], group["metric_value"], label=metric_name)

        # Add a title and axis labels
        plt.title("Metric Value Over Time")
        plt.xlabel("Computation Day")
        plt.ylabel("Metric Value")
        plt.legend()

        # Display the plot using streamlit
    st.pyplot()


def main():
    parser = ArgumentParser()
    parser.add_argument("--path", type=str, default=None)
    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the value of the --path argument
    csv_file_path = args.path

    df = pd.read_csv(csv_file_path, low_memory=False)

    run(df)


if __name__ == "__main__":
    main()
