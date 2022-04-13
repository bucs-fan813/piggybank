import enum


class EXPORT_FORMAT(str, enum.Enum):
    """Enums for export formats
    """
    TEXT = "text"
    JSON = "json"
    TABLE = "table"
    CSV = "csv"


class EXPORT_PERIOD(str, enum.Enum):
    """Enums for import providers
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
