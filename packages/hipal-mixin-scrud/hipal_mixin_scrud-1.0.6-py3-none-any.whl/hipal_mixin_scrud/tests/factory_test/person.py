# lib
from pydantic import BaseModel
from faker import Faker
import factory
import random

# sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy import String

Base = declarative_base()

fake = Faker()


class PersonModel(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_1 = Column(String)
    name_2 = Column(String)
    last_name_1 = Column(String)
    last_name_2 = Column(String)
    rh = Column(String)


class PersonFactory(factory.Factory):
    class Meta:
        model = PersonModel

    id = random.randint(1, 100)
    name_1 = fake.name()
    name_2 = fake.name()
    last_name_1 = fake.name()
    last_name_2 = fake.name()
    rh = fake.name()

    
class PersonSchema(BaseModel):
    id: int
    name_1: str
    name_2: str
    last_name_1: str
    last_name_2: str
    rh: str
    
    class Config:
        orm_mode = True