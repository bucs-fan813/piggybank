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
    Y2020 = "CrawfordTech"
    Y2021 = "iText"
