import asyncio
import sys
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from models import metadata
from db_config import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    try:
        # Create the engine and tables
        engine = create_async_engine(
            DATABASE_URL,
            echo=True,
            pool_pre_ping=True,
            connect_args={"timeout": 30, "command_timeout": 30}
        )
        
        logger.info("Attempting to connect to the database...")
        async with engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
        logger.info("Tables created successfully!")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        logger.error("Possible issues:")
        logger.error("1. Database server is running and accessible")
        logger.error("2. Database credentials are correct")
        logger.error("3. Network connection is stable")
        logger.error("4. Firewall settings allow the connection")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(init_db())
