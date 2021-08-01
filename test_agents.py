from mesa import Agent

class Consumer(Agent):

    energy = None

    def __init__(self, unique_id, pos, model, energy=None):
        super().__init__(unique_id, model)
        self.pos = pos
        self.energy = energy

class Producer(Agent):

    energy = None

    def __init__(self, unique_id, pos, model, energy=None):
        super().__init__(unique_id, model)
        self.pos = pos
        self.energy = energy

class Terrain(Agent):

    energy = None

    def __init__(self, unique_id, pos, model, land):
        super().__init__(unique_id, model)
        self.pos = pos
        self.land = land



