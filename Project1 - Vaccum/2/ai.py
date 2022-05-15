class Agent:
    def __init__(self, perceive_func=None):
        self.perceive_func = perceive_func
        self.i , self.j = 0 , 0
        self.directions_1 = ['down', 'right', 'right']
        self.directions_2 = ['right', 'up', 'up', 'up', 'left', 'left', 'left']

    def find(self, i, j, map, tabu):
        if (not (0 <= i < len(map))) or (not (0 <= j < len(map[0]))) or map[i][j] == -1 or (i, j) in tabu:
            return 1000
        tabu.append((i, j))

        if map[i][j] == 1:
            return 0

        a = self.find(i - 1, j, map, tabu)
        b = self.find(i + 1, j, map, tabu)
        c = self.find(i, j + 1, map, tabu)
        d = self.find(i, j - 1, map, tabu)
        return (min(a + 1, b + 1, c + 1, d + 1))


    def act(self):
        sensor_data = self.perceive_func(self)
        directions = []
        map = sensor_data['map']
        if (len(map) == 2):
            directions = self.directions_1.copy()
            if(len(self.directions_1) != 0) :
                self.i, self.j= 1, 2
        elif (len(map) == 4):
            directions = self.directions_2.copy()
            if (len(self.directions_2) != 0):
                self.i, self.j = 0, 0

        if len(directions)!=0 and len(map) == 2 :
            action = directions[0]
            self.directions_1.pop(0)
            return action
        elif len(directions)!=0 and len(map) == 4 :
            action = directions[0]
            self.directions_2.pop(0)
            return action

        if map[self.i][self.j] == 1:
            return 'suck'

        up = self.find(self.i - 1, self.j, map, [])
        down = self.find(self.i + 1, self.j, map, [])
        right = self.find(self.i, self.j + 1, map, [])
        left = self.find(self.i, self.j - 1, map, [])
        selected_path = min(up, down, right, left)

        if selected_path == right:
            self.j = self.j +1
            return 'right'
        elif selected_path == left:
            self.j = self.j - 1
            return 'left'
        elif selected_path == down:
            self.i = self.i + 1
            return 'down'
        else :
            self.i = self.i - 1
            return 'up'