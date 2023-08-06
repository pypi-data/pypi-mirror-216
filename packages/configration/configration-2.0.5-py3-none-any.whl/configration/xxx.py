from pathlib import Path
from src.toml_config import TomlConfig

extension = 'toml'

path = Path('tests', 'test_data', f'config_invalid_{extension}.{extension}')
err_msg = f"Invalid {extension} format in {path}"
TomlConfig(path)
