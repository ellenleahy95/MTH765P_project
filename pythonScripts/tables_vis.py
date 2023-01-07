# import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import colorsys
# from pathlib import Path
# import re

tables = pd.read_csv("../Data/tables/tables_clean.csv")

# output n evenly spaces colour in RGB
def chart_colours(N):
    colours=[]
    HSV = [(i*1.0/N, 1.0, 1.0) for i in range(N)]
    for colour in HSV:
        colours.append(colorsys.hsv_to_rgb(*colour))
    return colours

# Team top scorer v. Rank, coloured by season
seasons = tables['season'].unique()

colors = chart_colours(len(seasons))

col_map = {}
i = 0
while i < len(seasons):
	col_map[seasons[i]] = colors[i]
	i += 1

fig, ax = plt.subplots()
for s,c in zip(seasons, colors):
	temp = tables[(tables.season == s) ]
	plt.scatter(temp["Rk"], temp["Top Scorer Num Goals"], c=c)

plt.title('Top Scorer Goals Scored v Final League Rank')
plt.xlabel("Goals Scored by Team's top scorer")
plt.ylabel('Finishing position in League')

plt.legend(seasons)
plt.savefig('../vis/tables/topscorer_rank.png')
plt.close()

# Team scorer v Rank, coloured by team
squads = tables['Squad'].unique()
colors_squads = chart_colours(len(squads))


col_map = {}
i = 0
while i < len(squads):
	col_map[squads[i]] = colors_squads[i]
	i += 1

fig, ax = plt.subplots()
for s,c in zip(squads, colors_squads):
	temp = tables[(tables.Squad == s) ]
	plt.scatter(temp["Rk"], temp["Top Scorer Num Goals"], c=c)

plt.title('Top Scorer Goals Scored v Final League Rank')
plt.ylabel("Goals Scored by Team's top scorer")
plt.xlabel('Finishing position in League')

plt.legend(squads, bbox_to_anchor=(1.05, 1))
# plt.show( )
plt.savefig('../vis/tables/topscorer_rank_squad.png', bbox_inches='tight')
plt.close()

# Goals per Game
tables['Top Scorer Goals Per Game'] = tables["Top Scorer Num Goals"]/tables['MP']

fig, ax = plt.subplots()
for s,c in zip(squads, colors_squads):
	temp = tables[(tables.Squad == s) ]
	plt.scatter(temp["Rk"], temp["Top Scorer Goals Per Game"])

plt.title('Top Scorer Goals Scored Per Game v Final League Rank')
plt.ylabel("Goals Scored Per Game by Team's Top Scorer")
plt.xlabel('Finishing position in League')

plt.legend(squads, bbox_to_anchor=(1.05, 1))
plt.savefig('../vis/tables/topscorer_pergame_rank_squad.png', bbox_inches='tight')
plt.close()

# Attendance over time
avg_per_season = tables.groupby("season").mean().reset_index()

fig, ax = plt.subplots()
plt.plot(avg_per_season['season'], avg_per_season['Attendance'])
# ax.set_xticks(range(len(seasons)))
ax.set_xticklabels(['16-17', '17-18', '18-19', '19-20', '20-21', '21-22'])
plt.title('Average Attendance Per Season')
plt.ylabel("Average Match Attendance")
plt.xlabel('Season')

plt.savefig('../vis/tables/average_attendance.png')
plt.close()

# box and whisker plot for attendance
ax = tables.boxplot(column=['Attendance'], by=['season'])

plt.title('Average Attendance Per Team Per Season')
plt.ylabel("Team's Average Match Attendance")
plt.xlabel('Season')
plt.savefig('../vis/tables/attendance_boxwhisker.png')
plt.close()

# xG over time
avg_per_season_xg = avg_per_season[~avg_per_season['season'].isin(['16-17','17-18'])]
fig, ax = plt.subplots()
plt.plot(avg_per_season_xg['season'], avg_per_season_xg['xG'])
# ax.set_xticklabels(['18-19', '19-20', '20-21', '21-22'])
ax.set_xticklabels(avg_per_season_xg['season'].unique())
plt.title('Average xG Per Season')
plt.ylabel("Average Match xG")
plt.xlabel('Season')

plt.savefig('../vis/tables/average_xg.png')
plt.close()

# xG per game over time
fig, ax = plt.subplots()
plt.plot(avg_per_season_xg['season'], avg_per_season_xg['xG']/avg_per_season_xg['MP'])
ax.set_xticklabels(avg_per_season_xg['season'].unique())
plt.title('Average xG Per Season')
plt.ylabel("Average Match xG")
plt.xlabel('Season')


plt.savefig('../vis/tables/average_xg_pergame.png')
plt.close()

# xG per game over time corrected axis
fig, ax = plt.subplots()
plt.plot(avg_per_season_xg['season'], avg_per_season_xg['xG']/avg_per_season_xg['MP'])
ax.set_xticklabels(avg_per_season_xg['season'].unique())
plt.title('Average xG Per Season')
plt.ylabel("Average Match xG")
plt.xlabel('Season')

plt.ylim((0,1.7))
plt.savefig('../vis/tables/average_xg_pergame_newaxis.png')
plt.close()

# box and whisker plot for attendance
tables_xg = tables[~tables['season'].isin(['16-17', '17-18'])]
ax = tables_xg.boxplot(column=['xG'], by=['season'])

plt.title('Average xG Per Team Per Season')
plt.ylabel("Team's Average Match Attendance")
plt.xlabel('Season')

plt.savefig('../vis/tables/xg_boxwhisker.png')
plt.close()

