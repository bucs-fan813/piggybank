import enum

class EXPORT_FORMAT(str, enum.Enum):
    """Enums for export formats
    """
    TEXT = "text"
    JSON = "json"
    TABLE = "table"
    CSV = "csv"