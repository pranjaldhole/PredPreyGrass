[![Python 3.11.7](https://img.shields.io/badge/python-3.11.7-blue.svg)](https://www.python.org/downloads/release/python-3117/)
[![PettingZoo version dependency](https://img.shields.io/badge/PettingZoo-v1.24.3-blue)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Wiki](https://img.shields.io/badge/Wiki-background-green)]()
</br>
<p align="center">
    <img src="https://github.com/doesburg11/PredPreyGrass/blob/main/assets/images/readme/predpreygrass.png" width="700" height="80"/> 
</p>
</br>

## The environments
[**so_predpregrass_v0.py**](https://github.com/doesburg11/PredPreyGrass/tree/main/predpreygrass/envs/_so_predpreygrass_v0): A (single-objective) multi-agent reinforcement learning (MARL) environment, [trained and evaluated](https://github.com/doesburg11/PredPreyGrass/tree/main/predpreygrass/optimizations/so_predpreygrass_v0) using Proximal Policy Optimization (PPO). Learning agents Predators (red) and Prey (blue) both expend energy moving around, and replenish it by eating. Prey eat Grass (green), and Predators eat Prey if they end up on the same grid cell. In the base case for simplicity, the agents obtain all the energy from the eaten Prey or Grass. Predators die of starvation when their energy is zero, Prey die either of starvation or when being eaten by a Predator. The agents asexually reproduce when energy levels of learning agents rise above a certain treshold by eating. Learning agents, learn to execute movement actions based on their partial observations (transparent red and blue squares respectively) of the environment to maximize cumulative reward. The single objective rewards (fore stepping, eating, dying and reproducing) are simply added and can be adjusted in the [environment configuration](https://github.com/doesburg11/PredPreyGrass/blob/main/predpreygrass/envs/_so_predpreygrass_v0/config/config_predpreygrass.py) file. 

[**mo_predpregrass_v0.py**](https://github.com/doesburg11/PredPreyGrass/tree/main/predpreygrass/envs/_mo_predpreygrass_v0):  A (multi-objective) multi-agent reinforcement learning (MOMARL) environment. The envrionment has two objectives: 1) maximize cumulative rewards for reproduction of Predator agents and 2) maximize cumulative rewards for reproduction of Prey agents. The rewards returned by the environment are stored in a two-dimensional vector in accordance with Farama's [Momaland](https://momaland.farama.org/) framework.

</br>
</br>
<p align="center">
    <img src="https://github.com/doesburg11/PredPreyGrass/blob/main/assets/gif/predpreygrass.gif" width="1000" height="200"/>
</p>


## Emergent Behaviors
The PPO algorithm is an example of how elaborate behaviors can emerge from simple rules in agent-based models. In the above displayed MARL example, rewards for learning agents are only obtained by reproduction. However, maximizing these rewards results in emerging behaviors such as: 1) Predators hunting Prey, 2) Predators hovering around grass to catch Prey and 3) Prey trying to escape Predators. These emerging behaviors lead to more complex dynamics at the ecosystem level. The trained agents are displaying a classic [Lotka–Volterra](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations) pattern over time. This learned outcome is not obtained with a random policy:

<p align="center">
    <img src="https://github.com/doesburg11/PredPreyGrass/blob/main/assets/images/readme/PredPreyPopulation_episode.png" width="450" height="270"/>
</p>

More emergent behavior and findings are described [on our website](https://www.behaviorpatterns.info/predator-prey-grass-project/).


## Installation

**Editor used:** Visual Studio Code 1.93.1 on Linux Mint 21.3 Cinnamon

1. Clone the repository: 
   ```bash
   git clone https://github.com/doesburg11/PredPreyGrass.git
   ```
2. Open Visual Studio Code and execute:
   - Press `ctrl+shift+p`
   - Type and choose: "Python: Create Environment..."
   - Choose environment: Conda 
   - Choose interpreter: Python 3.11.7
   - Open a new terminal
   - Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. If encountering "ERROR: Failed building wheel for box2d-py," run:
   ```bash
   conda install swig
   ```
   and
   ```bash
   pip install box2d box2d-kengz
   ```
4. Alternative 1:
   ```bash
   pip install wheel setuptools pip --upgrade
   pip install swig
   pip install gymnasium[box2d]
   ``` 
6. Alternative 2: a workaround is to copy Box2d files from [assets/box2d](https://github.com/doesburg11/PredPreyGrass/tree/main/assets/box2d) to the site-packages directory.
7. If facing "libGL error: failed to load driver: swrast," execute:
    ```bash
    conda install -c conda-forge gcc=12.1.0
    
## Getting started

### Visualize a random policy
In Visual Studio Code run:
```pettingzoo/predpreygrass/random_policy.py```
</br>
<p align="center">
    <img src="https://github.com/doesburg11/PredPreyGrass/blob/main/assets/gif/predpreygrass_random.gif" width="1000" height="200"/>
</p>


### Training and visualize trained model using PPO from stable baselines3
Adjust parameters accordingly in:
```predpreygrass/envs/_predpreygrass_v0/config/config_predpreygrass.py```
In Visual Studio Code run:
```predpreygrass/optimizationspredpreygrass/train_predpreygrass_v0_ppo.py```
To evaluate and visualize after training follow instructions in:
```predpreygrass/optimizationspredpreygrass/evaluate_from_file.py```

## Configuration of the PredPreyGrass environment
[The benchmark configuration](https://github.com/doesburg11/PredPreyGrass/blob/main/predpreygrass/envs/_predpreygrass_v0/config/config_predpreygrass.py) used in the gif-video above.

## References

- [Terry, J and Black, Benjamin and Grammel, Nathaniel and Jayakumar, Mario and Hari, Ananth and Sullivan, Ryan and Santos, Luis S and Dieffendahl, Clemens and Horsch, Caroline and Perez-Vicente, Rodrigo and others. Pettingzoo: Gym for multi-agent reinforcement learning. 2021-2024](https://pettingzoo.farama.org/)    
- [Paper Collection of Multi-Agent Reinforcement Learning (MARL)](https://github.com/LantaoYu/MARL-Papers)
- [MOMAland: A Set of Benchmarks for Multi-Objective Multi-Agent Reinforcement Learning (MOMARL). Florian Felten and Umut Ucak and Hicham Azmani and Gao Peng and Willem Röpke and Hendrik Baier and Patrick Mannion and Diederik M. Roijers and Jordan K. Terry and El-Ghazali Talbi and Grégoire Danoy and Ann Nowé and Roxana Rădulescu](https://momaland.farama.org/)
- [Multi-Objective Multi-Agent Decision Making: A Utility-based Analysis and Survey](https://arxiv.org/abs/1909.02964)
- [A Practical Guide to Multi-Objective Reinforcement Learning and Planning](https://arxiv.org/abs/2103.09568)
- [Multi-Agent Reinforcement Learning: Foundations and Modern Approaches. Stefano V. Albrecht, Filippos Christianos, and Lukas Schäfer](https://www.marl-book.com/download/marl-book.pdf)




