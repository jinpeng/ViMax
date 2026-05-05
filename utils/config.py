import os
import re
import yaml
from dotenv import load_dotenv

load_dotenv()

_ENV_VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")


def _expand_env_vars(obj):
    """Recursively expand ${VAR} placeholders in strings using os.environ."""
    if isinstance(obj, str):
        def replacer(match):
            var = match.group(1)
            value = os.environ.get(var)
            if value is None:
                raise ValueError(f"Environment variable '{var}' is not set.")
            return value
        return _ENV_VAR_PATTERN.sub(replacer, obj)
    if isinstance(obj, dict):
        return {k: _expand_env_vars(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_expand_env_vars(item) for item in obj]
    return obj


def load_config(config_path: str) -> dict:
    """Load a YAML config file and expand ${VAR} environment variable placeholders."""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return _expand_env_vars(config)
