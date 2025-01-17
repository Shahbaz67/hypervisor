from enum import Enum

class Role(str, Enum):
    ADMIN = "Admin"
    DEVELOPER = "Developer"
    VIEWER = "Viewer"
