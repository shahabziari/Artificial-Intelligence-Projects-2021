import random
from collections import deque
from copy import deepcopy


class Agent:
    def __init__(self, perceive_func=None, agent_id=None):
        self.perceive_func = perceive_func
        self.my_id = agent_id
        self.predicted_actions = []

    def act(self):
        sensor_data = self.perceive_func(self)
        if self.predicted_actions==[]: self.predicted_actions=self.bfs(sensor_data['Current_Env'])
        action=self.predicted_actions.pop()
        return action


    def idfs(self, root_env):
        def dls(game, limit):
            if game.goal_test():
                return [True, "found the goal"]
            elif limit == 0:
                return [False, "reached limit"]

            actions_list = ["right", "left", "up", "down"]
            if (random.random() < 0.2):
                random.shuffle(actions_list)
            for action in actions_list:
                child_game = deepcopy(game)
                game_result = child_game.take_action(action, self.my_id)
                if 'has died' not in game_result:
                    dls_result = dls(child_game, limit - 1)
                    actions_taken = deepcopy(dls_result[1]) if type(dls_result[1]) is list else []
                    actions_taken.append(action)
                    if dls_result[0]:
                        return [True, actions_taken]

            return [False, "no good action found"]

        depth = 1
        while True:
            print("limited to depth of: ", depth)
            result = dls(root_env, depth)
            if result[0]:
                return result[1]
            depth += 1

    def bfs(self, game):
        queue = deque()
        queue.append([game, []])
        actions_list = ["right", "left", "up", "down"]
        depth = 1
        width = 1
        while queue:
            if width == 0:
                width = len(queue)
                print("limited to depth of: ", depth)
                depth += 1
            width -= 1
            node = queue.popleft()
            if (random.random() < 0.2):
                random.shuffle(actions_list)
            for action in actions_list:
                child_game = node[0].create_copy()
                if 'has died' not in child_game.take_action(action, self.my_id):
                    queue.append([child_game, [action] + node[1]])
                if child_game.goal_test():
                    return [action]+node[1]

    def dfs(self, game):
        stack = deque()
        stack.append([game,[]])
        actions_list = ["right", "left", "up", "down"]
        depth = 1
        while stack:
            print("limited to depth of: ", depth)
            depth += 1
            node = stack.pop()

            if node[0].goal_test():
                return node[1]
            if (random.random() < 0.2):
                random.shuffle(actions_list)
            for action in actions_list:
                child_game = node[0].create_copy()
                result = child_game.take_action(action, self.my_id)
                if 'has died' not in result:
                    stack.append([child_game, [action] + node[1]])
