"""
- to evaluate a ppo trained and saved model
- evaluation can be done with or without watching the grid
instructions:
- navigate with linux mint file-explorer to your local directory defined in:
  "predpreygrass/aec_predpreygrass/config/config_predpreygrass.py"
- note that the entire file/directory structure of the project is copied 
  during training to the defined local directory
- go to the directory with the appropriate time stamp of training and go 
  down the directory tree:
  /eval/evaluate_ppo_from_file.py
- right mouseclick "evaluate_ppo_rom_file.py" and:
- select "Open with"
- select "Visual Studio Code" 
- select "Run without debugging"
- results can be found in: /[time_stamp]/output/
"""
# discretionary libraries
from predpreygrass.single_objective.envs import predpreygrass_aec_v0, predpreygrass_parallel_v0
from predpreygrass.single_objective.config.config_predpreygrass import (
    env_kwargs,
)
from predpreygrass.single_objective.eval.utils.evaluator import Evaluator

# external libraries
import os
from os.path import dirname as up 

if __name__ == "__main__":
    training_steps_string = env_kwargs["training_steps_string"]
    watch_grid_model = env_kwargs["watch_grid_model"]
    num_episodes = env_kwargs["num_episodes"] 
    is_parallel = env_kwargs["is_parallel"]
    env_fn = predpreygrass_parallel_v0 if is_parallel else predpreygrass_aec_v0
    environment_name = str(env_fn.parallel_env.metadata['name']) if is_parallel else str(env_fn.raw_env.metadata['name'])
    model_file_name = f"{environment_name}_steps_{training_steps_string}"
    evaluation_directory = os.path.dirname(os.path.abspath(__file__))
    print("evaluation_directory: ", evaluation_directory)
    destination_source_code_dir = up(up(__file__))  # up 2 levels in directory tree
    print("destination_source_code_dir: ", destination_source_code_dir)
    output_directory = destination_source_code_dir +"/output/"
    loaded_policy = output_directory + model_file_name
    # input from so_config_predpreygrass.py
    training_steps = int(training_steps_string)

    render_mode = "human" if watch_grid_model else None

    # Create an instance of the Evaluator class
    evaluator = Evaluator(
        env_fn,
        output_directory, # destination_output_dir,
        loaded_policy,
        destination_source_code_dir, # destination_root_dir,
        render_mode,
        destination_source_code_dir, # destination_source_code_dir,
        **env_kwargs
    )

    # Call the eval method to perform the evaluation
    if is_parallel:
      evaluator.parallel_evaluation()
    else:
      evaluator.aec_evaluation()
    