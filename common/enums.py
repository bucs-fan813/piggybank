from enum import Enum


class EXPORT_FORMAT(str, Enum):
    """Enums for export formats
    """
    TEXT = "text"
    JSON = "json"
    TABLE = "table"
    SPREADSHEET = "spreadsheet"


class EXPORT_PERIOD(int, Enum):
    """Enums for export periods
    """
    MONTHLY = 1
    YEARLY = 2
    STATEMENT = 3
    ALL = 4


class IMPORT_PROVIDER(str, Enum):
    """Enums for import providers
    """
    USAA_V1 = 1
    USAA_V2 = 2
    GA_SOUTH_V1 = 3
    JACKSON_EMC_V1 = 4
    WATER_V1 = 5
    CHASE_V1 = 6
