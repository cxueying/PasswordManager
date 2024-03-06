from config import constants
from pathlib import Path
from cryptography.fernet import Fernet
import base64
import yaml

path_db_conf_key = Path(constants.CONF_LOCATION, constants.FN_DB_CONF_KEY)
path_db_conf_yaml = Path(constants.CONF_LOCATION, constants.FN_DB_CONF_YAML)
                        
key_bak = Path(path_db_conf_key.parent, path_db_conf_key.name + ".bak" + "1")
yaml_bak = Path(path_db_conf_yaml.parent, path_db_conf_yaml.name + ".bak" + "1")

if key_bak.exists() or yaml_bak.exists():
    key_bak_str = str(key_bak)
    yaml_bak_str = str(yaml_bak)
    num = int(key_bak_str[-1]) + 1
    while True:
        key_bak_str = key_bak_str[:-1] + str(num)
        yaml_bak_str = yaml_bak_str[:-1] + str(num)
        if not Path(key_bak_str).exists() and not Path(yaml_bak_str).exists():
            path_db_conf_key.rename(Path(key_bak_str))
            path_db_conf_yaml.rename(Path(yaml_bak_str))
            break
        num += 1
else:
    path_db_conf_key.rename(key_bak)
    path_db_conf_yaml.rename(yaml_bak)
    
        

# path_db_conf_key.rename()
# path_db_conf_yaml.rename()