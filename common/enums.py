import enum

class EXPORT_FORMAT(str, enum.Enum):
    """Enums for export formats
    """
    TEXT = "text"
    JSON = "json"
    TABLE = "table"
    CSV = "csv"

class IMPORT_PROVIDER(str, enum.Enum):
    """Enums for export formats
    """
    Y2020 = "CrawfordTech"
    Y2021 = "iText"
