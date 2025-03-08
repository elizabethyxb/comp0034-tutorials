"""
Move this file to the flask_paralympics package for activity 7.3

The 'db' parameter is defined during activity 7.2.

Complete the code for the quiz tables at the end of the models.py file."""
from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from student.flask_paralympics import db


# Note: db.Model is the declarative base class for SQLAlchemy that was defined in the __init__.py file
class Event(db.Model):
    __tablename__ = 'event'
    event_id = mapped_column(Integer, primary_key=True)
    type = mapped_column(Text, nullable=False)
    year = mapped_column(Integer, nullable=False)
    start: Mapped[Optional[str]] = mapped_column(Text)  # Different syntax to show the difference
    end = mapped_column(Text)
    duration = mapped_column(Integer)
    countries = mapped_column(Integer)
    events = mapped_column(Integer)
    sports = mapped_column(Integer)
    highlights = mapped_column(Text)
    url = mapped_column(Text)

    # Relationships - one-to-many:
    host_events: Mapped[List["HostEvent"]] = relationship(back_populates="event", cascade="all, delete", passive_deletes=True)
    disability_events: Mapped[List["DisabilityEvent"]] = relationship(back_populates="event", cascade="all, delete", passive_deletes=True)
    medal_results: Mapped[List["MedalResult"]] = relationship(back_populates="event", cascade="all, delete", passive_deletes=True)
    question: Mapped[List["Question"]] = relationship(back_populates="event", cascade="all, delete", passive_deletes=True)
    # one-to-one relationship:
    participants: Mapped["Participants"] = relationship(back_populates="event", cascade="all, delete", passive_deletes=True)


class Country(db.Model):
    """
    Represents a country in the database.

    Attributes:
        code (str): Primary key for the country.
        name (str): Name of the country.
        region (str): Region of the country.
        sub_region (str): Sub-region of the country.
        member_type (str): Type of team.
        notes (str): Additional notes about the country.
    """
    __tablename__ = 'country'

    code = mapped_column(Text, primary_key=True)
    name = mapped_column(Text, nullable=False)
    region = mapped_column(Text)
    sub_region = mapped_column(Text)
    member_type = mapped_column(Text)
    notes = mapped_column(Text)
    # Relationships
    medal_results: Mapped[List["MedalResult"]] = relationship(back_populates="country", cascade="all, delete", passive_deletes=True)
    hosts: Mapped[List["Host"]] = relationship(back_populates="country", cascade="all, delete", passive_deletes=True)


class Disability(db.Model):
    __tablename__ = 'disability'

    disability_id = mapped_column(Integer, primary_key=True)
    category = mapped_column(Text, nullable=False)
    # Relationship to the DisabilityEvent table. back_populates takes the name of the relationship that is defined in the DisabilityClass
    disability_events: Mapped[List["DisabilityEvent"]] = relationship(back_populates="disability", cascade="all, delete", passive_deletes=True)


class DisabilityEvent(db.Model):
    __tablename__ = 'disability_event'

    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id', ondelete="CASCADE"), primary_key=True)
    disability_id: Mapped[int] = mapped_column(ForeignKey('disability.disability_id', ondelete="CASCADE"), primary_key=True)

    # Relationships to the parent classes: Event and Disability
    # back_populates takes the name of the relationships that is defined in the parent classes (same name was used in both)
    event: Mapped["Event"] = relationship("Event", back_populates="disability_events")
    disability: Mapped["Disability"] = relationship("Disability", back_populates="disability_events")


class Host(db.Model):
    __tablename__ = 'host'

    host_id = mapped_column(Integer, primary_key=True)
    country_code = mapped_column(ForeignKey('country.code', ondelete="CASCADE"))
    host = mapped_column(Text, nullable=False)

    # Relationships
    host_events: Mapped[List["HostEvent"]] = relationship(back_populates="host", cascade="all, delete", passive_deletes=True)
    country: Mapped["Country"] = relationship(back_populates="hosts")


class HostEvent(db.Model):
    __tablename__ = 'host_event'

    host_id = mapped_column(Integer,
                            ForeignKey('host.host_id', onupdate="CASCADE", ondelete="CASCADE"),
                            primary_key=True
                            )
    event_id = mapped_column(Integer,
                             ForeignKey('event.event_id', onupdate="CASCADE", ondelete="CASCADE"),
                             primary_key=True
                             )
    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="host_events")
    host: Mapped["Host"] = relationship("Host", back_populates="host_events")


class Participants(db.Model):
    __tablename__ = 'participants'

    participant_id = mapped_column(Integer, primary_key=True)
    event_id = mapped_column(Integer, ForeignKey('event.event_id', ondelete="CASCADE"))
    participants_m = mapped_column(Integer)
    participants_f = mapped_column(Integer)
    participants = mapped_column(Integer)

    # THis is a one-to-one relationship:
    event: Mapped["Event"] = relationship(back_populates="participants")


class MedalResult(db.Model):
    __tablename__ = 'medal_result'

    result_id = mapped_column(Integer, primary_key=True)
    event_id = mapped_column(Integer, ForeignKey('event.event_id', ondelete="CASCADE"))
    country_code = mapped_column(Text, ForeignKey('country.code', ondelete="CASCADE"))
    rank = mapped_column(Integer)
    gold = mapped_column(Integer)
    silver = mapped_column(Integer)
    bronze = mapped_column(Integer)
    total = mapped_column(Integer)
    # Relationships
    event: Mapped["Event"] = relationship(back_populates="medal_results")
    country: Mapped["Country"] = relationship(back_populates="medal_results")


class Quiz(db.Model):
    __tablename__ = 'quiz'

    quiz_id = mapped_column(Integer, primary_key=True)
    quiz_name = mapped_column(Text, nullable=False)
    date = mapped_column(Text)

    # Relationships
    quiz_questions: Mapped[List["QuizQuestion"]] = relationship(back_populates="quiz", cascade="all, delete")
    student_response: Mapped[List["StudentResponse"]] = relationship(back_populates="quiz", cascade="all, delete")

class Question(db.Model):
    __tablename__ = 'question'

    question_id = mapped_column(Integer, primary_key=True)
    question = mapped_column(Text, nullable=False)
    event_id = mapped_column(Integer, ForeignKey('event.event_id', ondelete="CASCADE"))

    # Relationships
    event: Mapped["Event"] = relationship(back_populates="question")
    answer_choice: Mapped[List["AnswerChoice"]] = relationship(back_populates="question", cascade="all, delete")
    quiz_questions: Mapped[List["QuizQuestion"]] = relationship(back_populates="question", cascade="all, delete")


class AnswerChoice(db.Model):
    __tablename__ = 'answer_choice'

    ac_id = mapped_column(Integer, primary_key=True)
    question_id = mapped_column(Integer, ForeignKey('question.question_id', ondelete="CASCADE"))
    choice_text = mapped_column(Text, nullable=False)
    choice_value = mapped_column(Integer)
    is_correct = mapped_column(Boolean)

    # Relationships
    question: Mapped["Question"] = relationship(back_populates="answer_choice")


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_question'

    quiz_id = mapped_column(Integer, ForeignKey('quiz.quiz_id', ondelete="CASCADE"), primary_key=True)
    question_id = mapped_column(Integer, ForeignKey('question.question_id', ondelete="CASCADE"), primary_key=True)

    # Relationships
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="quiz_questions", cascade="all, delete")
    question: Mapped["Question"] = relationship("Question", back_populates="quiz_questions", cascade="all, delete")

class StudentResponse(db.Model):
    __tablename__ = 'student_response'
    
    response_id = mapped_column(Integer, primary_key=True)
    student_email = mapped_column(Text, nullable=False)
    score = mapped_column(Integer)
    quiz_id = mapped_column(Integer, ForeignKey('quiz.quiz_id', ondelete="CASCADE"))

    # Relationships
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="student_response")

