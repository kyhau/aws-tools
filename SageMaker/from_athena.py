#import sys
#!{sys.executable} -m pip install pyathena

from pyathena import connect
import pandas as pd

conn = connect(s3_staging_dir='s3://aws-athena-query-results-459817416023-us-east-1/', region_name='us-east-1')
df = pd.read_sql('SELECT * FROM "ticketdata"."nfl_stadium_data" order by stadium limit 10;', conn)
df