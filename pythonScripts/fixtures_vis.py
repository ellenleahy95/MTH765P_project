import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import colorsys

fx = pd.read_csv("../Data/fixtures/fixtures_clean.csv")

fx.Date = pd.to_datetime(fx.Date)

fx.sort_values(by='Date', inplace = True)

# Attendance over time
seasons = fx['season'].unique()

fig, ax = plt.subplots()
for s in seasons:
	temp = fx[(fx.season == s) ]
	plt.plot(temp["Date"], temp["Attendance"],color='b')

fig.set_size_inches(11.5, 4.5)
plt.title('Attendance Over Time')
plt.xlabel("Date")
plt.ylabel('Match Attendance')

plt.savefig('../vis/fixtures/attendance_overtime.png')
plt.close()

fx_att = fx[['Date', 'Attendance', 'season']]

attend_q3 = fx_att["Attendance"].quantile(0.75)
attend_q1 = fx_att["Attendance"].quantile(0.25)

h_spread = attend_q3 - attend_q1

upper_outer_fence = 3*h_spread+attend_q3

while fx_att.Attendance.max() > upper_outer_fence:
	for index, row in fx_att.iterrows():
		rowval = row['Attendance']
		if pd.isnull(rowval):
			continue
		elif row['Attendance'] > upper_outer_fence:
			x = fx_att.at[index-1, 'Attendance']
			lowerval = x if not np.isnan(x) else 0
			y = fx_att.at[index+1, 'Attendance']
			upperval = y if not np.isnan(y) else 0
			fx_att.at[index,'Attendance'] = (lowerval+upperval)/2

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



