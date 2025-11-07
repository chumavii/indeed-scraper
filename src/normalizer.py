import pandas as pd

def clean_basic(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    df = df.dropna(how="all")
    return df