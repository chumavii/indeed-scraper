import re
import pandas as pd

def clean_basic(df: pd.DataFrame) -> pd.DataFrame:
    # Drop duplicates and empty rows
    df = df.drop_duplicates().dropna(how="all")

    if "salary" in df.columns:
        def clean_salary(s):
            if not isinstance(s, str):
                return ""
            if not re.search(r"\d", s):
                return ""

            s = s.replace("\xa0", " ")
            numbers = re.findall(r"\d+", s)
            big_nums = [n for n in numbers if len(n) >= 2]

            # If no meaningful numbers, blank it out
            if not big_nums:
                return ""

            return s.strip()

        df["salary"] = df["salary"].apply(clean_salary)

    # Strip whitespace from other string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
        
    return df