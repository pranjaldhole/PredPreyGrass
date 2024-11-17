# discretionary libraries
from predpreygrass.predpreygrass.envs import predpreygrass_parallel_v0, predpreygrass_aec_v0
from predpreygrass.predpreygrass.config.config_predpreygrass import (
    env_kwargs,
    training_steps_string,
)

# from predpreygrass.parallel_predpreygrass.eval.utils.evaluator import Evaluator

# external libraries
from pathlib import Path
from stable_baselines3 import PPO
import time


def parallel_evaluation(env_fn, model_path):
    model = PPO.load(model_path)
    render_mode = "human"
    parallel_env = env_fn.parallel_env(**env_kwargs, render_mode=render_mode)
    env_base = parallel_env.predpreygrass
    observations = parallel_env.reset()[
        0
    ]  # Parallel environment reset returns a tuple: (observations, infos)
    done = False
    while not done:
        actions = {
            agent: model.predict(observations[agent], deterministic=True)[0]
            for agent in parallel_env.agents
        }
        observations, rewards = parallel_env.step(actions)[:2]
        """
        for agent, reward in rewards.items():
            if reward > 0.0:
                 print(f"{agent}, reward: {reward}")
        """
        print(
            f"Prey: {env_base.n_active_agent_type[env_base.prey_type_nr]}, Predator: {env_base.n_active_agent_type[env_base.predator_type_nr]}, Grass: {env_base.n_active_agent_type[env_base.grass_type_nr]}"
        )

        done = env_base.is_no_prey or env_base.is_no_predator
        time.sleep(sleep_time)


def aec_evaluation(env_fn, model_path, watch_grid=False):
    model = PPO.load(model_path)
    env = env_fn.env(render_mode="human", **env_kwargs)
    # to access base environment attributes
    env_base = env.unwrapped.predpreygrass
    env.reset(seed=1)
    for agent in env.agent_iter():
        # only first two elements of the tuple are needed
        observation, reward, _, _, _ = env.last()
        """
        if reward > 0.0:
            print(f"{agent}, aec_reward: {reward}")
        """
        if env_base.is_no_prey or env_base.is_no_predator:
            break
        else:
            action = model.predict(observation, deterministic=True)[0]
        env.step(action)
        time.sleep(sleep_time)
    env.close()


if __name__ == "__main__":
    is_parallel = True
    env_fn = predpreygrass_parallel_v0 if is_parallel else predpreygrass_aec_v0
    sleep_time = 0
    environment_name = str(env_fn.parallel_env.metadata['name']) if is_parallel else str(env_fn.raw_env.metadata['name'])
    model_file_name = f"{environment_name}_steps_{training_steps_string}"
         
    destination_source_code_dir = Path(__file__).resolve().parents[1]
    output_directory = destination_source_code_dir / "output"
    loaded_policy = output_directory / model_file_name

    print("Model file loaded from file: ", model_file_name)
    print("Environment name: ", environment_name, "")
    if is_parallel:
        print("Parallel evaluation")
    else:
        print("AEC evaluation")
    print("directory path: ", loaded_policy)

    num_episodes = env_kwargs["num_episodes"]
    training_steps = int(training_steps_string)

    # Evaluate the model
    if is_parallel:
        parallel_evaluation(env_fn=env_fn, model_path=str(loaded_policy))
    else:
        aec_evaluation(env_fn=env_fn, model_path=str(loaded_policy))
