from enum import Enum


class MissingDataOptions(str, Enum):
    descard = "descard"
    avergae_imputation = "avergae_imputation"