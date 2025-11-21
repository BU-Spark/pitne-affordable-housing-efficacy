import pandas as pd

def applicant_property_geocoding(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applicant + property geocoding cleaning step.

    Right now this is a no-op (it just returns df unchanged).
    The goal is to match the pipeline structure.
    Later we can add your real geocoding logic here.
    """
    return df
