import enum


class EXPORT_FORMAT(str, enum.Enum):
    """Enums for export formats
    """
    TEXT = "text"
    JSON = "json"
    TABLE = "table"
    SPREADSHEET = "spreadsheet"


class EXPORT_PERIOD(int, enum.Enum):
    """Enums for export periods
    """
    MONTHLY = 1
    YEARLY = 2
    STATEMENT = 3
    ALL = 4


class IMPORT_PROVIDER(str, enum.Enum):
    """Enums for import providers
    """
    USAA_V1 = "CrawfordTech"
    USAA_V2 = "iText"
    GA_SOUTH_V1 = "Compart"
