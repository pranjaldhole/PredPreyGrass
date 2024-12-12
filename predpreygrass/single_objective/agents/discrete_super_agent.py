+# external libraries
from pettingzoo.utils.env import AgentID
import numpy as np

class DiscreteSuperAgent:
    def __init__(
        self,
        agent_type_nr: int,
        agent_id_nr: int,
        agent_name: AgentID,
        initial_energy: float = 10,
        energy_gain_per_step: float = -0.1,
    ):
        # identification agent
        self.agent_type_nr: int = agent_type_nr  # also channel number of agent
        self.agent_name: AgentID = agent_name  # string like "prey_1"
        self.agent_id_nr: int = agent_id_nr  # unique integer per agent

        self.position: np.ndarray = np.zeros(2, dtype=np.int32)  # x and y position
        self.energy: float = initial_energy  # still to implement
        self.energy_gain_per_step: float = energy_gain_per_step

        self.is_active: bool = False
        self.age: int = 0

        self.x_grid_dim: int = self.model_state_agent.shape[0]
        self.y_grid_dim: int = self.model_state_agent.shape[1]


    def step(self, **kwargs) -> None:
        self.energy += self.energy_gain_per_step
        self.age += 1


