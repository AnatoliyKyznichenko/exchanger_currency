from dotenv import dotenv_values
from services.api_sqlite import *

config_file = dotenv_values('.env')
user_id = (786332182, 466963358,)
id_channel = -1001550861551
db = Admin()