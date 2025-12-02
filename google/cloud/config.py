import json
from pathlib import Path


def get_or_load_config(config_json_path:str = 'gcs.json') -> dict[str, str]:
    ################################################################
    # create/load config
    ################################################################
    config_json = Path(config_json_path)

    if config_json.exists():
        with open(config_json) as fp:
            config = json.load(fp)
        # print(f'{CONFIG = }')
    else:
        config = {
            "FAKE_BUCKETS_ROOT_DIR": "_FAKE_BUCKET/",
            "PROJECT_DIRNAME": "project_root_dir",
            "LOG_PREFIX": "FAKE_GOOGLE_CLOUD | "
        }
    return config


def get_project_root(project_dir_name:str) -> Path:
    pwd = Path.cwd()
    while pwd.name != project_dir_name:
        pwd = pwd.parent
        # print(f'pwd = {pwd}')
        if pwd == Path('/').resolve():
            raise FileNotFoundError(f'cannot find {project_dir_name}')
    return pwd

CONFIG = get_or_load_config()
PROJECT_ROOT = get_project_root(CONFIG['PROJECT_DIRNAME'])
