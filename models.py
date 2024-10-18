from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    note_value = Column(String, index=True)
    note_title = Column(String, index=True, nullable=True)
    date_created = Column(DateTime)