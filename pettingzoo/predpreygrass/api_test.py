# passed API test for predpreygrass
from pettingzoo.test import api_test
import environments.predpreygrass as predpreygrass

env = predpreygrass.raw_env()
api_test(env, num_cycles=1000, verbose_progress=False)