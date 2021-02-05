# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union, Tuple
from datetime import datetime
import json, os, shutil

# Pip
from ksimpleapi import Api
from simple_multiprocessing import MultiProcess, Task

# Local
from .models import Sport, Game, GameAssets
from ._cache_utils import _CacheUtils

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
        only_major_games: bool = False,
        only_live_games: bool = False,
        included_status_groups: List[int] = [1, 2, 3, 4],
        include_cancelled: bool = False,
        include_postponed: bool = False
    ) -> Optional[List[Game]]:
        if sports and type(sports) != list:
            sports = [sports]

        try:
            res = self._get(
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
                }
            ).json()

            games = []

            for game_json in res['games']:
                try:
                    sport_id = game_json['sportId']
                    competition_id = game_json['competitionId']
                    competition_dict = [competition_dict for competition_dict in res['competitions'] if competition_dict['id'] == competition_id][0]
                    home_competitor_country_id = game_json['homeCompetitor']['countryId']
                    away_competitor_country_id = game_json['awayCompetitor']['countryId']

                    game = Game(
                        game_json,
                        sport_dict=[sport_dict for sport_dict in res['sports'] if sport_dict['id'] == sport_id][0],
                        competition_dict=competition_dict,
                        competition_country_dict=[country_dict for country_dict in res['countries'] if country_dict['id'] == competition_dict['countryId']][0],
                        home_competitor_country_dict=[country_dict for country_dict in res['countries'] if country_dict['id'] == home_competitor_country_id][0],
                        away_competitor_country_dict=[country_dict for country_dict in res['countries'] if country_dict['id'] == away_competitor_country_id][0]
                    )

                    if (
                        (not included_status_groups or game.status_group in included_status_groups)
                        and
                        (include_cancelled or not game.cancelled)
                        and
                        (include_postponed or not game.postponed)
                        and
                        (not only_live_games or game.live)
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

    def download_assets(
        self,
        game: Game,
        competition_image_path: Optional[str] = None,
        home_competitor_image_path: Optional[str] = None,
        away_competitor_image_path: Optional[str] = None,
        image_folder_path: Optional[str] = None,
        round_images: bool = True,
        request_timeout: float = 5,
        use_cache: bool = True
    ) -> GameAssets:
        if image_folder_path:
            os.makedirs(image_folder_path, exist_ok=True)

        def get_image(
            image_url: str,
            image_path: Optional[str] = None,
            image_folder_path: Optional[str] = None,
            round_image: bool = True,
            request_timeout: float = 5,
            use_cache: bool = True
        ) -> Tuple[str, bool]:
            downloaded_image_path = _CacheUtils.temp_download_image_path_for_url(image_url, image_path, image_folder_path, use_cache)
            final_download_image_path = _CacheUtils.final_download_image_path_for_url(image_url, image_path, image_folder_path)

            if not os.path.exists(downloaded_image_path) and not self._download(image_url, downloaded_image_path, timeout=request_timeout):
                return final_download_image_path, False

            if not downloaded_image_path == final_download_image_path:
                shutil.copy2(downloaded_image_path, final_download_image_path)

            return final_download_image_path, True

        _kwargs = {
            'image_folder_path': image_folder_path,
            'round_image': round_images,
            'request_timeout': request_timeout,
            'use_cache': use_cache
        }

        competition_image_url = game.competition.get_image_url(round=round_images)
        home_competitor_image_url = game.home_competitor.get_image_url(round=round_images)
        away_competitor_image_url = game.away_competitor.get_image_url(round=round_images)

        (competition_image_path, _), (home_competitor_image_path, _), (away_competitor_image_path, _) = MultiProcess([
            Task(get_image, competition_image_url, competition_image_path, **_kwargs),
            Task(get_image, home_competitor_image_url, home_competitor_image_path, **_kwargs),
            Task(get_image, away_competitor_image_url, away_competitor_image_path, **_kwargs)
        ]).solve()

        return GameAssets(
            competition_image_url, competition_image_path,
            home_competitor_image_url, home_competitor_image_path,
            away_competitor_image_url, away_competitor_image_path
        )


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