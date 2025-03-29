from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

app = FastAPI()
security = HTTPBasic()

# Предположим, у нас есть простая база пользователей
fake_users_db = {
    "user1": "password1",
    "user2": "password2"
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """Проверка правильности учетных данных"""
    correct_username = fake_users_db.get(credentials.username)
    if correct_username is None or correct_username != credentials.password:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Basic"})
    return credentials.username

@app.get("/login")
async def login(username: str = Depends(authenticate)):
    """Защищенная конечная точка, доступная только для авторизованных пользователей"""
    return {"message": "You got my secret, welcome"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
