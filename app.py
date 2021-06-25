import streamlit as st
import time
import numpy as np
# from epintervene.simobjects import simulation
import matplotlib.pyplot as plt

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
print(last_rows)
chart = st.line_chart(last_rows)

adjlist = [[0, 16, 65, 89], [1, 19, 65, 76], [2, 7], [3, 17, 18, 27, 52], [4, 86], [5], [6, 30], [7, 57, 65, 93, 97, 2], [8, 41, 63], [9, 18, 19, 98], [10, 26, 53], [11, 17, 22, 62], [12, 24, 45, 67], [13, 61], [14, 26, 66], [15, 27, 30, 46, 65], [16, 0], [17, 46, 86, 3, 11], [18, 3, 9], [19, 24, 49, 87, 1, 9], [20, 28, 49], [21, 52, 63], [22, 28, 11], [23, 38], [24, 33, 12, 19], [25, 30, 90], [26, 57, 74, 10, 14], [27, 81, 89, 94, 3, 15], [28, 52, 79, 20, 22], [29, 45, 76], [30, 35, 6, 15, 25], [31, 49, 57, 66], [32, 46], [33, 54, 24], [34], [35, 53, 61, 82, 30], [36, 64], [37, 71, 76, 96], [38, 60, 81, 23], [39, 93], [40, 59, 83], [41, 73, 8], [42, 51, 57], [43], [44, 51, 70], [45, 12, 29], [46, 58, 76, 15, 17, 32], [47, 58, 62, 70], [48], [49, 79, 19, 20, 31], [50], [51, 42, 44], [52, 59, 87, 90, 3, 21, 28], [53, 61, 10, 35], [54, 58, 69, 90, 98, 33], [55, 64], [56], [57, 77, 81, 7, 26, 31, 42], [58, 46, 47, 54], [59, 40, 52], [60, 38], [61, 13, 35, 53], [62, 11, 47], [63, 8, 21], [64, 71, 36, 55], [65, 86, 0, 1, 7, 15], [66, 14, 31], [67, 76, 95, 12], [68, 79], [69, 54], [70, 77, 44, 47], [71, 37, 64], [72, 75], [73, 41], [74, 76, 26], [75, 72], [76, 78, 89, 1, 29, 37, 46, 67, 74], [77, 57, 70], [78, 76], [79, 28, 49, 68], [80, 87], [81, 99, 27, 38, 57], [82, 35], [83, 40], [84], [85, 95], [86, 4, 17, 65], [87, 95, 19, 52, 80], [88], [89, 0, 27, 76], [90, 25, 52, 54], [91], [92], [93, 94, 7, 39], [94, 27, 93], [95, 67, 85, 87], [96, 37], [97, 7], [98, 9, 54], [99, 81]]
# sim = simulation.Simulation(N=100, adj_list=adjlist)
# sim.set_uniform_gamma(.05)
# sim.set_uniform_beta(0.5)
# sim.run_sim()
# timeseries_results = sim.tabulate_continuous_time(time_buckets=100, custom_range=True, custom_t_lim=25)
# print(timeseries_results[1])

# fig, ax = plt.subplots()
# ax.spines['bottom'].set_color('red')
# ax.spines['top'].set_color('red')
# ax.xaxis.label.set_color('red')
# ax.tick_params(axis='x', colors='red')
# fig.patch.set_alpha(0)
#
# x = np.arange(0, max(timeseries_results[0]))
# ax.set_ylim(0, max_rand)
# line, = ax.plot(timeseries_results[0], timeseries_results[1])
# the_plot = st.pyplot(fig)
# nanfilled = [np.nan] * len(timeseries_results[0])

# def init():  # give a clean slate to start
#     line.set_ydata([np.nan] * len(x))
#
# def animate(i):  # update the y values (every 1000ms)
#     nanfilled[:i] = timeseries_results[1][:i]
#     line.set_ydata(nanfilled)
#     # line.set_ydata(timeseries_results[1][i])
#     the_plot.pyplot(fig)
#
# init()
# for i in range(2, len(timeseries_results[0])):
#     animate(i)
#     time.sleep(0.01)



for i in range(1,100):
    new_rows = last_rows[-1, :] + np.random.randn(1, 1).cumsum(axis=0)
    print('new rows:')
    print(new_rows)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")