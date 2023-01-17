import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import colorsys
from scipy.interpolate import make_interp_spline

# Set font size on charts to 12
plt.rcParams.update({'font.size': 12})

# output n evenly spaces colour in RGB
def chart_colours(N):
    colours=[]
    HSV = [(i*1.0/N, 1.0, 1.0) for i in range(N)]
    for colour in HSV:
        colours.append(colorsys.hsv_to_rgb(*colour))
    return colours

# read in clean data
fx = pd.read_csv("../Data/fixtures/fixtures_clean.csv")

###############
# Attendance  #
############### 
# Chart: Attendance over time
# update date column to be the correct date format
fx.Date = pd.to_datetime(fx.Date)

# sort by date
fx.sort_values(by='Date', inplace = True)

# take maximum value of attendance per season, per date
fx_agg = fx[['season', 'Date', 'Attendance']].groupby(['season', 'Date']).max().reset_index()

# find unique value of seasons
seasons = fx['season'].unique()

fig, ax = plt.subplots()

# plotting line chart for each season, this creates a gap between each season to reflect the periods when there are no games
for s in seasons:
	temp = fx_agg[(fx_agg.season == s) ]
	temp['Att new'] = temp['Attendance']/1000
	plt.plot(temp["Date"], temp["Att new"], color='b')

plt.title('Attendance Over Time')
plt.xlabel("Date")
plt.ylabel('Match Attendance (1000)')

plt.savefig('../vis/fixtures/attendance_overtime.png')
plt.close()

# Chart: Attendance over time without outliers
fx_att = fx_agg[['Date', 'Attendance', 'season']]

# caluclate third and first quartile using Pandas
attend_q3 = fx_att["Attendance"].quantile(0.75)
attend_q1 = fx_att["Attendance"].quantile(0.25)

# use Q1 and Q3 to calculate h_spread
h_spread = attend_q3 - attend_q1

# calculate upper outer fence, which we will use as limit for ourliars
upper_outer_fence = 3*h_spread+attend_q3

# iterate through rows, and if they are greater then upper outer fence, replace with nan
for index, row in fx_att.iterrows():
	rowval = row['Attendance']
	if pd.isnull(rowval):
		continue
	elif rowval > upper_outer_fence:
		fx_att.at[index,'Attendance'] = np.nan

fig, ax = plt.subplots()

# plot new data
for s in seasons:
	temp = fx_att[(fx_att.season == s) ]
	plt.plot(temp["Date"], temp["Attendance"],color='b')

# set size to make chart easier to read
fig.set_size_inches(11.5, 4.5)
plt.title('Attendance Over Time Without Outliers')
plt.xlabel("Date")
plt.ylabel('Match Attendance')

plt.savefig('../vis/fixtures/attendance_overtime_no_outliers.png')
plt.close()

# Chart: Home and away goals v attendance
fig, axs = plt.subplots(1, 2)
fig.set_size_inches(11.5, 4.5)

# to make axis clearer, divide attendance values by 1000
fx["Attendance_2"] = fx["Attendance"]/1000

# plot each scatter plot and set labels and titles
axs[0].scatter(fx["Attendance_2"], fx["Home Goals"])
axs[1].scatter(fx["Attendance_2"], fx["Away Goals"])

axs[0].title.set_text("Goals Scored by the Home Team v Attendance")
axs[1].title.set_text("Goals Scored by the Away Team v Attendance")

axs[0].set_xlabel("Attendance (1000)")
axs[0].set_ylabel('Home Goals Scored')

axs[1].set_xlabel("Attendance (1000)")
axs[1].set_ylabel('Away Goals Scored')

plt.savefig('../vis/fixtures/attendance_v_goals.png')
plt.close()

###############
# xG          #
###############
# remove the first two seasons, with no xg data and fill all nulls with 0 
fx_xg = fx[~fx['season'].isin(['16-17','17-18'])].fillna(0)

# Calculate total match xg
fx_xg['Match xG'] = fx_xg['xG Home Team'] + fx_xg['xG Away Team']

# group by season and date and find the average xg per date
fx_xg = fx_xg[['season', 'Date', 'Match xG']].groupby(['season', 'Date']).mean().reset_index()
# use cumcount function to rank each row, so we have a number of each date per season to create an overlapping chart
fx_xg['dt'] = fx_xg.groupby('season')['Date'].cumcount()+1

# pivot table so we now have one column per season
fx_pivot = pd.pivot_table(fx_xg, values='Match xG', index=['dt'],
                     columns=['season'], aggfunc=np.sum).reset_index().drop(['dt'], axis=1)

# get seasons and assign a colour for each season
seasons = fx_xg['season'].unique()
colors = chart_colours(len(seasons))

col_map = {}
i = 0
while i < len(seasons):
	col_map[seasons[i]] = colors[i]
	i += 1

# for each season and colour, plot an interpolated line
for s,c in zip(seasons, colors):
	# get season
	test = fx_pivot[[s]]
	# remove any null values
	test = test[test[s].notna()]
	# create x values wusing index
	test_x = test.index.tolist()

	# generate new x valuse with fewer spaces
	xnew = np.linspace(min(test_x), max(test_x), 20)

	# using scipy, generate a new set of y values, interpolating at 3 DoF
	spl = make_interp_spline(test_x, test[s], k=3)
	smooth = spl(xnew)

	# plot the results
	plt.plot(xnew, smooth, c=c)


plt.title('xG Per Match Day')
plt.xlabel("Match Day")
plt.ylabel('Average xG')

# set legend using the season array
plt.legend(seasons)

plt.savefig('../vis/fixtures/xg_matchday20.png')
plt.close()




