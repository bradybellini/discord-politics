import asyncio
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pytz import timezone
from matplotlib import style
from pandas import DataFrame, read_csv

# @TODO find a way to see when new polls have been updated. Can do something with checking the last update globals. Store the last one here or check when it has changed.
# Completed the above. Just imported the function in the datafetch file and when new data gets downloaded it makes a new file on the spot. easy...at least for now.
# Why the hell are dates and times so hard to work with in python holy shit

STATES = set()

get_state = pd.read_csv(
    'data/primary_average/president_primary_polls_avg.csv', encoding='ANSI')

for i in get_state.state:
    STATES.add(i)

CANIDATES = ['Amy Klobuchar', 'Bernard Sanders',
             'Pete Buttigieg', 'Elizabeth Warren', 'Michael Bloomberg', 'Joseph R. Biden Jr.']

async def driver():
    pass


def get_est_time():
    fmt = '%m/%d/%Y %H:%M %Z'
    eastern = timezone('US/Eastern')
    est_raw = datetime.now(eastern)
    return est_raw.strftime(fmt)


async def primary_avg(state):
    print(state)
    style.use('ggplot')

    polling_avg_data = pd.read_csv(
        'data/primary_average/president_primary_polls_avg.csv', encoding='ANSI')

    formatter = mdates.DateFormatter('%d %b')

    klobuchar = polling_avg_data[(polling_avg_data.candidate_name == 'Amy Klobuchar') & (
        polling_avg_data.state == f'{state}')]
    sanders = polling_avg_data[(polling_avg_data.candidate_name == 'Bernard Sanders') & (
        polling_avg_data.state == f'{state}')]
    buttigieg = polling_avg_data[(polling_avg_data.candidate_name == 'Pete Buttigieg') & (
        polling_avg_data.state == f'{state}')]
    warren = polling_avg_data[(polling_avg_data.candidate_name == 'Elizabeth Warren') & (
        polling_avg_data.state == f'{state}')]
    bloomberg = polling_avg_data[(polling_avg_data.candidate_name == 'Michael Bloomberg') & (
        polling_avg_data.state == f'{state}')]
    biden = polling_avg_data[(polling_avg_data.candidate_name == 'Joseph R. Biden Jr.') & (
        polling_avg_data.state == f'{state}')]

    fig = plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    ax1.text(0.13, 0, f'Updated: {get_est_time()}',
             fontsize=8, transform=fig.transFigure)
    ax1.text(0.45, 0, f'Data Source: FiveThirtyEight',
             fontsize=8, transform=fig.transFigure)

    sanders_converted_dates = mdates.datestr2num(sanders.modeldate.iloc[:50])
    warren_converted_dates = mdates.datestr2num(warren.modeldate.iloc[:50])
    biden_converted_dates = mdates.datestr2num(biden.modeldate.iloc[:50])
    bloomberg_converted_dates = mdates.datestr2num(bloomberg.modeldate.iloc[:50])
    buttigieg_converted_dates = mdates.datestr2num(
        buttigieg.modeldate.iloc[:50])
    klobuchar_converted_dates = mdates.datestr2num(
        klobuchar.modeldate.iloc[:50])

    ax1.plot(klobuchar_converted_dates,
             klobuchar.pct_estimate.iloc[:50], '#4caf50', linewidth=2)
    ax1.plot(sanders_converted_dates,
             sanders.pct_estimate.iloc[:50], '#2196f3', linewidth=2)
    ax1.plot(buttigieg_converted_dates,
             buttigieg.pct_estimate.iloc[:50], '#e91e63', linewidth=2)
    ax1.plot(warren_converted_dates,
             warren.pct_estimate.iloc[:50], '#ffc107', linewidth=2)
    ax1.plot(bloomberg_converted_dates,
             bloomberg.pct_estimate.iloc[:50], '#cddc39', linewidth=2)
    ax1.plot(biden_converted_dates,
             biden.pct_estimate.iloc[:50], '#9c27b0', linewidth=2)

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1.xaxis_date()
    ax1.xaxis.set_major_formatter(formatter)

    try:
        bloomberg_latest_avg_int = round(bloomberg.pct_estimate.iloc[0], 2)
    except:
        bloomberg_latest_avg_int = 0

    try:
        klobuchar_latest_avg_int = round(klobuchar.pct_estimate.iloc[0], 2)
    except:
        klobuchar_latest_avg_int = 0 

    sanders_latest_avg = round(sanders.pct_estimate.iloc[0], 2)
    warren_latest_avg = round(warren.pct_estimate.iloc[0], 2)
    biden_latest_avg = round(biden.pct_estimate.iloc[0], 2)
    bloomberg_latest_avg = bloomberg_latest_avg_int
    buttigieg_latest_avg = round(buttigieg.pct_estimate.iloc[0], 2)
    klobuchar_latest_avg = klobuchar_latest_avg_int

    # how to order the legend by who is in the lead descending
    # sort by latest average then map the index to the order array dynamically controlling the order.

    first = .85
    second = .78
    third = .71
    fourth = .64
    fifth = .57
    sixth = .50

    legend_order_position = [first, second, third, fourth, fifth, sixth]

    legend_order_candidates = [sanders_latest_avg, warren_latest_avg, biden_latest_avg,
                               bloomberg_latest_avg, buttigieg_latest_avg, klobuchar_latest_avg]

    legend_order_candidates.sort(reverse=True)
    if klobuchar_latest_avg > 0:
        klobuchar_legend = plt.text(x=.93, y=legend_order_position[legend_order_candidates.index(klobuchar_latest_avg)], s=f'{klobuchar_latest_avg_int} - Klobuchar', size='10', bbox=dict(
            boxstyle='round', facecolor='#4caf50'), transform=fig.transFigure)
    if sanders_latest_avg > 0:
        sanders_legend = plt.text(x=.93, y=legend_order_position[legend_order_candidates.index(sanders_latest_avg)], s=f'{round(sanders.pct_estimate.iloc[0],2)} - Sanders', size='10', bbox=dict(
        boxstyle='round', facecolor='#2196f3'), transform=fig.transFigure)
    if buttigieg_latest_avg > 0:
        buttigieg_legend = plt.text(x=.93, y=legend_order_position[legend_order_candidates.index(buttigieg_latest_avg)], s=f'{round(buttigieg.pct_estimate.iloc[0],2)} - Buttigieg', size='10', bbox=dict(
        boxstyle='round', facecolor='#e91e63'), transform=fig.transFigure)
    if bloomberg_latest_avg > 0:
        bloomberg_legend = plt.text(x=.93, y=legend_order_position[legend_order_candidates.index(bloomberg_latest_avg)], s=f'{bloomberg_latest_avg_int} - Bloomberg', size='10', bbox=dict(
        boxstyle='round', facecolor='#cddc39'), transform=fig.transFigure)
    if biden_latest_avg > 0:
        biden_legend = plt.text(x=.93, y=legend_order_position[legend_order_candidates.index(biden_latest_avg)], s=f'{round(biden.pct_estimate.iloc[0],2)} - Biden', size='10', bbox=dict(
        boxstyle='round', facecolor='#9c27b0'), transform=fig.transFigure)
    if warren_latest_avg > 0:
        warren_legend = plt.text(x=.93, y=legend_order_position[legend_order_candidates.index(warren_latest_avg)], s=f'{round(warren.pct_estimate.iloc[0],2)} - Warren', size='10', bbox=dict(
        boxstyle='round', facecolor='#ffc107'), transform=fig.transFigure)

    plt.xlabel('Date')
    plt.ylabel('Average')
    plt.title(f'Democratic Primary {state} Poll Average')

    plt.subplots_adjust(bottom=0.2)
    plt.savefig(
        f'graphs/primary_average_state/{state}/{state}_avg-{round(time.time())}.png', bbox_inches='tight', dpi=150)
    # plt.show()
    plt.close(fig=fig)

if __name__ == "__main__":
    for state in STATES:
        asyncio.run(primary_avg(state))
    # asyncio.run(primary_avg("Wyoming"))

    # may be useful later "Wyoming"

    # plt.annotate('Test', xy=(mdates.datestr2num(sanders.modeldate.iloc[0]),
#                          sanders.pct_estimate.iloc[0]), xycoords='data', xytext=(.9, .6), textcoords='figure fraction',
#                           arrowprops=dict(facecolor='black', arrowstyle='|-|'))
