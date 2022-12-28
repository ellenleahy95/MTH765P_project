import numpy as np
import pandas as pd
from pathlib import Path
import re

tables = pd.read_csv("../Data/tables/tables_all.csv")

# Create two new columns, one for the name of the top scorer and one for the number of goals
tables[['Top Scorer', 'Top Scorer Num Goals']] = tables['Top Team Scorer'].str.split(' - ', 1, expand=True)
# Remove oroginal column as no longer needed
tables = tables.drop(['Top Team Scorer'], axis=1)

# Output new table
tables.to_csv("../Data/tables/tables_clean.csv", mode='w+')