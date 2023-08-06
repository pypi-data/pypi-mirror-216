from __future__ import annotations
import itertools
from decimal import Decimal


def make_scoring_configs(config_scoring) -> list[dict]:
    """combines every possible option defined in the config_scoring dictionary
    to create a number of scoring configurations that can be passed to the
    scoring functions.

    Args:
        config_scoring (dict): can be made by loading a valid toml file
        like so, toml.load(f"config_scoring.toml")

    Returns:
        list[dict]: list of scoring configurations
    """
    scoring_configs = []
    parameters = config_scoring.keys()

    for values in itertools.product(*config_scoring.values()):
        scoring_config = {}
        for param, value in zip(parameters, values):
            scoring_config[param] = Decimal(value)
        scoring_configs.append(scoring_config)

    return scoring_configs
