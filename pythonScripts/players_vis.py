import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import colorsys

# set font size for all charts
plt.rcParams.update({'font.size': 12})

pl = pd.read_csv("../Data/playerStats/playerStats_clean.csv")

# output n evenly spaces colour in RGB
def chart_colours(N):
    colours=[]
    HSV = [(i*1.0/N, 1.0, 1.0) for i in range(N)]
    for colour in HSV:
        colours.append(colorsys.hsv_to_rgb(*colour))
    return colours

###############
# Goals       #
############### 
# Chart: Goals scored v minutes, coloured by position
# get unique list of positions
positions = pl['Pos'].unique()

# generate the correct number of colours
colors = chart_colours(len(positions))

# assign a colour to a position
col_map = {}
i = 0
while i < len(positions):
	col_map[positions[i]] = colors[i]
	i += 1

# for each position, create a chart of mins played v goals
fig, ax = plt.subplots()
for s,c in zip(positions, colors):
	temp = pl[(pl.Pos == s) ]
	plt.scatter(temp["Min"], temp["Gls Overall"], c=c)

plt.title('Minutes Played v Goals Scored')
plt.xlabel("Minutes Played")
plt.ylabel('Total Goals Scored in The Season')

plt.legend(positions)

plt.savefig('../vis/playerStats/goal_minutes.png')
plt.close()

# Chart: Goals scored v minutes forwards only
# filter data to only fowards with at least 1 minute and 1 goal
frwrds = pl[(pl['Pos'] == "FW") & (pl['Gls Overall'] > 0) & (pl['Min'] > 0)]

# plot with colour red for consistency with previous chart
plt.scatter(frwrds["Min"], frwrds["Gls Overall"], c='r')

plt.title('Minutes Played v Goals Scored For Forwards')
plt.xlabel("Minutes Played")
plt.ylabel('Total Goals Scored in The Season')

# calculate the top 95th percentile for goals scored
top_5_perc = frwrds["Gls Overall"].quantile(0.95)
# find x and y values for goals >  Q95
x_vals = list(frwrds["Min"][frwrds["Gls Overall"] >= top_5_perc])
y_vals = list(frwrds["Gls Overall"][frwrds["Gls Overall"] >= top_5_perc])
# find player list for goals > Q95
players = list(frwrds["Player"][frwrds["Gls Overall"] >= top_5_perc])

# add annotation to chart for each of these players
for i, txt in enumerate(players):
    plt.annotate(txt, (x_vals[i], y_vals[i]), ha='right')

plt.savefig('../vis/playerStats/goal_minutes_forwards.png')
plt.close()

# Chart: overall top scorers
# group by players and find total number of assists and goals per player
scorers = pl[['Player', 'Gls Overall', 'Ast Overall']].groupby('Player').sum().reset_index()

# Calculate total goals and assists and then sort by this value
scorers['Gls and Ast'] = scorers['Gls Overall'] + scorers['Ast Overall']
scorers.sort_values(by=['Gls and Ast'], inplace=True, ascending=False)

# set players as index and drop goals and assists, take top 10 rows
top_scorers = scorers.set_index('Player').drop(['Gls and Ast'], axis=1).head(10)

# rename columns 
top_scorers.rename(columns = {'Gls Overall':'Goals', 'Ast Overall':'Assists'}, inplace = True)

# plot goals and assists on a horizontal barchart
ax = top_scorers.plot.barh(stacked=True, title="Top 10 Scorers In the WSL", color=['red','black'])
ax.set_xlabel('Goals and Assists')
# rotate and resize y ticks to make easier to read
plt.yticks(rotation=45, fontsize=6.5)
# invert y-axis so best players are on the top
plt.gca().invert_yaxis()

plt.savefig('../vis/playerStats/top_scorers.png')
plt.close()

# Chart: Top scorers per season
# Aggregate on players and calculate total number of goals, assists and the distinct number of seasons played
scorers = pl[['Player', 'season', 'Gls Overall', 'Ast Overall']].groupby('Player') \
						.agg({"Gls Overall": np.sum, "Ast Overall": np.sum, "season": pd.Series.nunique}).reset_index()

# calculate goals and assists per season by dividing by number of seasons played column
scorers['Goals per season'] = scorers['Gls Overall']/scorers['season']
scorers['Assists per season'] = scorers['Ast Overall']/scorers['season']

# Calculate new total goals and assists and sort by this column
scorers['Gls and Ast'] = scorers['Goals per season'] + scorers['Assists per season']
scorers.sort_values(by=['Gls and Ast'], inplace=True, ascending=False)

# set players as index, remove unnecessary columns and take top 10 values
top_scorers = scorers.set_index('Player').drop(['Gls and Ast', 'Gls Overall', 'Ast Overall', 'season'], axis=1).head(10)

# plot as above
ax = top_scorers.plot.barh(stacked=True, title="Top 10 Scorers In the WSL Per Season", color=['red','black'])
ax.set_xlabel('Goals and Assists')
plt.yticks(rotation=45, fontsize=6.5)
plt.gca().invert_yaxis()

plt.savefig('../vis/playerStats/top_scorers_perseason.png')
plt.close()

####################
# Nationalities    #
#################### 
# Chart: histogram of nationalities
# get unique list of players and nationalities
ply_nat = pl[['Player','Nation']].drop_duplicates().dropna()

# remove rows where nationality is unknown
ply_nat = ply_nat[ply_nat['Nation'] != 'unknown']

# found count of each nationality
nat = ply_nat.groupby('Nation').count().reset_index()

# plot on bar chart with values descending
nat.sort_values('Player', ascending=False).plot.bar(x='Nation', legend=None)

plt.title('Number of Players Per Country')
plt.ylabel('Number of Players')

# remove x label
plt.xlabel(None)
plt.xticks(fontsize=9)

plt.savefig('../vis/playerStats/nation_bar.png')
plt.close()

# Chart: English v non-English pie chart
# itterate through rows and rename nationality as either English or not English
for index, row in nat.iterrows():
	if row['Nation'] == "ENG":
		nat.at[index,'Nation'] = "English"
	else:
		nat.at[index,'Nation'] = "Non-English"

# group by new nations and find sum of each
nat_pie = nat.groupby('Nation').sum().reset_index()

# create pie chart, with no legend and % of each slice on chart
nat_pie.set_index('Nation').plot.pie(y='Player', legend=None, colors=['lightblue', 'lightcoral'], autopct='%1.1f%%')

plt.savefig('../vis/playerStats/nation_pie.png')
plt.close()

# Chart: Number of foreign players v rank
# get unique list of squad, player and nation
team_nat = pl[['Squad','Player','Nation']].drop_duplicates().dropna()

# repeat renaming of columns, not with squad column included
for index, row in team_nat.iterrows():
	if row['Nation'] == "ENG":
		team_nat.at[index,'Nation'] = "English"
	else:
		team_nat.at[index,'Nation'] = "Non-English"

# group by squad and find total number of non-english playeres, then drop nation column
team_nat = team_nat[team_nat['Nation'] == "Non-English"].groupby('Squad').count().reset_index().drop(['Nation'], axis=1)

# rename column
team_nat.rename(columns={"Player": "Number Non-English Players"}, inplace=True)

# read in tables data
tables = pd.read_csv("../Data/tables/tables_clean.csv")

# find average rank per squad
sqd_rnk = tables[['Squad', 'Rk']].groupby('Squad').mean().reset_index()

# join squad data on team data
sqd_rnk_nat = sqd_rnk.join(team_nat.set_index('Squad'), on='Squad')

# plot the results
plt.scatter(sqd_rnk_nat["Rk"], sqd_rnk_nat["Number Non-English Players"])

plt.title('Average finishing position v number of non-English players')
plt.xlabel("Average Finishing Position")
plt.ylabel('Number of Non-English Players')

plt.savefig('../vis/playerStats/nation_rank.png')
plt.close()

# Chart: xG v Goals
# pull all data for xg and goals where neither value is null 
gls_xg = pl[['Gls Overall', 'xG Overall']].dropna()

# fit a line to the data
fit = np.polyfit(gls_xg['xG Overall'], gls_xg['Gls Overall'], 1)
m = fit[0]
intercept = fit[1]

# calculate y values for linear fit
fit_eq = m*gls_xg['xG Overall'] + intercept

# plot scatter points and line on the same chart
fig = plt.figure()
ax = fig.subplots()
ax.plot(gls_xg['xG Overall'], fit_eq, label="Linear Fit", color='r')
ax.scatter(gls_xg['xG Overall'], gls_xg['Gls Overall'], color='b', label="Data Points")
ax.legend()

plt.title('Goals Scored v xG Per Player Per Season')
plt.xlabel("xG")
plt.ylabel('Goals Scored')

plt.savefig('../vis/playerStats/goals_v_xg_linear_fit.png')
plt.close()

# Chart: histogram of residual values
yfit = np.polyval(fit, gls_xg['xG Overall'])

# plot difference between actual and expected values
plt.hist(gls_xg['Gls Overall']-yfit)

# calculate reduced chi squared values
chi_squared = np.sum(((yfit - gls_xg['Gls Overall']) ** 2)/yfit)/(len(yfit) - 1)

# add reduced chi square value to chart
label = "Reduced Chi Squared = " + str(round(chi_squared,4))
plt.figtext(.6, .8, label)

plt.title('Residuals for Linear Fit')
plt.xlabel("Residual value")
plt.ylabel('Count')

plt.savefig('../vis/playerStats/goals_v_xg_residuals.png')
plt.close()


