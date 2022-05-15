class Agent:
    def __init__(self, perceive_func=None):
        self.perceive_func = perceive_func

    def find(self, i, j, map, tabu):
        if (not(0 <= i < len(map))) or (not(0 <= j < len(map[0]))) or map[i][j] == -1 or (i, j) in tabu:
            return 1000
        tabu.append((i, j))

        if map[i][j] == 1:
            return 0

        a = self.find(i-1 , j, map, tabu)
        b = self.find(i+1 , j , map, tabu)
        c = self.find(i , j+1, map, tabu)
        d = self.find(i , j-1, map, tabu)
        return (min(a + 1, b + 1, c + 1, d + 1))

    def act(self):
        sensor_data = self.perceive_func(self)

        map = sensor_data['map']
        i, j = sensor_data['agent_loc']
        if map[i][j] == 1:
            return 'suck'
        up = self.find(i - 1, j, map, [])
        down = self.find(i + 1, j, map, [])
        right = self.find(i, j + 1, map, [])
        left = self.find(i, j - 1, map, [])
        selected_path = min(up, down, right, left)
        if selected_path == right:
            return 'right'
        elif selected_path == left:
            return 'left'
        elif selected_path == down:
            return 'down'
        return 'up'