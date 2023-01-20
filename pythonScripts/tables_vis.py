import matplotlib.pyplot as plt
import pandas as pd
import colorsys

# set fontsize for all charts
plt.rcParams.update({'font.size': 12})

tables = pd.read_csv("../Data/tables/tables_clean.csv")
###############
# Goals       #
############### 
### NOT USED ###
# output n evenly spaces colour in RGB
def chart_colours(N):
    colours=[]
    HSV = [(i*1.0/N, 1.0, 1.0) for i in range(N)]
    for colour in HSV:
        colours.append(colorsys.hsv_to_rgb(*colour))
    return colours

# Chart: Team top scorer v. Rank, coloured by season
# get unique list of seasons
seasons = tables['season'].unique()

# generate a colour for each season
colors = chart_colours(len(seasons))

# assign a colour per season
col_map = {}
i = 0
while i < len(seasons):
	col_map[seasons[i]] = colors[i]
	i += 1

# create scatter plot for each season and colour
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

# Chart: Team scorer v Rank, coloured by team
### NOT USED ###
# get unique list of squads
squads = tables['Squad'].unique()

# generate a colour for each squad and assign 
colors_squads = chart_colours(len(squads))
col_map = {}
i = 0
while i < len(squads):
	col_map[squads[i]] = colors_squads[i]
	i += 1

# plot a scatter plot for each squad
fig, ax = plt.subplots()
for s,c in zip(squads, colors_squads):
	temp = tables[(tables.Squad == s) ]
	plt.scatter(temp["Rk"], temp["Top Scorer Num Goals"], c=c)

plt.title('Top Scorer Goals Scored v Final League Rank')
plt.ylabel("Goals Scored by Team's top scorer")
plt.xlabel('Finishing position in League')

# create a legend and anchor such that the data is not covered
plt.legend(squads, bbox_to_anchor=(1.05, 1))

plt.savefig('../vis/tables/topscorer_rank_squad.png', bbox_inches='tight')
plt.close()

# Chart: Goals per Game
### NOT USED ###
# Calculate top scorers per number of games played
tables['Top Scorer Goals Per Game'] = tables["Top Scorer Num Goals"]/tables['MP']

# plot top scorer per game against rank
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

###############
# Attendance  #
############### 
# Chart: Attendance over time
# calcualte mean values by season
avg_per_season = tables.groupby("season").mean().reset_index()

fig, ax = plt.subplots()
# plot average attendance by season
plt.plot(avg_per_season['season'], avg_per_season['Attendance'])

# set x ticks to be more readable
ax.set_xticklabels(['16-17', '17-18', '18-19', '19-20', '20-21', '21-22'])
plt.title('Average Attendance Per Season')
plt.ylabel("Average Match Attendance")
plt.xlabel('Season')

plt.savefig('../vis/tables/average_attendance.png')
plt.close()

# Chart: box and whisker plot for attendance
# divide attendance by 1000 to make chart more readable
tables["Att per thousand"] = tables['Attendance']/1000

# generate boxplot so each box shows range of attendance per season
ax = tables.boxplot(column=['Att per thousand'], by=['season'])

ax.set_title('Average Attendance Across Teams Per Season')
# this line removes the automatic boxplot title
plt.suptitle('')
plt.ylabel("Team's Average Match Attendance (1000)")
plt.xlabel('Season')
plt.savefig('../vis/tables/attendance_boxwhisker.png')
plt.close()

###############
# xG          #
############### 
# Chart: xG over time
# remove first two seasons as they do not have values for xg
avg_per_season_xg = avg_per_season[~avg_per_season['season'].isin(['16-17','17-18'])]

# plot line chart of season by average xg
fig, ax = plt.subplots()
plt.plot(avg_per_season_xg['season'], avg_per_season_xg['xG'])

# set x ticks using unique season values
ax.set_xticklabels(avg_per_season_xg['season'].unique())
plt.title('Average xG Per Season')
plt.ylabel("Average Match xG")
plt.xlabel('Season')

plt.savefig('../vis/tables/average_xg.png')
plt.close()

# Chart: xG per game over time
fig, ax = plt.subplots()

# Plot season by xg divided by number of matches played
plt.plot(avg_per_season_xg['season'], avg_per_season_xg['xG']/avg_per_season_xg['MP'])

# set x ticks using season values
ax.set_xticklabels(avg_per_season_xg['season'].unique())
plt.title('Average xG Per Season')
plt.ylabel("Average Match xG")
plt.xlabel('Season')

plt.savefig('../vis/tables/average_xg_pergame.png')
plt.close()

# Chart: xG per game over time corrected axis
fig, ax = plt.subplots()

# plot same chart as above
plt.plot(avg_per_season_xg['season'], avg_per_season_xg['xG']/avg_per_season_xg['MP'])
ax.set_xticklabels(avg_per_season_xg['season'].unique())
plt.title('Average xG Per Season')
plt.ylabel("Average Match xG")
plt.xlabel('Season')

# change y limits to 0 -> 1.7
plt.ylim((0, 1.7))
plt.savefig('../vis/tables/average_xg_pergame_newaxis.png')
plt.close()

# box and whisker plot for xg
# Chart: get full table data with first two seasons removed
tables_xg = tables[~tables['season'].isin(['16-17', '17-18'])]

# create box and whisker plot for variation in xG per season
ax = tables_xg.boxplot(column=['xG'], by=['season'])

plt.title('Average xG Per Team Per Season')
plt.ylabel("Team's Average Match Attendance")
plt.xlabel('Season')

plt.savefig('../vis/tables/xg_boxwhisker.png')
plt.close()

