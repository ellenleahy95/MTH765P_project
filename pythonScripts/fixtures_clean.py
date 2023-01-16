import numpy as np
import pandas as pd
from pathlib import Path
import re

fixtures = pd.read_csv("../Data/fixtures/fixtures_all.csv")


fixtures = fixtures[fixtures['Score'].notna()]

fixtures = fixtures.rename(columns={'xG': 'xG Home Team', 'xG.1': 'xG Away Team'})
fixtures[['Home Goals', 'Away Goals']] = fixtures['Score'].str.split('–', 1, expand=True)

# Output new table
fixtures.to_csv("../Data/fixtures/fixtures_clean.csv", mode='w+')