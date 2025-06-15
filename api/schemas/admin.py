from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



from pydantic import BaseModel, Field
from typing import Optional

class PromoteToTeacher(BaseModel):
    user_id: int
    qualifications: str
    university_id: int


class SubjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class LessonTypeCreate(BaseModel):
    name: str

class ClassroomCreate(BaseModel):
    type_lesson: int
    number: str
    capacity: Optional[int] = None
    has_projector: Optional[bool] = False
    university_id: int

class GroupCreate(BaseModel):
    name: str
    student_count: Optional[int] = None
    faculty: Optional[str] = None
    university_id: int

class UniversityCreate(BaseModel):
    name: str
    address: str | None = None
    phone: str | None = None
    email: str | None = None

from datetime import datetime

class ScheduleCreate(BaseModel):
    teacher_id: int
    subject_id: int
    classroom_id: int
    group_id: int
    type_id: int
    start_time: datetime
    end_time: datetime
    day_of_week: str
    university_id: int
