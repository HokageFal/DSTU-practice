from fastapi import status, APIRouter, Depends, HTTPException, Response, Request, UploadFile
from mypy.build import record_missing_stub_packages
from sqlalchemy import select, insert
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.users import user, user_login, user_response
from models import User
from database import SECRET_KEY, ALGORITHM, get_db
from datetime import datetime, timedelta
import jwt

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/add")
async def create_user(users: user, db: AsyncSession = Depends(get_db)):

    result = await db.scalars(select(User).filter(User.email == users.email))
    existing_user = result.first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким email уже существует")


    await db.execute(insert(User).values(
        first_name=users.first_name,
        last_name=users.last_name,
        email=users.email,
        password=bcrypt_context.hash(users.password),
    ))

    await db.commit()

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Ok"
    }

@router.post("/login")
async def user_login(users: user_login,response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.scalars(select(User).filter(User.email == users.email))
    user = result.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')

    if not bcrypt_context.verify(users.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    access_payload = {
        "id": user.id,
        "type": "access",
        "role": user.role,
        "iat": datetime.utcnow(),  # ✅ Указываем текущее время
        "exp": datetime.utcnow() + timedelta(minutes=59)  # ✅ Истекает через 59 минут
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

    refresh_payload = {
        "id": user.id,
        "type": "refresh",
        "role": user.role,
        "iat": datetime.utcnow(),  # ✅ Указываем текущее время
        "exp": datetime.utcnow() + timedelta(days=15)  # ✅ Истекает через 59 минут
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

    response.set_cookie(key="jwt", value=refresh_token, httponly=True, samesite="None")

    return {"access_token": access_token,
            "refresh_token": refresh_token}

@router.post("/access")
async def update_access(request: Request):
    data = await request.json()
    refresh = data.get("refresh_token")


    if not refresh:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='токен не найден')

    refresh_payload = jwt.decode(refresh, SECRET_KEY, algorithms=[ALGORITHM])

    access_payload = {
        "id": refresh_payload["id"],
        "type": "access",
        "role": refresh_payload["role"],
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=59),

    }

    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token
    }

@router.get("/view")
async def user_view(request: Request, db: AsyncSession = Depends(get_db)):
    access = request.headers.get("Authorization")

    if not access:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='токен не найден')

    if access.split()[0] != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат токена")

    token = access.split()[1]

    decode_access = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user = await db.scalars(select(User).filter(User.id == decode_access["id"]))

    result = user.first()

    return user_response.model_validate(result)

@router.post("/logout")
async def user_logout(response: Response):
    response.delete_cookie(key="jwt")
    return {"message": "Вы успешно вышли из аккаунта"}