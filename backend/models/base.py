from sqlalchemy.ext.declarative import declarative_base
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
Base model for SQLAlchemy ORM.

The Base class serves as the foundation for all SQLAlchemy models.
It provides a common structure and allows the use of declarative syntax.
"""

# Base class for models
Base = declarative_base()
logger.info("SQLAlchemy base model initialized successfully.")
