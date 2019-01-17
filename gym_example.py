#! /usr/bin/python3.6

from rover_domain_core_gym import rover_domain_core_gym
from parameters import Parameters as p
from mods import Mod as m
from code.agent import *
from code.trajectory_history import create_trajectory_histories, save_trajectory_histories, update_trajectory_histories
from code.reward_history import save_reward_history, create_reward_history, update_reward_history
from code.ccea import Ccea
from code.neural_network import NeuralNetwork
import numpy as np

step_count = p.data["Steps"]
generations_per_episode = p.data["Generations per Episode"]
tests_per_episode = p.data["Tests per Episode"]
num_episodes = p.data["Number of Episodes"]

# NOTE: Add the mod functions (variables) to run to mod_col here:
mod_col = [
    m.global_reward_mod
    #m.difference_reward_mod,
    #m.dpp_reward_mod
]

stat_runs = 1
sim = rover_domain_core_gym()
cc = Ccea(); nn = NeuralNetwork()

for func in mod_col:
    #func(p.data)

    for s in range(stat_runs):
        print("Run %i" % s)

        # Trial Begins
        create_reward_history(p.data)
        p.data["Steps"] = step_count
        cc.reset_populations()
        nn.reset_nn()

        # Training Phase
        # obs = sim.reset('Train', True)

        for gen in range(generations_per_episode):
            p.data["World Index"] = gen
            # obs = sim.reset('Train', False)
            cc.create_new_pop()  # Create a new population via mutation
            cc.select_policy_teams()
            joint_state = get_agent_state(p.data)

            for policies in range(cc.population_size):
                joint_action = np.zeros((p.data["Number of Agents"], p.data["Number of Outputs"]))

                for rover_id in range(p.data["Number of Agents"]):
                    nn.get_inputs(joint_state[rover_id], rover_id)
                    pol_select = cc.team_selection[rover_id, 0]
                    nn.get_weights(cc.pops[rover_id, pol_select], rover_id)
                    joint_action[rover_id] = nn.get_outputs(rover_id)

                # Rovers execute actions
                # Performance is evaluated
                # Fitness assigned

            # Down selection

            # done = False
            # step_count = 0
            # while not done:
            #     get_agent_actions(p.data)
            #     joint_action = p.data["Agent Actions"]
            #     obs, reward, done, info = sim.step(joint_action)
            #     step_count += 1

        # # Testing Phase
        # obs = sim.reset('Test', True)
        #
        # for test in range(tests_per_episode):
        #     p.data["World Index"] = test
        #     obs = sim.reset('Test', False)
        #
        #     done = False
        #     step_count = 0
        #     while not done:
        #         get_agent_actions(p.data)
        #         joint_action = p.data["Agent Actions"]
        #         obs, reward, done, info = sim.step(joint_action)
        #         step_count += 1

        # update_reward_history(p.data)
        #
        # # Trial End
        # save_reward_history(p.data)
        # save_trajectory_histories(p.data)
