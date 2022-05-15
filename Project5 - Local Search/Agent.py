import math
import Sensor
import random
import numpy as np
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, mode):
        self.mode = mode

    def act(self):
        method = self.mode
        print(method)
        if method == 'hill':
            self.hill_climbing()
        elif method == 'randomhill':
            self.random_hill_climbing()
        elif method == 'annealing':
            self.simulated_annealing()

    def hill_climbing(self):
        lights = []
        for i in range(5):
            eps = 16
            state = random.uniform(-60.0, 60.0)
            light = Sensor.evaluateState(state)
            while (0.001<eps):
                light = Sensor.evaluateState(state)

                right_neighbour = min(state + eps, 60)
                right_light = Sensor.evaluateState(right_neighbour)

                left_neighbour = max(state - eps, -60)
                left_light = Sensor.evaluateState(left_neighbour)

                if light < right_light or light < left_light:
                    if left_light <= right_light:
                        state = right_neighbour
                        eps = eps * 2
                    elif right_light < left_light:
                        state = left_neighbour
                        eps = eps * 2
                else :
                    eps = eps / 2
            lights.append(light)
            print(f'light : {light} , state : {state}.')
        print(lights)
        plt.plot(lights)
        plt.xlabel('number of test')
        plt.ylabel('lights in this test')
        plt.title('hill_climbing')
        plt.show()

    def random_hill_climbing(self):
        best_lights = []
        for i in range (5):
            best_light = -(math.inf)
            best_state = None
            for j in range(15):
                state = random.uniform(-60.0, 60.0)
                eps = 16
                light = Sensor.evaluateState(state)
                while (0.001<eps):

                    light = Sensor.evaluateState(state)

                    right_neighbour = min(state + eps, 60)
                    right_light = Sensor.evaluateState(right_neighbour)

                    left_neighbour = max(state - eps, 60)
                    left_light = Sensor.evaluateState(left_neighbour)

                    if light < right_light or light < left_light:
                        if left_light <= right_light:
                            state = right_neighbour
                            eps = eps*2
                        elif right_light < left_light:
                            state = left_neighbour
                            eps = eps * 2
                    else:
                        eps = eps / 2
                if light > best_light:
                    best_light = light
                    best_state = state
            best_lights.append(best_light)
            print(f'best light : {best_light} , state : {best_state}.')
        plt.plot(best_lights)
        plt.xlabel('number of test')
        plt.ylabel('light in this test')
        plt.title('randoom-hill_climbing')
        plt.show()

    def simulated_annealing(self):
        lights = []
        temp = 14
        for i in range(5):
            eps = 16
            state = random.uniform(-60.0, 60.0)
            light = Sensor.evaluateState(state)
            for i in range (100):
                light = Sensor.evaluateState(state)

                right_neighbour = min(state + eps, 60)
                right_light = Sensor.evaluateState(right_neighbour)

                left_neighbour = max(state - eps, -60)
                left_light = Sensor.evaluateState(left_neighbour)

                right_diff = light - right_light
                left_diff = light - left_light
                T = temp / float(i + 1)
                if left_light <= right_light:
                    if  light < right_light or random.random() < np.exp(-right_diff / T):
                        state = right_neighbour
                        eps = eps * 2
                elif right_light < left_light:
                    if light < left_light or random.random() < np.exp(-left_diff / T):
                        state = left_neighbour
                        eps = eps * 2
                if light == Sensor.evaluateState(state):
                    eps = eps / 2
            lights.append(light)
            print(f'light : {light} , state : {state}.')
        plt.plot(lights)
        plt.xlabel('number of test')
        plt.ylabel('lights in this test')
        plt.title('simulated_annealing')
        plt.show()


if __name__ == "__main__":
    agent = Agent(mode='annealing')
    agent.act()