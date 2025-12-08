"""Minimal config for uMap Data API.

This avoids pulling pydantic-settings for simple usage in this project.
"""

class Settings:
    def __init__(self):
        self.app_name = "uMap Data API"


settings = Settings()
