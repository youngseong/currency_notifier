import json
from pathlib import Path
import os
import re


def load_json(json_path: Path):
    def remove_comments(content: str):
        return re.sub(r"//[^\n]*", "", content)

    with open(json_path) as fp:
        return json.loads(remove_comments(fp.read()))


def load_config(config_path: Path, replace_secrets_with_env: bool = True):
    config = load_json(config_path)

    def replace_secrets(table: dict, secret_keywords: list):
        for k, v in table.items():
            if isinstance(v, dict):
                replace_secrets(v, secret_keywords)
            elif isinstance(v, str):
                for kwd in secret_keywords:
                    if kwd in k:
                        env_val = os.environ.get(v)
                        if env_val is None:
                            raise EnvironmentError(
                                f"Required environment variable '{v}' is not set"
                            )
                        table[k] = env_val
                        break

    if replace_secrets_with_env:
        replace_secrets(config, ["api_key", "token"])

    return config


if __name__ == "__main__":
    config_dir = Path(__file__).parent.parent / "config"
    cfg = load_config(config_dir / "config.json")
    print(cfg)
