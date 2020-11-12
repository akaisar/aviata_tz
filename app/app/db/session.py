from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core import config

engine = create_engine(config.DATABASE_URL, pool_pre_ping=True,
                       pool_size=30, max_overflow=0, pool_timeout=45)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
