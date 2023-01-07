import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import colorsys
# from pathlib import Path
# import re

pl = pd.read_csv("../Data/playerStats/playerStats_clean.csv")

# output n evenly spaces colour in RGB
def chart_colours(N):
    colours=[]
    HSV = [(i*1.0/N, 1.0, 1.0) for i in range(N)]
    for colour in HSV:
        colours.append(colorsys.hsv_to_rgb(*colour))
    return colours

# Goals scored v minutes, coloured by position
positions = pl['Pos'].unique()

colors = chart_colours(len(positions))

col_map = {}
i = 0
while i < len(positions):
	col_map[positions[i]] = colors[i]
	i += 1

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

frwrds = pl[(pl['Pos'] == "FW") & (pl['Gls Overall'] > 0) & (pl['Min'] > 0)]

plt.scatter(frwrds["Min"], frwrds["Gls Overall"])

plt.title('Minutes Played v Goals Scored For Forwards')
plt.xlabel("Minutes Played")
plt.ylabel('Total Goals Scored in The Season')

# annotate players who are in the top 5% 
top_5_perc = frwrds["Gls Overall"].quantile(0.95)
x_vals = list(frwrds["Min"][frwrds["Gls Overall"] >= top_5_perc])
y_vals = list(frwrds["Gls Overall"][frwrds["Gls Overall"] >= top_5_perc])
players = list(frwrds["Player"][frwrds["Gls Overall"] >= top_5_perc])

for i, txt in enumerate(players):
    plt.annotate(txt, (x_vals[i], y_vals[i]))

plt.savefig('../vis/playerStats/goal_minutes_forwards.png')
plt.close()

# Overall top scorers
scorers = pl[['Player', 'Gls Overall', 'Ast Overall']].groupby('Player').sum().reset_index()

scorers['Gls and Ast'] = scorers['Gls Overall'] + scorers['Ast Overall']

scorers.sort_values(by=['Gls and Ast'], inplace=True, ascending=False)
top_scorers = scorers.set_index('Player').drop(['Gls and Ast'], axis=1).head(10)
top_scorers.rename(columns = {'Gls Overall':'Goals', 'Ast Overall':'Assists'}, inplace = True)

ax = top_scorers.plot.barh(stacked=True, title="Top 10 Scorers In the WSL", color=['red','black'])
ax.set_xlabel('Goals and Assists')
plt.yticks(rotation=45, fontsize=6.5)
plt.gca().invert_yaxis()

plt.savefig('../vis/playerStats/top_scorers.png')
plt.close()

# histogram of nationalities
ply_nat = pl[['Player','Nation']].drop_duplicates().dropna()

nat = ply_nat.groupby('Nation').count().reset_index()

nat.sort_values('Player', ascending=False).plot.bar(x='Nation', legend=None)


plt.title('Number of Players Per Country')
plt.ylabel('Number of Players')

plt.savefig('../vis/playerStats/nation_bar.png')
plt.close()

for index, row in nat.iterrows():
	if row['Nation'] == "eng ENG":
		nat.at[index,'Nation'] = "English"
	else:
		nat.at[index,'Nation'] = "Non-English"

nat_pie = nat.groupby('Nation').sum().reset_index()

nat_pie.set_index('Nation').plot.pie(y='Player', legend=None)

plt.savefig('../vis/playerStats/nation_pie.png')
plt.close()

# Do teams with more non-English players tend to finish higher
team_nat = pl[['Squad','Player','Nation']].drop_duplicates().dropna()
for index, row in team_nat.iterrows():
	if row['Nation'] == "eng ENG":
		team_nat.at[index,'Nation'] = "English"
	else:
		team_nat.at[index,'Nation'] = "Non-English"

team_nat = team_nat[team_nat['Nation'] == "Non-English"].groupby('Squad').count().reset_index().drop(['Nation'], axis=1)
team_nat.rename(columns={"Player": "Number Non-English Players"}, inplace=True)

tables = pd.read_csv("../Data/tables/tables_clean.csv")

sqd_rnk = tables[['Squad', 'Rk']].groupby('Squad').mean().reset_index()

sqd_rnk_nat = sqd_rnk.join(team_nat.set_index('Squad'), on='Squad')

plt.scatter(sqd_rnk_nat["Rk"], sqd_rnk_nat["Number Non-English Players"])

plt.title('Average finishing position v number of non-English players')
plt.xlabel("Average Finishing Position")
plt.ylabel('Number of Non-English Players')

plt.savefig('../vis/playerStats/nation_rank.png')
plt.close()

# xG v Goals
gls_xg = pl[['Gls Overall', 'xG Overall']].dropna()

fit = np.polyfit(gls_xg['xG Overall'], gls_xg['Gls Overall'], 1)
m = fit[0]
intercept = fit[1]
fit_eq = m*gls_xg['xG Overall'] + intercept

fig = plt.figure()
ax = fig.subplots()
ax.plot(gls_xg['xG Overall'], fit_eq, label="Linear Fit", color='r')
ax.scatter(gls_xg['xG Overall'], gls_xg['Gls Overall'], color='b', label="Data Points")
ax.legend()

plt.title('Goals Scored v xG Per Player Per Season')
plt.xlabel("xG")
plt.ylabel('Goals Scored')

plt.savefig('../vis/playerStats/linear_fit.png')
plt.close()

yfit = np.polyval(fit, gls_xg['xG Overall'])

fig, ax = plt.subplots(1,2)
ax[0].hist(gls_xg['Gls Overall']-yfit)

fit2 = np.polyfit(gls_xg['xG Overall'], gls_xg['Gls Overall'], 2)
yfit2 = np.polyval(fit2, gls_xg['xG Overall'])
ax[1].hist(gls_xg['Gls Overall']-yfit2)

ax[0].set_title('Residuals for Linear Fit')
ax[1].set_title('Residuals for Quadratic Fit')
plt.show()


