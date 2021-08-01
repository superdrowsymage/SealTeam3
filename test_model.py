from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from test_agents import Producer, Consumer, Terrain
from test_schedule import RandomActivationByType


class EnergyModel(Model):
    """
    Energy Model
    """

    height = 20
    width = 20

    initial_producers = 100
    initial_consumers = 50

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating energy."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_producers=100,
        initial_consumers=50,
    ):
        """
        Create a new model with the given parameters.

        Args:
            initial_producers: Number of turbines to start with
            initial_consumers: Number of houses to start with
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_producers = initial_producers
        self.initial_consumers = initial_consumers

        self.schedule = RandomActivationByType(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector(
            {
                "Consumers": lambda m: m.schedule.get_energy_count(Consumer),
                "Sheep": lambda m: m.schedule.get_energy_count(Producer),
            }
        )

        # Create producers:
        for i in range(self.initial_producers):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = 5
            producer = Producer(self.next_id(), (x, y), self, energy)
            self.grid.place_agent(producer, (x, y))
            self.schedule.add(producer)

        # Create consumers
        for i in range(self.initial_consumers):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = 1
            consumer = Consumer(self.next_id(), (x, y), self, energy)
            self.grid.place_agent(consumer, (x, y))
            self.schedule.add(consumer)

        # Create landmass
        for agent, x, y in self.grid.coord_iter():
            land = self.random.choice([True, False])

            patch = Terrain(self.next_id(), (x, y), self, land)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                ]
            )

    def run_model(self, step_count=200):

        for i in range(step_count):
            self.step()
