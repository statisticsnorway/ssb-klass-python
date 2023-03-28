import toml
import os

config = toml.load(os.path.abspath("klass/klass_config.toml"))

LANGUAGES = config["LANGUAGES"]

BASE_URL = config["BASE_URL"]
HEADERS = config["HEADERS"]
