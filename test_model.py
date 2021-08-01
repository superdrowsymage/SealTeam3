from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from test_agents import Turbine, House, Terrain
from test_schedule import RandomActivationByType

import numpy as np

class RenewableModel(Model):
    """
    Energy Model
    """

    height = 20
    width = 20

    initial_producers = 100
    houses = 50

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating energy."
    )

    def __init__(self, height=20, width=20, turbines=25, houses=15, ):
        """
        Create a new model with the given parameters.

        Args:
            turbines: Number of turbines to start with
            houses: Number of houses to start with
        """
        super().__init__()

        # Set parameters
        self.height = height
        self.width = width
        self.turbines = turbines
        self.houses = houses

        self.schedule = RandomActivationByType(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector(
            {
                "Consumers": lambda m: m.schedule.get_energy_count(House),
                "Producers": lambda m: m.schedule.get_energy_count(Turbine),
            }
        )

        land_coords = []

        # Create landmass
        for agent, x, y in self.grid.coord_iter():
            land = True  # can be false for water
            if land:
                land_coords.append((x, y))
            patch = Terrain(self.next_id(), (x, y), self, land)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)

        # Create consumers
        for i in range(self.houses):
            num = self.random.choice(np.arange(len(land_coords)))
            (x, y) = land_coords[num]
            land_coords.pop(num)

            energy = 1
            house = House(self.next_id(), (x, y), self, energy)
            self.grid.place_agent(house, (x, y))
            self.schedule.add(house)

        # Create producers:
        for i in range(self.turbines):
            num = self.random.choice(np.arange(len(land_coords)))
            (x, y) = land_coords[num]
            land_coords.pop(num)
            energy = 5
            turbine = Turbine(self.next_id(), (x, y), self, energy)
            self.grid.place_agent(turbine, (x, y))
            self.schedule.add(turbine)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()

        # collect data
        # self.datacollector.collect(self)

    def run_model(self, step_count=200):

        for i in range(step_count):
            self.step()
