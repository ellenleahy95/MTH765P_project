# import numpy as np
import pandas as pd
from pathlib import Path
import re

for p in Path('.').glob('../Data/[a-z,A-Z]*'):
    df = pd.DataFrame()

    filepath = "../Data/" + p.name + "/*.csv"
    for f in Path('.').glob(filepath):
	    # Extract season from filename
	    filename = f.name
	    result = re.search('[a-z,A-Z]*_(.*).csv', filename)
	    season = result.group(1)[:2] + "-" + result.group(1)[2:]

	    temp = pd.read_csv("../Data/" + p.name + "/" + filename) 
	    temp.insert(1, 'season', season)

	    df = pd.concat([df, temp])


    df.to_csv("../Data/" + p.name + "/" + p.name + "_all.csv", mode='w+')


