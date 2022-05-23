import time
import numpy as np
from epintervene.simobjects import simulation
from epintervene.simobjects import extended_simulation
import matplotlib.pyplot as plt
import sample_networks


class SimType:
    def __init__(self, sim_type, adj_list, rollout_gens=None, rollout_proportns=None):
        self.sim_type = sim_type
        self.adj_list = adj_list
        self.rollout_gens = rollout_gens
        self.rollout_proportns = rollout_proportns
        self.sim_obj = self.get_sim_object()

    def get_sim_object(self):
        if self.sim_type == "standard":
            return simulation.Simulation(N=len(self.adj_list), adj_list=self.adj_list)
        elif self.sim_type == "random_rollout":
            sim = extended_simulation.RandomRolloutSimulation(N=len(self.adj_list), adjlist=self.adj_list)
            print(self.rollout_gens)
            sim.configure_intervention(intervention_gen_list=self.rollout_gens, beta_redux_list=self.rollout_proportns, proportion_reduced_list=self.rollout_proportns)
            return sim
        elif self.sim_type == "targeted_rollout":
            sim = extended_simulation.TargetedRolloutSimulation(N=len(self.adj_list), adjlist=self.adj_list)
            sim.configure_intervention(self.rollout_gens, self.rollout_proportns, self.rollout_proportns)
            return sim


class Simulator:
    def __init__(self, sim_type, rollout_gens=None, rollout_proportns=None):
        self.sim_type = sim_type
        self.max_time = 0
        self.timeseries_results_cum = None
        self.infected_results = None
        self.recovered_results = None
        self.total_number_infected = None
        self.rollout_gens = rollout_gens
        self.rollout_proportns = rollout_proportns

    def calibrate(self, adj_list, gamma, beta):
        # Initial simulation to callibrate custom time limit and x_range for plot, runs five times and takes max
        max_time_result = 0
        for t in range(5):
            # progress_bar.progress(1 / int(num_sims))
            # status_text.text("Running Simulations:\n %s%% Complete" % (int(1 / int(num_sims) * 100)))
            # sim = simulation.Simulation(N=len(adj_list), adj_list=adj_list)
            sim = SimType(self.sim_type, adj_list, rollout_gens=self.rollout_gens,
                          rollout_proportns=self.rollout_proportns).sim_obj
            sim.set_uniform_gamma(gamma)
            sim.set_uniform_beta(beta)
            sim.run_sim(wait_for_recovery=True)
            timeseries_results = sim.tabulate_continuous_time(time_buckets=100)
            if np.max(timeseries_results[0]) > max_time_result:
                max_time_result = np.max(timeseries_results[0])
        self.max_time = max_time_result
        return max_time_result

    def simulate(self, num_sims, gamma, beta, adj_list, progress_bar, status_text):
        self.calibrate(adj_list=adj_list, gamma=gamma, beta=beta)
        # single
        # sim = simulation.Simulation(N=len(adj_list), adj_list=adj_list)
        sim = SimType(self.sim_type, adj_list, rollout_gens=self.rollout_gens,
                          rollout_proportns=self.rollout_proportns).sim_obj
        sim.set_uniform_gamma(gamma)
        sim.set_uniform_beta(beta)
        sim.run_sim(wait_for_recovery=True)
        custom_time_limit = self.max_time + 20
        timeseries_results = sim.tabulate_continuous_time(time_buckets=100, custom_range=True,
                                                          custom_t_lim=custom_time_limit)

        timeseries_results_cum = timeseries_results[0]
        infected_results = timeseries_results[1]
        recovered_results = timeseries_results[2]
        total_number_infected = timeseries_results[1][-1] + timeseries_results[2][-1]

        for s in range(1, int(num_sims) + 1):
            # sim = simulation.Simulation(N=len(adj_list), adj_list=adj_list)
            sim = SimType(self.sim_type, adj_list, rollout_gens=self.rollout_gens,
                          rollout_proportns=self.rollout_proportns).sim_obj
            sim.set_uniform_gamma(gamma)
            sim.set_uniform_beta(beta)
            sim.run_sim(wait_for_recovery=True)
            timeseries_results = sim.tabulate_continuous_time(time_buckets=100, custom_range=True,
                                                              custom_t_lim=custom_time_limit)
            timeseries_results_cum += timeseries_results[0]
            infected_results += timeseries_results[1]
            recovered_results += timeseries_results[2]
            total_number_infected += (timeseries_results[1][-1] + timeseries_results[2][-1])
            progress_bar.progress(s / int(num_sims))
            status_text.text("Running Simulations:\n %s%% Complete" % (int(s / int(num_sims) * 100)))
        status_text.text(f"{int(num_sims)} Simulations Complete")
        self.timeseries_results_cum = timeseries_results_cum / int(num_sims)
        self.infected_results = infected_results / int(num_sims)
        self.recovered_results = recovered_results / int(num_sims)
        self.total_number_infected = total_number_infected / int(num_sims)