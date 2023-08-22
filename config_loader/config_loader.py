import json
from pathlib import Path
import os
import re


def load_json(json_path: Path):
    def remove_comments(content: str):
        return re.sub("//.*\n", "", content)

    with open(json_path) as fp:
        return json.loads(remove_comments(fp.read()))


def load_config(config_path: Path, replace_secrets_with_env: bool = True):
    config = load_json(config_path)

    def replace_secrets(table: dict, secet_keywords: list):
        for k, v in table.items():
            if isinstance(v, dict):
                replace_secrets(v, secet_keywords)
            elif isinstance(v, str):
                for kwd in secet_keywords:
                    if kwd in k and v in os.environ:
                        table[k] = os.environ[v]
                        break

    if replace_secrets_with_env:
        replace_secrets(config, ['api_key', 'token'])

    return config


if __name__ == '__main__':
    config_dir = Path(__file__).parent.parent / 'config'
    cfg = load_config(config_dir / 'config.json')
    print(cfg)
