from sqlalchemy import Column, Integer, String
from database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    education = Column(String, nullable=True)
    college = Column(String, nullable=True)
    degree = Column(String, nullable=True)
    graduation_year = Column(Integer, nullable=True)
    career_goal = Column(String, nullable=True)
    resume_text = Column(String, nullable=True)