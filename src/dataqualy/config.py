from typing import Any

import yaml

def load_config(path: str) -> dict[str, Any]:
    """carrega a config do YAML do projeto """
    with open(path, encoding="utf-8") as file:
        return yaml.safe_load(file)
