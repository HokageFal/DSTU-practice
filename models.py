from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default="student") # Роль: admin/teacher/student


class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)  # Связь с User
    name = Column(String(100), nullable=False)
    qualifications = Column(String(200))

    user = relationship("User")
    schedules = relationship("Schedule", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))


class Classroom(Base):
    __tablename__ = "classroom"
    id = Column(Integer, primary_key=True)
    type_lesson = Column(Integer, ForeignKey("lesson_type.id"), unique=True)
    number = Column(String(10), unique=True, nullable=False)
    capacity = Column(Integer)
    has_projector = Column(Boolean, default=False)


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    student_count = Column(Integer)
    faculty = Column(String(50))


class LessonType(Base):
    __tablename__ = "lesson_type"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)  # "lecture", "seminar", "lab"


class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    classroom_id = Column(Integer, ForeignKey("classroom.id"))
    group_id = Column(Integer, ForeignKey("group.id"))
    type_id = Column(Integer, ForeignKey("lesson_type.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    day_of_week = Column(String(10), nullable=False)  # "Monday", "Tuesday"...

    teacher = relationship("Teacher", back_populates="schedules")
    subject = relationship("Subject")
    classroom = relationship("Classroom")
    group = relationship("Group")
    lesson_type = relationship("LessonType")