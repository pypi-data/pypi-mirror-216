"""
Modeling the (only Gross so far, but eventually Net as well) income of Bronsoneering LLC.  Script based on posted Ad
rates from admob, and estimates / projections from Jake Bronson.  Future update to add error bars to the output plots,
as well as integrate a schedule of sorts (add milestones to plots as well).
"""
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy import integrate
matplotlib.use('Qt5Agg')


# optimistic, normal, and pessimistic inputs (mulipliers for now, but later make be different inputs, graph all)
ism_dict = {
    # 'optimistic': 1.1,
    'normal': 1.0,
    # 'pessimistic': 0.9,
}

# inputs for Ad assumptions (admob rates)
banner_ecpm = 0.85          # USD per mille (per 1000 people who see the ad)
banner_cpc = 0.12           # USD per click
interstitial_ecpm = 7.50    # USD per mille
rewarded_vid_ecpm = 13.00   # USD per mille
native_ecpm = 1.00          # USD per mille
native_cpc = 0.15           # USD per click

# inputs for modeling the current number of users
init_daily_users = 0        # initial number of users of each app per day
max_daily_users = 1.00     # limit the maximum daily users of a single app (for modeling purposes only)
daily_new_users = 1.0       # overall new users per day (negative is possible / valid)

# inputs for ads, how hard I want to work
num_int_ads_per_app = 2     # how many interstitial ads per app?
num_rew_ads_per_app = 1     # how many rewarded video ads per app?
num_years = 1               # analyze the upcoming how many years
num_apps_per_year = 0.25       # number of apps released per year
both_services = True        # is App on both Google Play and Apple Store?

# constants
DAYS_PER_YEAR = 365     # ad revenue is coming in how many days per year?
AND_MULTIPLIER = 1.0    # multiplier applied to android income
IOS_MULTIPLIER = 1.4     # multiplier applier to ios income (based on a source I found)

# ====================================
# ---- CALCULATIONS AND MODELING -----
# ====================================

# create time array, number of apps array, and daily users array
tm_array = np.linspace(start=0, stop=num_years, num=DAYS_PER_YEAR)   # time array discretized into 365 points/year
num_apps_arr = tm_array * num_apps_per_year     # array, number of applications published (cumulative)
end_daily_users = init_daily_users + daily_new_users * DAYS_PER_YEAR * num_years  # float, number of users after X years
daily_users = np.linspace(start=init_daily_users, stop=end_daily_users, num=len(tm_array))  # array, users per app

# make daily users equal to max_daily_users wherever it exceeds that value
daily_users = np.array([max_daily_users if num_users >= max_daily_users else num_users for num_users in daily_users])

# calculate income rates
num_ads_per_app = num_int_ads_per_app + num_rew_ads_per_app     # how many ads are in each application?

# avg_usd_permille is a weighted average, as a float value, of USD per 1000 "views" of all ads within the app
# assumption used in this equation is that each user will use the app once per day and see all the ads
avg_usd_permille = (num_int_ads_per_app * interstitial_ecpm + num_rew_ads_per_app * rewarded_vid_ecpm) / num_ads_per_app
daily_usd_per_app = (1 + num_ads_per_app) * avg_usd_permille * daily_users  # array, USD per app per day

# android and ios have different download statistics (ios is downloaded 40% more frequently per some online source)
daily_and_income = AND_MULTIPLIER * daily_usd_per_app   # array, should just be a copy of daily_usd_per_app
daily_ios_income = IOS_MULTIPLIER * daily_usd_per_app   # array, should scale daily_usd_per_app by ~1.4
daily_income = daily_and_income + daily_ios_income if both_services else daily_and_income  # array, daily income in USD
yearly_income = daily_income * DAYS_PER_YEAR               # array, yearly income in USD

# multiply by number of apps
daily_income *= num_apps_arr    # array, USD per day
yearly_income *= num_apps_arr   # array, USD per year

# integrate to get the total as a function of time
total_usd_arr = integrate.cumtrapz(daily_income, x=tm_array, initial=0)  # running integral using cumulative trapezoids
total_usd = sum(total_usd_arr) * DAYS_PER_YEAR * num_years               # add up USD made each day

# plot and show results
ydatas = {
    '# Apps\nPublished': num_apps_arr,
    'Daily Users\nper App': daily_users,
    'USD\nper Day': daily_income,
    'USD\nper Year': yearly_income,
    'Total\nUSD\n1<deg<2': total_usd_arr,
}

# create figure and axes instance(s)
fig, axes = plt.subplots(nrows=len(ydatas), ncols=1, figsize=(12, 10))
axes[0].set_title('Bronsoneering Projections\nModeling with Both App Services: {}'.format(both_services))
axes[-1].set_xlabel('Time (years)')

# cycle axes in for loop
for ax, ylbl in zip(axes, ydatas):
    ax.grid(True)
    # ax.sharex(axes[0], axes[1], axes[2], axes[3], axes[4])
    ax.set_ylabel(ylbl)
    for key, val in ism_dict.items():
        ax.plot(tm_array, val * ydatas[ylbl], label=key)

# turn on the legend in the last plot
axes[-1].legend(loc='best')     # later I plan to shade in the area under this curve to indicate it is an integral

# print results (format the numbers to have commas and dollar signs)
first_day_txt = float('{:.2f}'.format(daily_income[0]))                    # first value in this array
last_day_txt = float('{:.2f}'.format(daily_income[-1]))                    # last value in this array
first_year_txt = float('{:.2f}'.format(sum(daily_income[tm_array <= 1])))  # adds up daily_income
last_year_txt = float('{:.2f}'.format(sum(daily_income[tm_array <= num_years])))  # adds up daily income over last year
total_txt = float('{:.2f}'.format(total_usd))                              # total accumulated
print('----------------------------------------------------------')
print('===================== SCRIPT OUTPUTS =====================')
print('----------------------------------------------------------')
print('First Day Income (Gross):                   ${:,}'.format(first_day_txt))
print('Last Day Income (Gross):                    ${:,}'.format(last_day_txt))
print('First Year Salary Equivalent (Gross):       ${:,}'.format(first_year_txt))
print('Last Year Salary Equivalent (Gross):        ${:,}'.format(last_year_txt))
print('Total Accumulated Over {} Years (Gross):    ${:,}'.format(num_years, total_txt))
