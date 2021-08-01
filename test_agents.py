from mesa import Agent

class House(Agent):
    """A house consumes energy"""

    energy = None

    def __init__(self, unique_id, pos, model, energy=None):
        super().__init__(unique_id, model)
        self.pos = pos
        self.energy = -self.random.randint(0, 10)

class Turbine(Agent):
    """Agent produces energy each tick"""

    energy = None

    def __init__(self, unique_id, pos, model, energy=None):
        super().__init__(unique_id, model)
        self.pos = pos
        self.energy = energy

    def produce_energy(self):
        self.energy += self.random.randint(0, 10)

    def get_dist(self):
        pass

    def transfer_energy(self):
        other_agent = self.random.choice(self.model.schedule.agents)
        other_agent.energy += 1
        self.energy -= 1

class Terrain(Agent):

    energy = None
    wind_value = 0

    def __init__(self, unique_id, pos, model, land):
        super().__init__(unique_id, model)
        self.pos = pos
        self.land = land
