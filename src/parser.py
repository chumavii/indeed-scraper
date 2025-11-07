import pandas as pd
from typing import List, Dict

def to_dataframe(rows: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)