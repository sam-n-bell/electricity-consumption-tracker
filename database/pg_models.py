# from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

PG_BASE = declarative_base()

"""
Sample test db model
"""
# class Test(PG_BASE):
#     __tablename__ = "test"
#
#     id = Column(Integer, primary_key=True, index=True)
#     text = Column(String)
