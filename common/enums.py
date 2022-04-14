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
    USAA_V1 = "bank"
    USAA_V2 = "bank"
    GA_SOUTH_V1 = "gas"
    JACKSON_EMC_V1 = "electricity"
