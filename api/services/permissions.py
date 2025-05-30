from fastapi import HTTPException, Request, status
import jwt
from database import SECRET_KEY, ALGORITHM

async def is_autorization(request: Request):
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Токен не найден")

    if not token.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверный формат токена")

    token = token.split()[1]

    try:
        decode_access = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Токен истёк")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверный токен")

    return decode_access  # Возвращаем данные из токена, чтобы использовать в других функциях


async def is_admin(request: Request):
    user_data = is_autorization(request)  # Получаем данные из токена

    if "role" not in user_data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")

    if not user_data["is_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Только администраторы могут выполнять это действие")

    return True  # Пользователь администратор, разрешаем доступ
