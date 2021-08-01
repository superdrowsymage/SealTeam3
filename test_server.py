from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from test_agents import Consumer, Producer, Terrain
from test_model import EnergyModel


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Consumer:
        portrayal["Shape"] = "resources/house-48.png"
        # https://icons8.com/icons/set/house
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Producer:
        portrayal["Shape"] = "resources/turbine-64.png"
        # https://icons8.com/icon/69964/wind-turbine
        portrayal["scale"] = 0.9 / 4 * 3
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is Terrain:
        if agent.land:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#00008B", "#ADD8E6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Demand", "Color": "#AA0000"}, {"Label": "Supply", "Color": "#666666"}]
)

model_params = {
    "initial_producers": UserSettableParameter(
        "slider", "Initial Energy Producers", 100, 10, 300
    ),

    "initial_consumers": UserSettableParameter(
        "slider", "Initial Consumer Population", 50, 10, 300
    ),

}

server = ModularServer(
    EnergyModel, [canvas_element, chart_element], "Energy Supply and Demand", model_params
)
server.port = 8521

server.launch()
