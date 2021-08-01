from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from test_agents import House, Turbine, Terrain
from test_model import RenewableModel


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is House:
        portrayal["Shape"] = "resources/house-48.png"
        # https://icons8.com/icons/set/house
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["text"] = agent.energy
        portrayal["text_color"] = "Red"

    elif type(agent) is Turbine:
        portrayal["Shape"] = "resources/turbine-64.png"
        # https://icons8.com/icon/69964/wind-turbine
        portrayal["scale"] = 0.9 / 4 * 3
        portrayal["Layer"] = 2
        portrayal["text"] = agent.energy
        portrayal["text_color"] = "Green"

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


canvas_element = CanvasGrid(agent_portrayal, RenewableModel.width, RenewableModel.height, 600, 600)
chart_element = ChartModule(
    [{"Label": "Demand", "Color": "#AA0000"}, {"Label": "Supply", "Color": "#666666"}]
)

model_params = {
    "turbines": UserSettableParameter(
        "slider", "Initial Energy Producers", 40, 10, 120
    ),

    "houses": UserSettableParameter(
        "slider", "Initial House Population", 15, 10, 80
    ),

}

server = ModularServer(
    RenewableModel, [canvas_element, chart_element], "Energy Supply and Demand", model_params
)
server.port = 8521

server.launch()
