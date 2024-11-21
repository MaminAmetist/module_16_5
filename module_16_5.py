# Шаблонизатор Jinja 2
# Задача "Список пользователей в шаблоне":
from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get(path="/get/user/{user_id}")
async def get_all_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id - 1]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.get("/")
def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.post('/post/{username}/{age}')
async def create_user(username: str, age: int) -> User:
    user_id = len(users) + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/put/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> List[User]:
    try:
        edit_user = users[user_id - 1]
        edit_user.username = username
        edit_user.age = age
        return users
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/del/user/{user_id}')
async def delete_user(user_id: int) -> List[User]:
    try:
        del_user = users[user_id - 1]
        if del_user.id == user_id:
            users.remove(del_user)
            return users
        else:
            raise HTTPException(status_code=404, detail='User was not found')
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')
        
