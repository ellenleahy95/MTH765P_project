import pandas as pd
from pathlib import Path
import re

# iterate over each folder in Data
for p in Path('.').glob('../Data/[a-z,A-Z]*'):
	# create empty dataframe to write data to
    df = pd.DataFrame()

    # create filepath to read data from
    filepath = "../Data/" + p.name + "/*.csv"
    for f in Path('.').glob(filepath):
	    # Extract season from filename
	    filename = f.name
	    result = re.search('[a-z,A-Z]*_(.*).csv', filename)
	    season = result.group(1)[:2] + "-" + result.group(1)[2:]

	    # add from each file to a temporary dataframe
	    temp = pd.read_csv("../Data/" + p.name + "/" + filename) 
	    temp.insert(1, 'season', season)

	    # join temp datafram to main dataframe
	    df = pd.concat([df, temp])

	# output to a new CSV file
    df.to_csv("../Data/" + p.name + "/" + p.name + "_all.csv", mode='w+')


