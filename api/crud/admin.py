from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from database import get_db
from models import Subject, LessonType, Classroom, Group, User, Teacher, UserRole, University, Schedule
from typing import List
from api.schemas.admin import (SubjectCreate, LessonTypeCreate,
                               ClassroomCreate, GroupCreate,
                               PromoteToTeacher, UniversityCreate, ScheduleCreate)
from api.services.permissions import is_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin CRUD"]
)

@router.post("/add/subjects/")
async def add_subject(subject: SubjectCreate,
                      request: Request,
                      db: AsyncSession = Depends(get_db),
                      _=Depends(is_admin)):
    stmt = insert(Subject).values(**subject.dict())
    await db.execute(stmt)
    await db.commit()
    return {"message": "Предмет добавлен"}


@router.post("/add/lesson-types/")
async def add_lesson_type(lesson_type: LessonTypeCreate,
                          request: Request,
                          db: AsyncSession = Depends(get_db),
                          _=Depends(is_admin)):
    stmt = insert(LessonType).values(**lesson_type.dict())
    await db.execute(stmt)
    await db.commit()
    return {"message": "Тип занятия добавлен"}


@router.post("/add/classrooms/")
async def add_classroom(classroom: ClassroomCreate,
                        request: Request,
                        db: AsyncSession = Depends(get_db),
                        _=Depends(is_admin)):
    stmt = insert(Classroom).values(**classroom.dict())
    await db.execute(stmt)
    await db.commit()
    return {"message": "Аудитория добавлена"}


@router.post("/add/groups/")
async def add_group(group: GroupCreate,
                    request: Request,
                    db: AsyncSession = Depends(get_db),
                    _=Depends(is_admin)):
    stmt = insert(Group).values(**group.dict())
    await db.execute(stmt)
    await db.commit()
    return {"message": "Группа добавлена"}


@router.post("/promote-to-teacher/")
async def promote_to_teacher(data: PromoteToTeacher,
                             request: Request,
                             db: AsyncSession = Depends(get_db),
                             _=Depends(is_admin)):

    # Проверяем, существует ли пользователь
    result = await db.execute(select(User).where(User.id == data.user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user.role != UserRole.STUDENT:
        raise HTTPException(status_code=400, detail="Пользователь не является студентом")

    # Проверяем, не создан ли уже Teacher-профиль
    teacher_result = await db.execute(select(Teacher).where(Teacher.user_id == data.user_id))
    if teacher_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Этот пользователь уже учитель")

    # Обновляем роль пользователя
    await db.execute(
        update(User).where(User.id == data.user_id).values(role=UserRole.TEACHER)
    )

    # Создаем профиль учителя
    full_name = f"{user.first_name} {user.last_name}"
    new_teacher = Teacher(user_id=data.user_id, name=full_name,
                          qualifications=data.qualifications, university_id=data.university_id)
    db.add(new_teacher)

    await db.commit()

    return {"message": f"Пользователь {user.email} повышен до учителя"}

@router.post("/add/university/")
async def add_university(university: UniversityCreate,
                         request: Request,
                         db: AsyncSession = Depends(get_db),
                         _=Depends(is_admin)):
    stmt = insert(University).values(**university.dict())
    await db.execute(stmt)
    await db.commit()
    return {"message": "Университет добавлен"}

@router.post("/add/schedule/")
async def add_schedule(schedule: ScheduleCreate,
                       request: Request,
                       db: AsyncSession = Depends(get_db),
                       _=Depends(is_admin)):
    stmt = insert(Schedule).values(**schedule.dict())
    await db.execute(stmt)
    await db.commit()
    return {"message": "Расписание добавлено"}