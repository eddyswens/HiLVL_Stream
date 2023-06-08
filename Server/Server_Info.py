from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RoleData:
    current_cargo_color: List[int]
    current_conditions: int
    is_cargo: bool


@dataclass
class Player:
    balls: int
    bullet: int
    color_cargo: List[int]
    current_color: List[int]
    current_pos: List[float]
    is_blocking: bool
    is_cargo: bool
    is_connected: bool
    is_shooting: bool
    name_object_controll: str
    name_player: str
    name_role: str
    repair: bool


@dataclass
class TeamInfo:
    balls_team: int
    name_team: str
    players: Dict[str, Player]


@dataclass
class PolygonInfo:
    current_pos: List[float]
    name_role: str
    role_data: RoleData


@dataclass
class ServerInfo:
    gameTime: str
    state: int
    version: str


@dataclass
class GameData:
    polygon_info: Dict[str, PolygonInfo]
    server_info: ServerInfo
    team_info: Dict[str, TeamInfo]


# Парсинг JSON-данных в объекты дата классов
def json_pars(json_file):
    data = json_file
    game_data = GameData(
        polygon_info={key: PolygonInfo(**value) for key, value in data['polygon_info'].items()},
        server_info=ServerInfo(**data['server_info']),
        team_info={key: TeamInfo(**value) for key, value in data['team_info'].items()}
    )
    dict_of_pos = {}

    # Получение параметра `pos` для каждого игрока и составление словаря
    for team, team_info in game_data.team_info.items():
        for player_id, player in team_info.players.items():
            dict_of_pos[player_id] = player['current_pos']
    return dict_of_pos




