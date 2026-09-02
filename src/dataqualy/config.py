from pathlib import Path
from typing import Any

import yaml


def _require_mapping(config: dict[str, Any], key: str) -> dict[str, Any]:
    value = config.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"A seção '{key}' é obrigatória e deve ser um mapa.")
    return value


def validate_config(config: Any) -> dict[str, Any]:
    """Valida a estrutura mínima antes de iniciar Spark ou acessar bancos."""
    if not isinstance(config, dict):
        raise ValueError("A raiz do YAML deve ser um mapa.")

    mode = config.get("mode", "migration")
    if mode == "package":
        package = _require_mapping(config, "package")
        if not package.get("files") and not package.get("attachments"):
            raise ValueError("Informe package.files ou package.attachments.")
        return config
    if mode != "migration":
        raise ValueError(f"Modo não suportado: {mode}")

    source = _require_mapping(config, "source")
    target = _require_mapping(config, "target")
    _require_mapping(config, "checks")
    if not config.get("key"):
        raise ValueError("O campo 'key' é obrigatório.")

    for name, source_config in (("source", source), ("target", target)):
        source_type = source_config.get("type", "csv")
        if source_type == "csv" and not source_config.get("path"):
            raise ValueError(f"A fonte '{name}' precisa de path.")
        if source_type == "jdbc":
            required = ("engine", "database", "user", "jar")
            missing = [field for field in required if not source_config.get(field)]
            if missing:
                raise ValueError(
                    f"A fonte '{name}' não informou: {', '.join(missing)}."
                )
            if bool(source_config.get("table")) == bool(source_config.get("query")):
                raise ValueError(
                    f"A fonte '{name}' deve informar exatamente table ou query."
                )
        elif source_type != "csv":
            raise ValueError(f"Tipo de fonte não suportado: {source_type}")
    return config


def load_config(path: str | Path) -> dict[str, Any]:
    """Carrega e valida uma configuração YAML UTF-8."""
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuração não encontrada: {config_path}")
    with config_path.open(encoding="utf-8") as file:
        return validate_config(yaml.safe_load(file))


# @hugaojanuario
