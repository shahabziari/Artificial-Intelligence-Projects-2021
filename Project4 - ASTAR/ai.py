import random
from queue import PriorityQueue
import json
from modeled_env import ModeledEnv, set_constants
from time import time


class Agent:
    def __init__(self, perceive_func=None, agent_id=None, optimized=True, mode='a_star'):
        self.perceive_func = perceive_func
        self.my_id = agent_id

        self.predicted_actions = []
        self.actions_list = ['u', 'r', 'd', 'l']

        self.optimized = optimized
        self.alg = eval('self.'+mode)
        print('running '+mode)

    def act(self):
        sensor_data = self.perceive_func(self)
        if self.optimized:
            set_constants(json.loads(sensor_data['Current_Env'])['state'])
            sensor_data['Current_Env'] = ModeledEnv()
        else:
            from env import Env
            self.actions_list = ['up', 'right', 'down', 'left']
            sensor_data['Current_Env'] = Env([1], [1]).from_json(**json.loads(sensor_data['Current_Env'])['state'])

        if self.predicted_actions == []:
            t0=time()
            self.predicted_actions = self.alg(sensor_data['Current_Env'])
            if self.optimized:
                self.predicted_actions=self.change_actions()
            print(time()-t0)

        action = self.predicted_actions.pop()

        return action

    def change_actions(self):
        actions1 = {'u': 'up', 'l': 'left', 'd': 'down', 'r': 'right'}
        changed_action = []
        for i in range(len(self.predicted_actions)):
            changed_action.append(actions1[self.predicted_actions[i]])
        return changed_action

    #DIDN'T CHAMGE IT
    def bfs(self, root_game):
        q = []
        q.append([root_game, []])
        while q:
            # pop first element from queue
            node = q.pop(0)
            if random.random()<0.2: random.shuffle(self.actions_list)
            for action in self.actions_list:
                # add children to queue
                child_game = node[0].create_copy()
                if 'd' not in child_game.take_action(action, self.my_id):
                    q.append([child_game, [action] + node[1]])
                # goal test
                if child_game.goal_test():
                    return [action] + node[1]


    def ucs(self, root_game):
        q = PriorityQueue()
        agent = root_game.state.agent_list[self.my_id]
        q.put((agent.realCost,id([root_game, []]),[root_game, []]))

        while q:
            node = q.get()[2]
            if random.random() < 0.2: random.shuffle(self.actions_list)
            for action in self.actions_list:
                child_game = node[0].create_copy()
                if 'd' not in child_game.take_action(action, self.my_id):
                    agent = child_game.state.agent_list[self.my_id]
                    q.put((agent.realCost,id([child_game,[action] + node[1]]), [child_game, [action] + node[1]]))

                if child_game.goal_test(): return [action] + node[1]


    def heuristic(self, state):
        agent = state.agent_list[self.my_id]
        return (state.winScore-agent.foodScore)/14 + agent.shekam + len(agent.body)


    def a_star(self, root_game):
        q = PriorityQueue()
        agent = root_game.state.agent_list[self.my_id]
        q.put((self.heuristic(root_game.state) + agent.realCost, id([root_game, []]) , [root_game, []]))
        while q:
            node = q.get()[2]
            if random.random() < 0.2: random.shuffle(self.actions_list)
            for action in self.actions_list:
                child_game = node[0].create_copy()
                if 'd' not in child_game.take_action(action, self.my_id):
                    agent = child_game.state.agent_list[self.my_id]
                    q.put((self.heuristic(child_game.state)+ agent.realCost,
                           id([child_game,[action] + node[1]]), [child_game, [action] + node[1]]))

                if child_game.goal_test(): return [action] + node[1]