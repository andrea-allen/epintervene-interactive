import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import sample_networks
import simulations

st.title("Epidemic SIR Simulations")

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

num_sims = st.sidebar.radio("Number of simulations", ("1", "10", "100", "500", "1000"))
num_nodes = st.sidebar.number_input("Number of nodes", min_value=10, max_value=5000, value=100)
beta_value = st.sidebar.slider('Select a beta, or infection rate, value',0.0, 1.0, value=0.5)
gamma_value = st.sidebar.slider('Select a gamma, or recovery rate, value',0.01, 1.0, value=0.1)
st.sidebar.text("Below, select either a random network type \nor upload your own adjacency list. If \nyou select 'None of these' and don't upload"
                "\nanything, the simulation will use a default network.")
network_type = st.sidebar.selectbox('Random network', ('Erdos-Renyi', 'Balanced Tree', 'Small world', 'None of these'))
st.sidebar.text("Leave intervention type as None \nfor a regular disease simulation. \nIf desired, select Random or \n"
                "Targeted vaccination to see\n the effects of these \npolicies on disease spread.")
intervention_type = st.sidebar.selectbox('Intervention', ('None', 'Random vaccination', 'Targeted vaccination', 'All'))
intervention_gens = st.sidebar.multiselect('Intervention generations',[2, 3, 4, 5, 6, 7, 8])
intervention_increment = st.sidebar.slider('Select % population\nincrement for vaccination',0.0, 1.0, value=0.1)
st.sidebar.text("You can upload your own adjacency list below.\n"
                "Make sure it is a .txt file, in the form\n"
                "0,1,2\n1,0\n2,0\n and is symmetric.")
uploaded_file = st.sidebar.file_uploader("Upload an adjacency list text file")
if uploaded_file is not None:
    list_of_lists = []
    raw_text = str(uploaded_file.read(), "utf-8")
    raw_text_rows = raw_text.strip().split("\n")
    for row in raw_text_rows:
        split_row = row.strip("\r").split(",")
        list_of_lists.append(list(map(int,split_row)))

elif network_type == 'Erdos-Renyi':
    progress_bar.progress(1/int(num_sims))
    status_text.text("Creating network")
    list_of_lists = sample_networks.erdos_renyi(n=num_nodes, p=2/num_nodes)

elif network_type == 'Small world':
    progress_bar.progress(1/int(num_sims))
    status_text.text("Creating network")
    list_of_lists = sample_networks.small_world(n=num_nodes, k=2, p=2/num_nodes)

elif network_type == "Balanced Tree":
    progress_bar.progress(1/int(num_sims))
    status_text.text("Creating network")
    list_of_lists = sample_networks.balanced_tree()

if uploaded_file is None and network_type == 'None of these':
    status_text.text("Using default network")
    list_of_lists = [[0, 16, 65, 89], [1, 19, 65, 76], [2, 7], [3, 17, 18, 27, 52], [4, 86], [5], [6, 30], [7, 57, 65, 93, 97, 2], [8, 41, 63], [9, 18, 19, 98], [10, 26, 53], [11, 17, 22, 62], [12, 24, 45, 67], [13, 61], [14, 26, 66], [15, 27, 30, 46, 65], [16, 0], [17, 46, 86, 3, 11], [18, 3, 9], [19, 24, 49, 87, 1, 9], [20, 28, 49], [21, 52, 63], [22, 28, 11], [23, 38], [24, 33, 12, 19], [25, 30, 90], [26, 57, 74, 10, 14], [27, 81, 89, 94, 3, 15], [28, 52, 79, 20, 22], [29, 45, 76], [30, 35, 6, 15, 25], [31, 49, 57, 66], [32, 46], [33, 54, 24], [34], [35, 53, 61, 82, 30], [36, 64], [37, 71, 76, 96], [38, 60, 81, 23], [39, 93], [40, 59, 83], [41, 73, 8], [42, 51, 57], [43], [44, 51, 70], [45, 12, 29], [46, 58, 76, 15, 17, 32], [47, 58, 62, 70], [48], [49, 79, 19, 20, 31], [50], [51, 42, 44], [52, 59, 87, 90, 3, 21, 28], [53, 61, 10, 35], [54, 58, 69, 90, 98, 33], [55, 64], [56], [57, 77, 81, 7, 26, 31, 42], [58, 46, 47, 54], [59, 40, 52], [60, 38], [61, 13, 35, 53], [62, 11, 47], [63, 8, 21], [64, 71, 36, 55], [65, 86, 0, 1, 7, 15], [66, 14, 31], [67, 76, 95, 12], [68, 79], [69, 54], [70, 77, 44, 47], [71, 37, 64], [72, 75], [73, 41], [74, 76, 26], [75, 72], [76, 78, 89, 1, 29, 37, 46, 67, 74], [77, 57, 70], [78, 76], [79, 28, 49, 68], [80, 87], [81, 99, 27, 38, 57], [82, 35], [83, 40], [84], [85, 95], [86, 4, 17, 65], [87, 95, 19, 52, 80], [88], [89, 0, 27, 76], [90, 25, 52, 54], [91], [92], [93, 94, 7, 39], [94, 27, 93], [95, 67, 85, 87], [96, 37], [97, 7], [98, 9, 54], [99, 81]]

hex_list = ['#0173b2', '#56b4e9',  '#029e73', '#ece133', '#de8f05', '#d55e00', '#cc78bc', '#fbafe4', '#ca9161',  '#949494',  ]

## Simulations for the standard simulation
simulator = simulations.Simulator("standard")
simulator.simulate(num_sims=num_sims, gamma=gamma_value, beta=beta_value, adj_list=list_of_lists,
                   progress_bar=progress_bar, status_text=status_text)

custom_time_limit = simulator.max_time+20

########
# Second set of simulations to show interventions
def run_rand():
    rand_intv_sim = simulations.Simulator("random_rollout", rollout_gens=sorted(intervention_gens),
                                     rollout_proportns=list([intervention_increment for i in intervention_gens]))
    rand_intv_sim.simulate(num_sims=num_sims, gamma=gamma_value, beta=beta_value, adj_list=list_of_lists,
                      progress_bar=progress_bar, status_text=status_text)
    return rand_intv_sim

def run_targ():
    targ_intv_sim = simulations.Simulator("targeted_rollout", rollout_gens=sorted(intervention_gens),
                                          rollout_proportns=list([intervention_increment for i in intervention_gens]))
    targ_intv_sim.simulate(num_sims=num_sims, gamma=gamma_value, beta=beta_value, adj_list=list_of_lists,
                           progress_bar=progress_bar, status_text=status_text)
    return targ_intv_sim


if intervention_type == "Random vaccination":
    rand_intv_sim = run_rand()

if intervention_type == "Targeted vaccination":
    targ_intv_sim = run_targ()

if intervention_type == "All":
    rand_intv_sim = run_rand()
    targ_intv_sim = run_targ()

#######

# fig, ax = plt.subplots(figsize=(16,8))
fig, ax = plt.subplots()
tc = st.get_option('theme.textColor')
ax.spines['bottom'].set_color(tc)
ax.spines['bottom'].set_visible(True)
ax.spines['top'].set_color(tc)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_color(tc)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(tc)
ax.spines['left'].set_visible(True)
ax.xaxis.label.set_color(tc)
ax.yaxis.label.set_color(tc)
ax.set_xlabel('Time')
ax.set_ylabel('Nodes')
ax.tick_params(axis='x', colors=tc)
ax.tick_params(axis='y', colors=tc)
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)
#
x = np.arange(0, max(simulator.timeseries_results_cum))


nanfilled = [np.nan] * len(simulator.timeseries_results_cum)
nanfilled_rec = [np.nan] * len(simulator.timeseries_results_cum)
line, = ax.plot(simulator.timeseries_results_cum, nanfilled, color=hex_list[3], label='infected')
if intervention_type == "Random vaccination":
    nanfilled_rand_intv = [np.nan] * len(rand_intv_sim.timeseries_results_cum)
    line_rand_intv, = ax.plot(rand_intv_sim.timeseries_results_cum, nanfilled_rand_intv, color=hex_list[4],
                              label='random vaccination')
if intervention_type == "Targeted vaccination":
    nanfilled_targ_intv = [np.nan] * len(targ_intv_sim.timeseries_results_cum)
    line_targ_intv, = ax.plot(targ_intv_sim.timeseries_results_cum, nanfilled_targ_intv, color=hex_list[5],
                              label='targeted vaccination')
if intervention_type == "All":
    nanfilled_rand_intv = [np.nan] * len(rand_intv_sim.timeseries_results_cum)
    line_rand_intv, = ax.plot(rand_intv_sim.timeseries_results_cum, nanfilled_rand_intv, color=hex_list[4],
                              label='random vaccination')
    nanfilled_targ_intv = [np.nan] * len(targ_intv_sim.timeseries_results_cum)
    line_targ_intv, = ax.plot(targ_intv_sim.timeseries_results_cum, nanfilled_targ_intv, color=hex_list[5],
                              label='targeted vaccination')
line_rec, = ax.plot(simulator.timeseries_results_cum, nanfilled_rec, color=hex_list[2], label='recovered')
ax.set_ylim(0, max(simulator.infected_results)+10)
ax.set_xlim(0, custom_time_limit)
the_plot = st.pyplot(fig)


def init():  # give a clean slate to start
    line.set_ydata([np.nan] * len(x))
    line_rec.set_ydata([np.nan] * len(x))
    if intervention_type == "Random vaccination":
        line_rand_intv.set_ydata([np.nan] * len(x))
    if intervention_type == "Targeted vaccination":
        line_targ_intv.set_ydata([np.nan] * len(x))
    if intervention_type == "All":
        line_rand_intv.set_ydata([np.nan] * len(x))
        line_targ_intv.set_ydata([np.nan] * len(x))
    lgnd = ax.legend(loc='upper left', frameon=False)
    for lines, text in zip(lgnd.get_lines(), lgnd.get_texts()):
        text.set_color(lines.get_color())

def animate(i):
    nanfilled[:i] = simulator.infected_results[:i]
    nanfilled_rec[:i] = simulator.recovered_results[:i]
    line.set_ydata(nanfilled)
    line_rec.set_ydata(nanfilled_rec)
    if intervention_type == "Random vaccination":
        nanfilled_rand_intv[:i] = rand_intv_sim.infected_results[:i]
        line_rand_intv.set_ydata(nanfilled_rand_intv)
    if intervention_type == "Targeted vaccination":
        nanfilled_targ_intv[:i] = targ_intv_sim.infected_results[:i]
        line_targ_intv.set_ydata(nanfilled_targ_intv)
    if intervention_type == "All":
        nanfilled_rand_intv[:i] = rand_intv_sim.infected_results[:i]
        line_rand_intv.set_ydata(nanfilled_rand_intv)
        nanfilled_targ_intv[:i] = targ_intv_sim.infected_results[:i]
        line_targ_intv.set_ydata(nanfilled_targ_intv)
    the_plot.pyplot(fig)

init()
for i in range(2, len(simulator.timeseries_results_cum), 4):
    animate(i)
    time.sleep(0.01)

st.text(f"Average total number infected: {simulator.total_number_infected}")

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
st.text("Psst... Open the sidebar in the top left to customize this simulation.")