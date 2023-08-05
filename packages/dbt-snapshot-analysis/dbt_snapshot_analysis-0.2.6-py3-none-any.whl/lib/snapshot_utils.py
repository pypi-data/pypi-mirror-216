import pandas as pd


def get_snapshot_as_of_date(df: pd.DataFrame, current_day: pd.Timestamp):
    """
    Returns a snapshot of the DataFrame as of a given date.

    Parameters:
    df (pandas.DataFrame): The snapshot DataFrame, with columns 'dbt_valid_from' and 'dbt_valid_to'.
    as_of_date (pandas.Timestamp): The date to snapshot the DataFrame as of.

    Returns:
    pandas.DataFrame: A snapshot of the DataFrame as of the given date.
    """

    valid_df = df[
        (df["dbt_valid_from"] <= current_day) & (current_day < df["dbt_valid_to"])
    ]

    return valid_df


import pandas as pd


def get_metric_by_month(
    df: pd.DataFrame, metric_value_col: str, metric_date_col: str, date_format="%Y-%m"
) -> pd.DataFrame:
    """
    Returns a DataFrame with the monthly sum of a metric value column.

    Parameters:
    df (pandas.DataFrame): The DataFrame to aggregate.
    metric_value_col (str): The name of the column containing the metric values.
    metric_date_col (str): The name of the column containing the metric dates.

    Returns:
    pandas.DataFrame: A DataFrame with the monthly sum of the metric value column.
    """
    df_copy = df.copy()
    df_copy[metric_date_col] = pd.to_datetime(df_copy[metric_date_col], unit="s")
    df_copy["metric_date"] = df_copy[metric_date_col].dt.strftime(date_format)
    monthly_sum = df_copy.groupby("metric_date")[metric_value_col].sum().reset_index()
    return monthly_sum
