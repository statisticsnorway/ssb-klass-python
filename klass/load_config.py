import toml

config = toml.load("klass_config.toml")

LANGUAGES = config["LANGUAGES"]

BASE_URL = config["BASE_URL"]
HEADERS = config["HEADERS"]
