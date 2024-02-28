import os
import pandas as pd
from google.cloud import bigquery

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "projekt1-415610-f19ebf54e064.json"  # lokalizacja pobranego klucza z punktu 1.4
client = bigquery.Client()

query = 'select * from ´bigquery-public-data.covid19_open_data.covid19_open_data´ limit 10'
query_job = client.query(query)
query_result = query_job.result()
df = query_result.to_dataframe()
