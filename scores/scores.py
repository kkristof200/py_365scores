# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union
from datetime import datetime
import json

# Pip
from ksimpleapi import Api

# Local
from .models import Sport, Game

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: 365Scores ----------------------------------------------------------- #

class Scores(Api):

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def get_games(
        self,
        sports: Optional[Union[List[Union[Sport, int]], Union[Sport, int]]] = None,
        competition_ids: Optional[Union[List[int], int]] = None,
        start_date: Optional[Union[int, datetime, str]] = None, # 03/01/2021
        end_date: Optional[Union[int, str]] = None,   # 03/01/2021
        only_major_games: bool = True,
        only_live_games: bool = False,
        included_status_groups: List[int] = [1, 2, 3, 4],
        include_cancelled: bool = False,
        include_postponed: bool = False
    ) -> Optional[List[Game]]:
        if sports and type(sports) != list:
            sports = [sports]

        try:
            games = []

            for game_json in self._get(
                'https://webws.365scores.com/web/games/allscores',
                params={
                    'appTypeId': 5,
                    'langId': 1,
                    'startDate': self.__normalized_date(start_date),
                    'endDate': self.__normalized_date(end_date),
                    'onlyMajorGames': 'true' if only_major_games else None,
                    'onlyLiveGames': 'true' if only_live_games else None,
                    'sports': ','.join([sport.value if type(sport) == Sport else sport for sport in sports]) if sports else None,
                    'competitionIds': ','.join(competition_ids) if competition_ids else None
                },
            ).json()['games']:
                try:
                    game = Game(game_json)

                    if (
                        (not included_status_groups or game.status_group in included_status_groups) 
                        and
                        (include_cancelled or not game.cancelled)
                        and
                        (include_postponed or not game.postponed)
                    ):
                        games.append(game)
                except Exception as e:
                    if self.debug:
                        print(e, json.dumps(game_json, indent=4))

            return games
        except Exception as e:
            if self.debug:
                print(e)

            return None


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def __normalized_date(
        self,
        date: Optional[Union[int, datetime, str]]
    ) -> Optional[str]:
        if not date:
            return None

        if type(date) == int:
            date = datetime.fromtimestamp(date)

        if type(date) == datetime:
            date = '{}/{}/{}'.format(str(date.day).zfill(2), str(date.month).zfill(2), date.year())

        return date


# ---------------------------------------------------------------------------------------------------------------------------------------- #