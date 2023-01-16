import numpy as np
import pandas as pd
from pathlib import Path
import re

pl = pd.read_csv("../Data/playerStats/playerStats_all.csv")

pl = pl.drop(['-additional', 'Unnamed: 23', 'Unnamed: 32'], axis=1)

# print(pl.head())

# Get column names and first row values (correct column names)
cols = list(pl.columns)
cols_2 = pl.iloc[[0]].to_numpy()[0]

i = 0
cols_new = []
cols_dict = {}
while i < len(cols):
	if re.search("(^Performance|^Expected)", cols[i]):
		#  Add Overall to cols with Performace or Expected at the beginning
		cols_new.append(cols_2[i] + " Overall")
	elif re.search("^Per 90.", cols[i]):
		#  Add per 90 to cols with Per 90 at the beginning
		cols_new.append(cols_2[i] + " per 90")
	elif cols[i] == "season":
		cols_new.append(cols[i])
	else:
		# for any other we can just take the original name
		cols_new.append(cols_2[i])
	# create dictionary with current and new column names
	cols_dict[cols[i]] = cols_new[i]
	i += 1

pl.rename(columns=cols_dict, inplace = True)

# Drop all rows that are actualy a subheader
pl = pl.drop(pl[pl.Rk == 'Rk'].index)

pl['Nation'] = pl['Nation'].fillna('unknown unknown')

pl['Nation'] = pl['Nation'].str.split(' ', n=1, expand=True)[1]

# Output new table
pl.to_csv("../Data/playerStats/playerStats_clean.csv", mode='w+')