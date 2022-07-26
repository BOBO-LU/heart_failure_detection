import configparser
import os

PROJECT_LOCATION = os.environ['PROJECT_LOCATION']
PROJECT_PROFILE = os.environ['PROJECT_PROFILE']
CONFIG_LOCATION = os.path.join(PROJECT_LOCATION, 'config.ini')
DATA_LOCATION = os.path.join(PROJECT_LOCATION, 'data')
PARAMETER_LOCATION = os.path.join(PROJECT_LOCATION, 'parameters.yaml')

def get_env_config():
    env_config = configparser.ConfigParser()
    env_config.read(CONFIG_LOCATION)
    print("Using profile: ", PROJECT_PROFILE)
    return env_config[PROJECT_PROFILE]

def setup_env_config():
    env_config = configparser.ConfigParser()
    env_config.read(CONFIG_LOCATION)
    try:
        env_config[PROJECT_PROFILE]
    except:
        print("Project profile doesn't exist, add profile")

        env_config.add_section(PROJECT_PROFILE)
        env_config.set(PROJECT_PROFILE, 'ROOT_FOLDER', PROJECT_LOCATION)
        env_config.set(PROJECT_PROFILE, 'RAW_DATA_FOLDER', DATA_LOCATION)
        env_config.set(PROJECT_PROFILE, 'CONFIG_LOCATION', CONFIG_LOCATION)
        env_config.set(PROJECT_PROFILE, 'PARAMETER_LOCATION', PARAMETER_LOCATION)
        env_config.set(PROJECT_PROFILE, 'PROJECT_PROFILE', PROJECT_PROFILE)

        with open(CONFIG_LOCATION, 'w') as configfile:    # save
            env_config.write(configfile)

        env_config = configparser.ConfigParser()
        env_config.read(CONFIG_LOCATION)

    print("Please change the raw_data_folder in config.ini")
    return env_config[PROJECT_PROFILE]



    # RAW_DATA_FOLDER = env_config[ENV_LOCATION]['RAW_DATA_FOLDER']
    # EXP_NAME = env_config['DEFAULT']['EXP_NAME']
    # IMG_FOLDER = "./hp_csv/" + EXP_NAME
    # ALL_FOLDER = "./hp_all/" + EXP_NAME
    # TIME_FORMAT = env_config['Others']['TIME_FORMAT']

        

if __name__ == "__main__":
    setup_env_config()