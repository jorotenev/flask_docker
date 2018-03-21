from os.path import join, dirname
from dotenv import load_dotenv

print("Trying to load .env_test")
dotenv_path = join(dirname(__file__), '../.env_test')
load_dotenv(dotenv_path, verbose=True)
