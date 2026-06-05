from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.engine import row
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

engine = create_engine("sqlite:///instance/database.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
#MAIN
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

#APPEARANCES
@app.get("/appearances")
async def get_appearances(request: Request, page: int = 1, db: Session = Depends(get_db)):
    offset = (page - 1) * 50
    result = db.execute(text(f"SELECT * FROM appearances LIMIT 50 OFFSET {offset}")).fetchall()
    if result:
        appearances_list = [row._mapping for row in result]
    else:
        appearances_list = []
    return templates.TemplateResponse(request=request, name="appearances.html", context={"appearances": appearances_list, "current_page": page, "search_query": None})

@app.get("/get_appearance")
async def get_appearance_player(appearance_player_name: str, request: Request, db: Session = Depends(get_db)):
    result = db.execute(text(f"SELECT p.*, a.*, g.* FROM appearances a JOIN players p ON a.player_id = p.player_id JOIN games g ON a.game_id = g.game_id WHERE p.name LIKE :player_name ORDER BY a.date DESC LIMIT 20"), {"player_name": f"%{appearance_player_name}%"}).fetchall()
    if result:
        appearances_list = [row._mapping for row in result]
    else:
        appearances_list = []
    return templates.TemplateResponse(request=request, name="appearances.html", context={"appearances": appearances_list, "current_page": 1, "search_query": None})

#CLUBS
@app.get("/clubs")
async def get_clubs(request: Request, page: int = 1, db:Session = Depends(get_db)):
    offset = (page - 1) * 50
    result = db.execute(text(f"SELECT * FROM clubs LIMIT 50 OFFSET {offset}")).fetchall()
    if result:
        clubs_list = [row._mapping for row in result]
    else:
        clubs_list = []
    return templates.TemplateResponse(request=request, name="clubs.html", context={"clubs": clubs_list, "current_page": page, "search_query": None})

@app.get("/get_club")
async def get_club(club_name: str, request: Request, db: Session = Depends(get_db)):
    result = db.execute(text(f"SELECT * FROM clubs WHERE name LIKE :name"), {"name": f"%{club_name}%"}).fetchone()
    if result:
        clubs_list = [result._mapping]
    else:
        clubs_list = []
    return templates.TemplateResponse(request=request, name="clubs.html", context={"clubs": clubs_list, "current_page": 1, "search_query": None})

#GAMES
@app.get("/games")
async def get_games(request: Request, page: int = 1,db: Session = Depends(get_db)):
    offset = (page - 1) * 50
    result = db.execute(text(f"SELECT * FROM games LIMIT 50 OFFSET {offset}")).fetchall()
    if result:
        games_list = [row._mapping for row in result]
    else:
        games_list = []
    return templates.TemplateResponse(request=request, name="games.html", context={"games": games_list, "current_page": page, "search_query": None})

@app.get("/get_game")
async def get_club_games(game_club_name: str, request: Request, db: Session = Depends(get_db)):
    result = db.execute(text(f"SELECT g.* FROM games g JOIN clubs c ON g.home_club_id = c.club_id OR g.away_club_id = c.club_id WHERE c.name LIKE :name ORDER BY g.date DESC LIMIT 20"), {"name": f"%{game_club_name}%"}).fetchall()
    if result:
        games_list = [row._mapping for row in result]
    else:
        games_list = []
    return templates.TemplateResponse(request=request, name="games.html", context={"games": games_list, "current_page": 1, "search_query": None})

#NATIONAL_TEAMS
@app.get("/national_teams")
async def get_national_teams(request: Request, page: int = 1,db: Session = Depends(get_db)):
    offset = (page - 1) * 50
    result = db.execute(text(f"SELECT * FROM national_teams LIMIT 50 OFFSET {offset}")).fetchall()
    if result:
        national_teams_list = [row._mapping for row in result]
    else:
        national_teams_list = []
    return templates.TemplateResponse(request=request, name="national_teams.html", context={"national_teams": national_teams_list, "current_page": page, "search_query": None})

@app.get("/get_national_team")
async def get_national_team(national_team_name: str, request: Request, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM national_teams WHERE name LIKE :national_team_name"), {"national_team_name": national_team_name}).fetchone()
    if result:
        national_teams_list = [result._mapping]
    else:
        national_teams_list = []
    return templates.TemplateResponse(request=request, name="national_teams.html", context={"national_teams": national_teams_list, "current_page": 1, "search_query": None})

#PLAYERS
@app.get("/players")
async def get_players(request: Request, page: int = 1,db: Session = Depends(get_db)):
    offset = (page - 1) * 50
    result = db.execute(text(f"SELECT * FROM players LIMIT 50 OFFSET {offset}")).fetchall()
    if result:
        players_list = [row._mapping for row in result]
    else:
        players_list = []
    return templates.TemplateResponse(request=request, name="players.html",context= {"players": players_list, "current_page": page, "search_query": None})

@app.get("/get_player")
async def get_player(player_name: str, request: Request, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM players WHERE name LIKE :player_name"), {"player_name" : f"%{player_name}%"}).fetchone()
    if result:
        players_list = [result._mapping]
    else:
        players_list = []
    return templates.TemplateResponse(request=request, name="players.html", context={"players": players_list, "current_page": 1, "search_query": player_name})

#TRANSFERS
@app.get("/transfers")
async def get_transfers(request: Request, page: int = 1,db: Session = Depends(get_db)):
    offset = (page - 1) * 50
    result = db.execute(text(f"SELECT * FROM transfers LIMIT 50 OFFSET {offset}")).fetchall()
    if result:
        transfers_list = [row._mapping for row in result]
    else:
        transfers_list = []
    return templates.TemplateResponse(request=request, name="transfers.html", context={"transfers": transfers_list, "current_page": page, "search_query": None})

@app.get("/transfers/top_10")
async def get_top_10_transfers(request: Request, db: Session = Depends(get_db)):
    result = db.execute(text(f"SELECT * FROM transfers ORDER BY transfer_fee DESC LIMIT 10")).fetchall()
    if result:
        transfers_list = [row._mapping for row in result]
    else:
        transfers_list = []
    return templates.TemplateResponse(request=request, name="transfers.html", context={"transfers": transfers_list, "current_page": 1, "search_query": None})

@app.get("/get_transfer")
async def get_transfer_player(transfer_player_name: str, request: Request, db: Session = Depends(get_db)):
    result = db.execute(text(f"SELECT * FROM transfers WHERE player_name LIKE :name "), {"name" : f"%{transfer_player_name}%"}).fetchone()
    if result:
        transfers_list = [result._mapping]
    else:
        transfers_list = []
    return templates.TemplateResponse(request=request, name="transfers.html", context={"transfers": transfers_list, "current_page": 1, "search_query": None})