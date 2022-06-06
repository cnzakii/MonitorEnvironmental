import os
from lib import config
file_path = os.path.join(os.path.abspath('..'), 'db_config.ini')
print(file_path)
print(config.read_config('mysql'))