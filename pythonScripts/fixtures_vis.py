import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import colorsys
from scipy.interpolate import make_interp_spline

plt.rcParams.update({'font.size': 12})

# output n evenly spaces colour in RGB
def chart_colours(N):
    colours=[]
    HSV = [(i*1.0/N, 1.0, 1.0) for i in range(N)]
    for colour in HSV:
        colours.append(colorsys.hsv_to_rgb(*colour))
    return colours

fx = pd.read_csv("../Data/fixtures/fixtures_clean.csv")

fx.Date = pd.to_datetime(fx.Date)

fx.sort_values(by='Date', inplace = True)

fx_agg = fx[['season', 'Date', 'Attendance']].groupby(['season', 'Date']).max().reset_index()

# Attendance over time
seasons = fx['season'].unique()

# temp['Att new'] = temp['Attendance']/1000

fig, ax = plt.subplots()
for s in seasons:
	temp = fx_agg[(fx_agg.season == s) ]
	temp['Att new'] = temp['Attendance']/1000
	plt.plot(temp["Date"], temp["Att new"], color='b')

# fig.set_size_inches(7.5, 5.5)
plt.title('Attendance Over Time')
plt.xlabel("Date")
plt.ylabel('Match Attendance (1000)')

plt.savefig('../vis/fixtures/attendance_overtime.png')
plt.close()

fx_att = fx_agg[['Date', 'Attendance', 'season']]

attend_q3 = fx_att["Attendance"].quantile(0.75)
attend_q1 = fx_att["Attendance"].quantile(0.25)

h_spread = attend_q3 - attend_q1

upper_outer_fence = 3*h_spread+attend_q3

for index, row in fx_att.iterrows():
	rowval = row['Attendance']
	if pd.isnull(rowval):
		continue
	elif row['Attendance'] > upper_outer_fence:
		fx_att.at[index,'Attendance'] = np.nan


fig, ax = plt.subplots()
for s in seasons:
	temp = fx_att[(fx_att.season == s) ]
	plt.plot(temp["Date"], temp["Attendance"],color='b')

fig.set_size_inches(11.5, 4.5)
plt.title('Attendance Over Time Without Outliers')
plt.xlabel("Date")
plt.ylabel('Match Attendance')

plt.savefig('../vis/fixtures/attendance_overtime_no_outliers.png')
plt.close()

fig, axs = plt.subplots(1, 2)
fig.set_size_inches(11.5, 4.5)

fx["Attendance_2"] = fx["Attendance"]/1000

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

fx_ag = fx[~fx['season'].isin(['16-17','17-18'])].fillna(0)

fx_ag['Match xG'] = fx_ag['xG Home Team'] + fx_ag['xG Away Team']

fx_xg = fx_ag[['season', 'Date', 'Match xG']].groupby(['season', 'Date']).mean().reset_index()
fx_xg['dt'] = fx_xg.groupby('season')['Date'].cumcount()+1

fx_pivot = pd.pivot_table(fx_xg, values='Match xG', index=['dt'],
                     columns=['season'], aggfunc=np.sum).reset_index().drop(['dt'], axis=1)


seasons = fx_xg['season'].unique()

colors = chart_colours(len(seasons))

col_map = {}
i = 0
while i < len(seasons):
	col_map[seasons[i]] = colors[i]
	i += 1


for s,c in zip(seasons, colors):
	test = fx_pivot[[s]]

	test = test[test[s].notna()]
	test_x = test.index.tolist()

	xnew = np.linspace(min(test_x), max(test_x), 10)

	# interpolation
	spl = make_interp_spline(test_x, test[s], k=3)
	smooth = spl(xnew)

	# # plotting
	plt.plot(xnew, smooth, c=c)


plt.title('xG Per Match Day')
plt.xlabel("Match Day")
plt.ylabel('Average xG')
plt.legend(seasons)

# plt.show()
plt.savefig('../vis/fixtures/xg_matchday10.png')
plt.close()




