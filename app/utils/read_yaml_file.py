import yaml
import os

def yaml_to_dict():
    """
    Parses yaml file into dict
    :param path_to_file: PAth of file
    :return: dict
    """

    path_to_file =  os.path.join(os.path.dirname(__file__), 
                                 "..","config.yaml" )
    with open(path_to_file) as file:
        config = yaml.safe_load(file)
    return config