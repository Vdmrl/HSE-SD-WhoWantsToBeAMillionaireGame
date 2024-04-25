import random

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from services import game

router = APIRouter(
    prefix="",
    tags=["game"]
)

templates = Jinja2Templates(directory="templates")
current_game = game.Game()


@router.get("/", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/{name}/", response_class=HTMLResponse)
async def get_members(request: Request, name: str):
    current_game = game.Game()
    quest = await current_game.get_question()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "question": quest[0],
        "is_divide": current_game.help_divide,
        "is_shown1": True,
        "is_shown2": True,
        "is_shown3": True,
        "is_shown4": True,
        "ans1": quest[1],
        "ans2": quest[2],
        "ans3": quest[3],
        "ans4": quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10)
    })

@router.post("/{name}/divide/")
async def divide(request: Request, name: str):
    quest = await current_game.get_question()
    show1 = True
    show2 = True
    show3 = True
    show4 = True
    if current_game.help_divide: # choose two random wrong answers to delete
        current_game.help_divide = False
        right = set()
        right.add(quest[5])
        variants = set()
        for i in [1,2,3,4]:
            variants.add(i)

        variants -= right # delete right question
        extra = set()
        extra.add(random.choice(list(variants)))
        variants -= extra # delete random wrong answer

        show1 = 1 not in variants
        show2 = 2 not in variants
        show3 = 3 not in variants
        show4 = 4 not in variants

    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "question": quest[0],
        "is_divide": current_game.help_divide,
        "is_shown1": show1,
        "is_shown2": show2,
        "is_shown3": show3,
        "is_shown4": show4,
        "ans1": quest[1],
        "ans2": quest[2],
        "ans3": quest[3],
        "ans4": quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10)
    })


@router.post("/{name}/{answer}/")
async def choose_answer(request: Request, name: str, answer: str):
    await current_game.give_answer(name, int(answer))
    quest = await current_game.get_question()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "question": quest[0],
        "is_divide": current_game.help_divide,
        "is_shown1": True,
        "is_shown2": True,
        "is_shown3": True,
        "is_shown4": True,
        "ans1": quest[1],
        "ans2": quest[2],
        "ans3": quest[3],
        "ans4": quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10)
    })


@router.get("/favicon.ico")
async def get_favicon():
    pass
