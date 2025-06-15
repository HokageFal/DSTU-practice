from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import University, Classroom, Teacher, Group, Schedule
from typing import List

router = APIRouter(
    prefix="/public",
    tags=["Public Info"]
)

@router.get("/universities/")
async def get_universities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(University))
    return result.scalars().all()

@router.get("/universities/{university_id}")
async def get_university_by_id(university_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(University).where(University.id == university_id))
    university = result.scalar_one_or_none()
    if not university:
        raise HTTPException(status_code=404, detail="Университет не найден")
    return university

@router.get("/universities/{university_id}/classrooms/")
async def get_classrooms_by_university(university_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Classroom).where(Classroom.university_id == university_id)
    )
    return result.scalars().all()

@router.get("/universities/{university_id}/teachers/")
async def get_teachers_by_university(university_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Teacher).where(Teacher.university_id == university_id)
    )
    return result.scalars().all()

@router.get("/universities/{university_id}/groups/")
async def get_groups_by_university(university_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Group).where(Group.university_id == university_id)
    )
    return result.scalars().all()

@router.get("/universities/{university_id}/schedules/")
async def get_schedules_by_university(university_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Schedule).where(Schedule.university_id == university_id)
    )
    return result.scalars().all()

@router.get("/classrooms/{classroom_id}/schedules/")
async def get_schedules_by_classroom(classroom_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Schedule).where(Schedule.classroom_id == classroom_id)
    )
    return result.scalars().all()

@router.get("/teachers/{teacher_id}/schedules/")
async def get_schedules_by_teacher(teacher_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Schedule).where(Schedule.teacher_id == teacher_id)
    )
    return result.scalars().all()

@router.get("/groups/{group_id}/schedules/")
async def get_schedules_by_group(group_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Schedule).where(Schedule.group_id == group_id)
    )
    return result.scalars().all()