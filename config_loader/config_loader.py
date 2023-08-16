import collections.abc
import json
from pathlib import Path


def load_config(config_path: Path, *args) -> dict:
    with open(config_path) as fp:
        config = json.load(fp)
        if args:
            # https://stackoverflow.com/a/3233356
            def update(d: dict, u: dict):
                for k, v in u.items():
                    if isinstance(v, collections.abc.Mapping):
                        d[k] = update(d.get(k, {}), v)
                    else:
                        d[k] = v
                return d

            update(config, load_config(*args))
    return config


if __name__ == '__main__':
    config_dir = Path(__file__).parent.parent / 'config'
    cfg = load_config(config_dir / 'base.json')
    print(cfg)
