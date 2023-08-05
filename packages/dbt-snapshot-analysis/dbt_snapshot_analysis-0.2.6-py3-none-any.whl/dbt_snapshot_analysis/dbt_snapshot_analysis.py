import pandas as pd
import streamlit as st
from typing import List
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


from snapshot_utils import get_metric_by_month, get_snapshot_as_of_date, determine_type


@st.cache_data()
def compute_all_metric_day_by_day(local_df: pd.DataFrame, date_range: List[str]):
    print("Computing metric day by day...")
    all_monthly_metrics = pd.DataFrame()
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    index = 0
    for day in date_range:
        index += 1
        day_date = datetime.strptime(day, "%Y-%m-%d")
        current_df = get_snapshot_as_of_date(local_df, day_date)
        if current_df.empty:
            continue
        metric_by_month = get_metric_by_month(
            current_df, "metric_value", "metric_date", "%Y-%m"
        )
        metric_by_month["computation_day"] = day_date.date()
        all_monthly_metrics = pd.concat(
            [all_monthly_metrics, metric_by_month], ignore_index=True
        )
        progress = index / date_range.__len__()
        my_bar.progress(progress, text=progress_text)

    my_bar.empty()

    return all_monthly_metrics


def is_numeric_column(df, column_name):
    try:
        pd.to_numeric(df[column_name])
        return True
    except ValueError:
        return False


def is_date_column(df, column_name):
    try:
        pd.to_datetime(df[column_name])
        return True
    except ValueError:
        return False


@st.cache_data()
def parse_csv_file(uploaded_file):
    if uploaded_file is None:
        return pd.DataFrame()
    print("Parsing uploaded file...")
    local_df = pd.read_csv(uploaded_file, low_memory=False)

    print(type(local_df["dbt_valid_from"].iloc[0]))
    datetime_format = determine_type(local_df["dbt_valid_from"].iloc[0])
    print(f"Date format: {datetime_format}")
    # format dates
    try:
        if datetime_format == "timestamp":
            local_df["is_current_version"] = local_df["dbt_valid_to"].isnull()
            local_df["dbt_valid_from"] = pd.to_datetime(
                local_df["dbt_valid_from"], unit="s"
            )
            now = pd.Timestamp.now().timestamp()
            local_df["dbt_valid_to"] = local_df["dbt_valid_to"].fillna(now)
            local_df["dbt_valid_to"] = pd.to_datetime(
                local_df["dbt_valid_to"], unit="s"
            )
        else:
            local_df["is_current_version"] = local_df["dbt_valid_to"].isnull()
            local_df["dbt_valid_from"] = pd.to_datetime(local_df["dbt_valid_from"])
            now = pd.Timestamp.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
            local_df["dbt_valid_to"] = local_df["dbt_valid_to"].fillna(now)
            local_df["dbt_valid_to"] = pd.to_datetime(local_df["dbt_valid_to"])
    except ValueError as e:
        invalid_row_index = int(str(e).split(" ")[-1])
        print(f"Invalid row index: {invalid_row_index}")

    print(f"Number of rows: {local_df.shape[0]}")
    print(f"Number of columns: {local_df.shape[1]}")
    return local_df


@st.cache_data()
def get_metric_value_and_date(local_df, metric_column, date_column):
    is_numeric_column_valid = is_numeric_column(local_df, metric_column)
    is_date_column_valid = is_date_column(local_df, date_column)
    if is_numeric_column_valid and is_date_column_valid:
        local_df["metric_value"] = local_df[metric_column]
        local_df["metric_date"] = local_df[date_column]

        local_df = local_df[
            (local_df["metric_date"].notnull()) & (local_df["metric_value"].notnull())
        ]
    else:
        st.write("Please select a valid metric column and a date column")
    return local_df


def run():
    firstCol1, firstCol2 = st.columns(2)
    df = pd.DataFrame()
    with firstCol1:
        uploaded_file = st.file_uploader("Choose a file")

    with firstCol2:
        if uploaded_file is not None:
            df = parse_csv_file(uploaded_file)
            unique_id_column = st.selectbox("Select unique id column", df.columns)

    if not df.empty:
        tab1, tab2, tab3 = st.tabs(["Version", "Lifespan", "Data"])
        with tab1:
            st.markdown("## Distribution of versions per ID")
            st.header("Version distribution")
            unique_ids = df.groupby(unique_id_column).size()
            print(f"Number of unique ids: {unique_ids.shape[0]}")
            versions_per_id = (
                df.groupby(unique_id_column).size().reset_index(name="version per id")
            )
            versions_count = (
                versions_per_id["version per id"].value_counts().sort_index()
            )

            st.bar_chart(versions_count)

        with tab2:
            lifespandf = df.copy()
            lifespandf["lifespan"] = (
                lifespandf["dbt_valid_to"] - lifespandf["dbt_valid_from"]
            )
            print(lifespandf["lifespan"].describe())
            lifespandf["lifespan_numeric"] = pd.to_numeric(
                lifespandf["lifespan"], errors="coerce"
            )
            lifespandf["lifespan (days)"] = lifespandf["lifespan"].dt.days
            print(lifespandf["lifespan (days)"].describe())

            all_versions = lifespandf["lifespan (days)"]
            dead_versions = lifespandf[lifespandf["is_current_version"] == False][
                "lifespan (days)"
            ]

            lifespan_df_with_alive = pd.DataFrame(
                dict(
                    series=np.concatenate(
                        (
                            ["lifespan all rows (days)"] * len(all_versions),
                            ["lifespan without active (days)"] * len(dead_versions),
                        )
                    ),
                    data=np.concatenate((all_versions, dead_versions)),
                )
            )

            fig = px.histogram(
                lifespan_df_with_alive,
                x="data",
                color="series",
                barmode="overlay",
                nbins=50,
            )

            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.header("Dataframe")
            st.write(df)

        min_date = df["dbt_valid_from"].min()
        max_date = df["dbt_valid_from"].max()
        date_range = pd.date_range(start=min_date, end=max_date)
        date_range_str = date_range.strftime("%Y-%m-%d").tolist()

        metric_distribution_df = df.copy()

        col1, col2, col3 = st.columns(3)

        with col1:
            is_metric_or_count = st.radio("Metric", ["Count", "Sum"])

        with col2:
            date_column = st.selectbox(
                "Select metric date column", metric_distribution_df.columns
            )
            is_date_column_valid = is_date_column(metric_distribution_df, date_column)
            if not is_date_column_valid:
                st.warning(
                    "Please select a valid date column, it should be supported by pandas.to_datetime."
                )

        with col3:
            is_numeric_column_valid = False
            if is_metric_or_count == "Sum":
                metric_column = st.selectbox(
                    "Select metric column to sum", metric_distribution_df.columns
                )
                is_numeric_column_valid = is_numeric_column(
                    metric_distribution_df, metric_column
                )
                if not is_numeric_column_valid:
                    st.warning(
                        "Please select a valid metric column, it should be a numeric column."
                    )
            else:
                metric_distribution_df["count"] = 1
                metric_column = "count"
                is_numeric_column_valid = True

        if is_numeric_column_valid and is_date_column_valid:
            metric_distribution_df_with_formated_date = get_metric_value_and_date(
                metric_distribution_df, metric_column, date_column
            )

            all_results = compute_all_metric_day_by_day(
                metric_distribution_df_with_formated_date, date_range_str
            )

            all_results = all_results[all_results["metric_value"] > 0]

            all_results["latest_value"] = (
                all_results.sort_values(
                    ["metric_date", "computation_day"], ascending=[True, False]
                )
                .groupby("metric_date")["metric_value"]
                .transform("first")
            )

            all_results["relative_value"] = (
                all_results["metric_value"] / all_results["latest_value"]
            )

            all_monthly_volatility = (
                all_results[all_results["metric_value"] > 0]
                .groupby("metric_date")["relative_value"]
                .std()
            )

            print("all_monthly_volatility", all_monthly_volatility)

            grouped_df = all_results.groupby("metric_date")

            st.set_option("deprecation.showPyplotGlobalUse", False)
            fig = go.Figure()

            for metric_name, group in grouped_df:
                fig.add_trace(
                    go.Scatter(
                        x=group["computation_day"],
                        y=group["relative_value"],
                        name=metric_name,
                    )
                )

            fig.update_layout(
                title="Metric Value Over Time",
                xaxis_title="Computation Day",
                yaxis_title="Metric Value",
                showlegend=True,
            )
            st.plotly_chart(fig)

            st.subheader("Monthly volatility")

            st.dataframe(all_monthly_volatility)


def main():
    run()


if __name__ == "__main__":
    main()
