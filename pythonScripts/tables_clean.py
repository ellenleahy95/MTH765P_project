import numpy as np
import pandas as pd
from pathlib import Path
import re

tables = pd.read_csv("../Data/tables/tables_all.csv")

# Split top team scorer column by the - to create two new columns, top scorer and top scorer num goals
tables[['Top Scorer', 'Top Scorer Num Goals']] = tables['Top Team Scorer'].str.split(' - ', 1, expand=True)
# Remove oroginal column as no longer needed
tables = tables.drop(['Top Team Scorer'], axis=1)

# Output new table
tables.to_csv("../Data/tables/tables_clean.csv", mode='w+')