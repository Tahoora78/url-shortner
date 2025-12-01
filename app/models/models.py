from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime
from sqlalchemy import event, insert

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    visit_count = Column(Integer, default=0)


class Key(Base):
    __tablename__ = "keys"
    value = Column(String(7), primary_key=True)

class Counter(Base):
    __tablename__ = "counter"
    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)

@event.listens_for(Counter.__table__, "after_create")
def insert_initial_counter(target, connection, **kw):
    connection.execute(
        insert(Counter).values(id=1, value=0)
    )