
from utils.odk import get_odk_client
import pandas as pd

def get_gps_metrics(form_id: str) -> pd.DataFrame:
    client = get_odk_client()
    submissions = client.submissions.get_table(form_id=form_id)
    
    if submissions.empty:
        return pd.DataFrame(columns=['latitude', 'longitude', 'submission_date'])

    gps_columns = [col for col in submissions.columns if 'latitude' in col or 'longitude' in col or 'gps' in col or 'geopoint' in col]

    if len(gps_columns) == 1 and ' ' in str(submissions[gps_columns[0]].iloc[0]):
        submissions[['latitude', 'longitude']] = submissions[gps_columns[0]].str.split(' ', expand=True)[[0, 1]]
    elif 'latitude' in submissions.columns and 'longitude' in submissions.columns:
        pass
    else:
        submissions['latitude'] = None
        submissions['longitude'] = None

    submissions['submission_date'] = pd.to_datetime(
        submissions.get('end') or submissions.get('submission_time') or pd.Timestamp.now()
    )

    return submissions

def get_filter_options(df: pd.DataFrame, columns: list) -> dict:
    options = {}
    for col in columns:
        if col in df.columns:
            unique_vals = df[col].dropna().unique().tolist()
            unique_vals.sort()
            options[col] = ["Tous"] + unique_vals
    return options
