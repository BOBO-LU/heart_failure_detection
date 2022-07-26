import os
import warnings
from pathlib import Path
import yaml
from ruamel.yaml import YAML
import pickle

def create_config_template():
    yaml_str = """\
# Experiment:
name:
date:
user:
project_path:
\n
# Environment:
time_format:
process_worker_num:
\n
# Folders:
raw_data_folder:
img_folder:
all_folder:
log_folder:
\n
# Preprocess:
data_length:
\n
# Heartpy:
ppg_sample_rate:
acc_sample_rate:
ma_window_size:
avg_window_size:
min_max_scaling_bound:
window_scaling_bound:
bandpass_cutoff_bound:
reject_bp_bound:
\n
# Model:
test_fraction:
validate_fraction:
epoch:
batch_size:
\n
    """
    
    ruamelFile = YAML()
    cfg_file = ruamelFile.load(yaml_str)
    return cfg_file, ruamelFile

    
def read_config(configname):
    """
    Reads structured config file
    """
    ruamelFile = YAML()
    path = Path(configname)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                cfg = ruamelFile.load(f)
                curr_dir = os.path.dirname(configname)
                if cfg["Project_path"] != curr_dir:
                    cfg["Project_path"] = curr_dir
                    write_config(configname, cfg)
        except Exception as err:
            if len(err.args) > 2:
                if (
                    err.args[2]
                    == "could not determine a constructor for the tag '!!python/tuple'"
                ):
                    with open(path, "r") as ymlfile:
                        cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
                        write_config(configname, cfg)
                else:
                    raise
    else:
        raise FileNotFoundError(
            "Config file is not found. Please make sure that the file exists and/or that you passed the path of the config file correctly!"
        )
    return cfg

def create_new_experiment(user, experiment, working_directory=None, copy=False):
    """
    TODO: copy directory
    TODO: reference data
    """
    from datetime import datetime as dt
    cfg_file, ruamelFile = create_config_template()

    months_3letter = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }
    date = dt.today()
    month = months_3letter[date.month]
    day = date.day
    d = str(month[0:3] + str(day))
    date = dt.today().strftime("%Y-%m-%d")
    if working_directory == None:
        working_directory = "."
    wd = Path(working_directory).resolve()
    project_name = "{user}-{exp}-{date}".format(user=user, exp=experiment, date=date)
    project_path = wd / project_name

    data_path = project_path / "data"
    model_path = project_path / "model"
    log_path = project_path / "log"
    plot_path = project_path / "plot"
    for p in [data_path, model_path, log_path, plot_path]:
        p.mkdir(parents=True)
    
    cfg_file, ruamelFile = create_config_template()
    cfg_file['name'] = experiment
    cfg_file['date'] = d
    cfg_file['user'] = user
    cfg_file['project_path'] = str(project_path)

    cfg_file['ppg_sample_rate'] = 64
    cfg_file['acc_sample_rate'] = 62.5
    cfg_file['ma_window_size'] = 3
    cfg_file['avg_window_size'] = 2
    cfg_file['min_max_scaling_bound'] = [0, 1]
    cfg_file['window_scaling_bound'] = [0, 1]
    cfg_file['bandpass_cutoff_bound'] = [0.7, 3.5]
    cfg_file['reject_bp_bound'] = [37, 180]

    projconfigfile = os.path.join(str(project_path), "config.yaml")
    write_config(projconfigfile, cfg_file)
    return projconfigfile

def write_config(configname, cfg):
    """
    Write structured config file.
    """
    with open(configname, "w") as cf:
        cfg_file, ruamelFile = create_config_template()
        for key in cfg.keys():
            cfg_file[key] = cfg[key]
        ruamelFile.dump(cfg_file, cf)

def edit_config(configname, edits, output_name=""):
    """
    Convenience function to edit and save a config file from a dictionary.
    Parameters
    ----------
    configname : string
        String containing the full path of the config file in the project.
    edits : dict
        Key–value pairs to edit in config
    output_name : string, optional (default='')
        Overwrite the original config.yaml by default.
        If passed in though, new filename of the edited config.
    Examples
    --------
    config_path = 'config.yaml'
    edits = {'numframes2pick': 5,
             'trainingFraction': [0.5, 0.8],
             'skeleton': [['a', 'b'], ['b', 'c']]}
    edit_config(config_path, edits)
    """
    cfg = read_plainconfig(configname)
    for key, value in edits.items():
        cfg[key] = value
    if not output_name:
        output_name = configname
    try:
        write_plainconfig(output_name, cfg)
    except ruamel.yaml.representer.RepresenterError:
        warnings.warn(
            "Some edits could not be written. "
            "The configuration file will be left unchanged."
        )
        for key in edits:
            cfg.pop(key)
        write_plainconfig(output_name, cfg)
    return cfg

def read_plainconfig(configname):
    if not os.path.exists(configname):
        raise FileNotFoundError(
            f"Config {configname} is not found. Please make sure that the file exists."
        )
    with open(configname) as file:
        return YAML().load(file)

def write_plainconfig(configname, cfg):
    with open(configname, "w") as file:
        YAML().dump(cfg, file)