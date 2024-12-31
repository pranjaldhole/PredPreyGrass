# discretionar libraries
from predpreygrass.single_objective.train.utils.logger import SampleLoggerCallback

# external libraries
import os
import supersuit as ss
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from pettingzoo.utils.conversions import parallel_wrapper_fn

class Trainer:
    def __init__(
            self, 
            env_fn, 
            output_directory: str, 
            model_file_name: str,
            steps: int = 10_000, 
            seed: int = 0, 
            **env_kwargs):
        self.env_fn = env_fn
        self.output_directory = output_directory
        self.model_file_name = model_file_name
        self.steps = steps
        self.seed = seed
        self.env_kwargs = env_kwargs

    def train_parallel_wrapped_aec_env(self):
        parallel_env = parallel_wrapper_fn(self.env_fn.raw_env)

        # Train a single model to play as each agent in a parallel environment
        raw_parallel_env = parallel_env(render_mode=None, **self.env_kwargs)
        raw_parallel_env.reset(seed=self.seed)
        num_cores = 2 # os.cpu_count()

        # for google cloud platform
        if num_cores == 128:
            n_steps = 818
            batch_size = 209_408
            total_timesteps = 10_470_4000
        # for local machine
        elif num_cores == 8:
            n_steps = 2048
            batch_size = 32_768
            total_timesteps = self.steps
        # for google cloud platform 
        elif num_cores == 2:
            n_steps = 2048
            batch_size = 8_192
            total_timesteps = 4_096_000 # 10_240_000



        print(f"Starting training on {str(raw_parallel_env.metadata['name'])}.")
        # create parallel environments by concatenating multiple copies of the base environment
        num_vec_envs_concatenated = num_cores
        print("Number of CPU cores utilized: ", num_cores)
        raw_parallel_env = ss.pettingzoo_env_to_vec_env_v1(raw_parallel_env)
        raw_parallel_env = ss.concat_vec_envs_v1(
            raw_parallel_env,
            num_vec_envs_concatenated,
            num_cpus=num_cores,
            base_class="stable_baselines3",
        )

        model = PPO(
            MlpPolicy,
            raw_parallel_env,
            n_steps=n_steps,
            batch_size=batch_size,  # Factor of 1,638,400; n_steps * num_envs (8) * n_possible_agents (100)
            n_epochs=10,        # Default number of epochs
            verbose=0,  # 0 for no output, 1 for info messages, 2 for debug messages, 3 default
            tensorboard_log=self.output_directory + "/ppo_predprey_tensorboard/",
         )

        sample_logger_callback = SampleLoggerCallback()

        model.learn(
            total_timesteps=total_timesteps, progress_bar=True, callback=sample_logger_callback
        )
        saved_directory_and_model_file_name = self.output_directory + "/" + self.model_file_name + ".zip" 

        model.save(saved_directory_and_model_file_name)   

        print("Saved model to: ", saved_directory_and_model_file_name)
        print("Model has been saved.")
        print(f"Finished training on {str(raw_parallel_env.unwrapped.metadata['name'])}.")

        raw_parallel_env.close()

    def train_unwrapped_parallel_env(self):
        parallel_env = self.env_fn.parallel_env

        # Train a single model to play as each agent in a parallel environment
        raw_parallel_env = parallel_env(render_mode=None, **self.env_kwargs)
        raw_parallel_env.reset(seed=self.seed)

        print(f"Starting training on {str(raw_parallel_env.metadata['name'])}.")
        # create parallel environments by concatenating multiple copies of the base environment
        num_vec_envs_concatenated = 8
        raw_parallel_env = ss.pettingzoo_env_to_vec_env_v1(raw_parallel_env)
        raw_parallel_env = ss.concat_vec_envs_v1(
            raw_parallel_env,
            num_vec_envs_concatenated,
            num_cpus=8,
            base_class="stable_baselines3",
        )

        model = PPO(
            MlpPolicy,
            raw_parallel_env,
            n_steps=2048,
            batch_size=32_768,  # Factor of 1,638,400; n_steps * num_envs (8) * n_possible_agents (100)
            n_epochs=10,        # Default number of epochs
            verbose=0,  # 0 for no output, 1 for info messages, 2 for debug messages, 3 default
            tensorboard_log=self.output_directory + "/ppo_predprey_tensorboard/",
        )

        sample_logger_callback = SampleLoggerCallback()

        model.learn(
            total_timesteps=self.steps, progress_bar=True, callback=sample_logger_callback
        )
        saved_directory_and_model_file_name = self.output_directory + "/" + self.model_file_name + ".zip" 

        model.save(saved_directory_and_model_file_name)   

        print("Saved model to: ", saved_directory_and_model_file_name)
        print("Model has been saved.")
        print(f"Finished training on {str(raw_parallel_env.unwrapped.metadata['name'])}.")

        raw_parallel_env.close()

