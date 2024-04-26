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
current_quest = None


@router.get("/", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/{name}/", response_class=HTMLResponse)
async def get_members(request: Request, name: str):
    current_game = game.Game()
    global current_quest
    if not current_game.is_extra_life_activated and not current_quest or current_game.round == 0 or current_quest[
        6] != current_game.round + 1:
        current_quest = await current_game.get_question()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "question": current_quest[0],
        "is_divide": current_game.help_divide,
        "is_change": current_game.help_change,
        "is_extra_life": current_game.help_extra_live,
        "is_friend": current_game.help_friend,
        "is_audience": current_game.help_audience,
        "is_shown1": True,
        "is_shown2": True,
        "is_shown3": True,
        "is_shown4": True,
        "ans1": current_quest[1],
        "ans2": current_quest[2],
        "ans3": current_quest[3],
        "ans4": current_quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10),
        "is_chart": False,
        "is_start": True
    })


@router.post("/{name}/{hints}/divide/")
async def divide(request: Request, name: str, hints: str):
    global current_quest
    if not current_game.is_extra_life_activated and not current_quest or current_game.round == 0 or current_quest[
        6] != current_game.round + 1:
        current_quest = await current_game.get_question()
    show1 = True
    show2 = True
    show3 = True
    show4 = True
    if current_game.help_divide:  # choose two random wrong answers to delete
        current_game.help_divide = False
        right = set()
        right.add(current_quest[5])
        variants = set()
        for i in [1, 2, 3, 4]:
            variants.add(i)

        variants -= right  # delete right question
        extra = set()
        extra.add(random.choice(list(variants)))
        variants -= extra  # delete random wrong answer

        show1 = 1 not in variants
        show2 = 2 not in variants
        show3 = 3 not in variants
        show4 = 4 not in variants

    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "hints": hints,
        "question": current_quest[0],
        "is_divide": current_game.help_divide and "1" in hints,
        "is_change": current_game.help_change and "2" in hints,
        "is_extra_life": current_game.help_extra_live and "3" in hints,
        "is_friend": current_game.help_friend and "4" in hints,
        "is_audience": current_game.help_audience and "5" in hints,
        "is_shown1": show1,
        "is_shown2": show2,
        "is_shown3": show3,
        "is_shown4": show4,
        "ans1": current_quest[1],
        "ans2": current_quest[2],
        "ans3": current_quest[3],
        "ans4": current_quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10),
        "is_chart": False,
        "is_start": False
    })


@router.post("/{name}/{hints}/change/")
async def change(request: Request, name: str, hints: str):
    global current_quest
    if current_game.help_change:
        current_game.help_change = False
        current_quest = await current_game.get_question()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "hints": hints,
        "question": current_quest[0],
        "is_divide": current_game.help_divide and "1" in hints,
        "is_change": current_game.help_change and "2" in hints,
        "is_extra_life": current_game.help_extra_live and "3" in hints,
        "is_friend": current_game.help_friend and "4" in hints,
        "is_audience": current_game.help_audience and "5" in hints,
        "is_shown1": True,
        "is_shown2": True,
        "is_shown3": True,
        "is_shown4": True,
        "ans1": current_quest[1],
        "ans2": current_quest[2],
        "ans3": current_quest[3],
        "ans4": current_quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10),
        "is_chart": False,
        "is_start": False
    })


@router.post("/{name}/{hints}/extra_life/")
async def extra_life(request: Request, name: str, hints: str):
    global current_quest
    if current_game.help_extra_live:
        current_game.help_extra_live = False
        current_game.is_extra_life_activated = True

    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "hints": hints,
        "question": current_quest[0],
        "is_divide": current_game.help_divide and "1" in hints,
        "is_change": current_game.help_change and "2" in hints,
        "is_extra_life": current_game.help_extra_live and "3" in hints,
        "is_friend": current_game.help_friend and "4" in hints,
        "is_audience": current_game.help_audience and "5" in hints,
        "is_shown1": True,
        "is_shown2": True,
        "is_shown3": True,
        "is_shown4": True,
        "ans1": current_quest[1],
        "ans2": current_quest[2],
        "ans3": current_quest[3],
        "ans4": current_quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10),
        "is_chart": False,
        "is_start": False
    })


@router.get("/{name}/{hints}/friend/")
async def friend(request: Request, name: str, hints: str):
    global current_quest
    if current_game.help_friend:
        current_game.help_friend = False
        current_game._round += 1
        current_quest = await current_game.get_question()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "hints": hints,
        "question": current_quest[0],
        "is_divide": current_game.help_divide and "1" in hints,
        "is_change": current_game.help_change and "2" in hints,
        "is_extra_life": current_game.help_extra_live and "3" in hints,
        "is_friend": current_game.help_friend and "4" in hints,
        "is_audience": current_game.help_audience and "5" in hints,
        "is_shown1": True,
        "is_shown2": True,
        "is_shown3": True,
        "is_shown4": True,
        "ans1": current_quest[1],
        "ans2": current_quest[2],
        "ans3": current_quest[3],
        "ans4": current_quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10),
        "is_chart": False,
        "is_start": False
    })


@router.post("/{name}/{hints}/audience/")
async def audience(request: Request, name: str, hints: str):
    global current_quest
    if current_game.help_audience and current_quest:
        game.Game.get_chart(int(current_quest[5]))
        current_game.help_audience = False

    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "hints": hints,
        "question": current_quest[0],
        "is_divide": current_game.help_divide and "1" in hints,
        "is_change": current_game.help_change and "2" in hints,
        "is_extra_life": current_game.help_extra_live and "3" in hints,
        "is_friend": current_game.help_friend and "4" in hints,
        "is_audience": current_game.help_audience and "5" in hints,
        "is_shown1": True,
        "is_shown2": True,
        "is_shown3": True,
        "is_shown4": True,
        "ans1": current_quest[1],
        "ans2": current_quest[2],
        "ans3": current_quest[3],
        "ans4": current_quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10),
        "is_chart": True,
        "is_start": False
    })


@router.get("/{name}/{hints}/{answer}/")
async def choose_answer(request: Request, name: str, hints: str, answer: str):
    global current_quest
    is_skipped = await current_game.give_answer(name, int(answer))
    if (not is_skipped) and (
            not current_quest or current_game.round == 0 or current_quest[6] != current_game.round + 1):
        current_quest = await current_game.get_question()

    show1 = True
    show2 = True
    show3 = True
    show4 = True
    if is_skipped:
        show1 = 1 != int(answer)
        show2 = 2 != int(answer)
        show3 = 3 != int(answer)
        show4 = 4 != int(answer)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": name,
        "hints": hints,
        "question": current_quest[0],
        "is_divide": current_game.help_divide and "1" in hints,
        "is_change": current_game.help_change and "2" in hints,
        "is_extra_life": current_game.help_extra_live and "3" in hints,
        "is_friend": current_game.help_friend and "4" in hints,
        "is_audience": current_game.help_audience and "5" in hints,
        "is_shown1": show1,
        "is_shown2": show2,
        "is_shown3": show3,
        "is_shown4": show4,
        "ans1": current_quest[1],
        "ans2": current_quest[2],
        "ans3": current_quest[3],
        "ans4": current_quest[4],
        "awards": list(reversed(game.win_amounts)),
        "award": game.win_amounts[current_game.round],
        "records": await game.Game.get_records(10),
        "is_chart": False,
        "is_start": False
    })


@router.get("/favicon.ico")
async def get_favicon():
    pass
