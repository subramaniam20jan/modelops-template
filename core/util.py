import yaml


def load_config(config_file: str, source: str, grid_index=-1):
    with open(config_file, "r") as file:
        loaded_config = yaml.safe_load(file)

    config_subset = loaded_config[source]

    if grid_index == -1:
        if "final" in config_subset:
            config_to_return = config_subset["final"]
        else:
            config_to_return = config_subset
    else:
        config_to_return = config_subset["grid"][grid_index]

    return config_to_return
