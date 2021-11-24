import random
import secrets
from copy import deepcopy
from typing import List

class Node:
    def __init__(self, score, cost, action, parent, snake_body):
        self.score = score
        self.cost = cost
        self.action = action
        self.parent = parent
        self.snake_body = snake_body
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def get_children(self):
        return deepcopy(self.children)

    def is_root(self):
        return self.parent is None

    def __str__(self):
        return f'{self.action, self.snake_body}'

    def __repr__(self):
        return str(self)


class Agent:
    def __init__(self, perceive_func=None, agent_id=None):
        self.perceive_func = perceive_func
        self.my_id = agent_id
        self.prev_action = ''
        self.win_score = 0
        self.turning_cost = 5
        self.food_add_score = 0
        self.food_score_multi = 0


    def act(self):
        sensor_data = self.perceive_func(self)
        agent_body = sensor_data['agent body']
        food_map = sensor_data['map']
        score = sensor_data['score']
        cost = sensor_data['cost']
        env = sensor_data['Current_Env']
        prev_action = self.prev_action
        self.win_score = env.state.winScore
        self.turning_cost = env.state.turningCost
        self.food_add_score = env.state.foodAddScore
        self.food_score_multi = env.state.foodScoreMulti
        snake = env.state.agent_list[0]
        snake_shekam = snake.shekam
        root = self.create_tree(food_map, score, cost, agent_body, 50, prev_action, snake_shekam, None)
        print('tree created')
        return self.get_best_action(root)

    def create_tree(self, food_map: List[List[int]], score: int, cost: int, agent_body: List[List[int]],
                    depth: int, prev_action: str, shekam, parent) -> Node:
        max_x, max_y = len(food_map), len(food_map[0])
        root = Node(score, cost, prev_action, parent, agent_body)
        if depth != 0:
            for action in (['right','left','up','down']):
                if self.is_possible(action, agent_body, max_x, max_y, shekam) :
                    body, new_score, new_shekam = self.get_update(action, food_map, agent_body, score, prev_action,
                                                                     shekam)
                    child = self.create_tree(food_map, new_score, cost + 1, body, depth - 1, action, new_shekam, root)
                    root.add_child(child)
        return root

    def get_best_action(self, root: Node):
        stack = [root]
        max_score, best_move = -1000, ''
        while len(stack) > 0:
            node = stack.pop(len(stack)-1)
            stack.extend(node.get_children())
            if node.score >= self.win_score:
                best_move = self.get_final_action(node)
                break
            if node.score > max_score and node.score != root.score:
                max_score = node.score
                best_move = self.get_final_action(node)
        return best_move

    def get_final_action(self, node):
        if node.parent is None:
            return node.action
        if node.parent.is_root():
            return node.action
        return self.get_final_action(node.parent)

    def is_possible(self, action, agent_body, max_x, max_y, shekam):
        new_head = self.get_new_head(action, agent_body)
        if shekam != 0:
            if new_head in agent_body:
                return False
        else:
            if new_head in agent_body[1:]:
                return False
        if new_head[0] < 0 or new_head[0] == max_x or new_head[1] < 0 or new_head[1] == max_y:
            return False
        return True

    def get_new_head(cls, action, agent_body):
        head = agent_body[-1]
        if (action=='right') :
            return [head[0] , head[1] + 1]
        if (action=='left') :
            return [head[0] , head[1] - 1]
        if (action == 'up'):
            return [head[0] - 1, head[1]]
        if (action == 'down'):
            return [head[0] + 1, head[1]]

    def get_update(self, action, food_map, agent_body, score, prev_action, shekam):
        new_head = self.get_new_head(action, agent_body)
        new_body = deepcopy(agent_body)
        new_body.append(new_head)
        if shekam == 0:
            del new_body[0]
            if len(new_body) != 1:
                del new_body[0]
        new_shekam = shekam
        new_score = score
        if shekam == 0:
            if len(new_body) == 1:
                new_score = score + self.food_add_score + self.food_score_multi * food_map[new_head[0]][new_head[1]]
                new_shekam = food_map[new_head[0]][new_head[1]]
        else:
            new_shekam = shekam - 1
        if action != prev_action:
            new_score -= self.turning_cost

        return new_body, new_score, new_shekam