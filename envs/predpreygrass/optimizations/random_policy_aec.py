from pettingzoo.sisl import predpreygrass_v0
from pettingzoo.preconfigs.config_predpreygrass import env_kwargs



env = predpreygrass_v0.env(render_mode='human', **env_kwargs)



env.reset()
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()
    if reward > 0:
        print(agent," reward: ", reward)

    if termination or truncation:
        action = None
    else:
        action = env.action_space(agent).sample() # this is where you would insert your policy

    env.step(action)
env.close()