import pandas as pd

def summary(df: pd.DataFrame):
    return {
        "row_count": df.shape[0],
        "column_count": df.shape[1]
    }