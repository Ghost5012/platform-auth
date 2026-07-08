import os
from pydantic import ConfigDict
from typing import List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    """Application configuration settings."""

    APP_NAME: str = "My Application"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./test.db"
    REDIS_HOST: str = "localhost"
    CORS_ORIGINS: str = "*"
    ENVIRONMENT: str = "development"
    REDIS_PORT: int = 6379
    SECRET_KEY: str = "your-secret-key"

    @property
    def cors_origins_list(self) -> List[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        elif isinstance(self.CORS_ORIGINS, str):
            return self.CORS_ORIGINS.split(",")
        else:
            return self.CORS_ORIGINS

    model_config = ConfigDict(
        env_file=None,
        env_file_encoding='utf-8'
    )

def get_env_file() -> str:
    """
    Determines which .env file to load based on the ENVIRONMENT variable.

    This allows for different configurations for production, staging,
    development, and sandbox environments.

    Returns:
        The filename of the .env file to use.
    """
    # Read the 'ENVIRONMENT' variable, defaulting to 'development'.
    environment = os.getenv("ENVIRONMENT", "development")

    # Select the appropriate .env file based on the environment.
    if environment == 'production':
        return '.env.prod'
    elif environment == 'staging':
        return '.env.staging'
    elif environment == 'development':
        return '.env'
    
    # Default to staging if the environment is not recognized.
    return '.env.staging'


# Determine the correct .env file to load.
env_file_to_load = get_env_file()

# Load environment variables from the specified .env file.
# This will not override existing environment variables.
load_dotenv(dotenv_path=env_file_to_load)

# Create a single, globally accessible instance of the AppConfig.
# Pydantic will read the environment variables and populate the object.
app_config = AppConfig()
print(app_config.DATABASE_URL)