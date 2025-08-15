# db.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Index
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///questions.db"  # файл БД в корне проекта

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    profession = Column(String(64), nullable=False)   # например: "Frontend Developer"
    question = Column(Text, nullable=False)
    # можем хранить оба варианта — plain и HTML
    answer_text = Column(Text, nullable=True)
    answer_html = Column(Text, nullable=True)

    __table_args__ = (
        Index("ix_questions_profession", "profession"),
        Index("ux_profession_question", "profession", "question", unique=True),
    )


def init_db():
    Base.metadata.create_all(bind=engine)
