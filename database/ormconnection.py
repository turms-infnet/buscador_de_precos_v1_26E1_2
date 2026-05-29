from sqlalchemy import create_engine, String, Table, Column, ForeignKey, Float, DateTime, func, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapper, mapped_column, relationship, Mapped

def get_engine():
    engine = create_engine('sqlite:///banco-orm.db')
    return engine

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session