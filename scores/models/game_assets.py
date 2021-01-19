# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Pip
from jsoncodable import JSONCodable

# Local
from .game_asset import GameAsset

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: GameAssets ----------------------------------------------------------- #

class GameAssets(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        competition_image_url: str,
        competition_image_path: str,
        home_competitor_image_url: str,
        home_competitor_image_path: str,
        away_competitor_image_url: str,
        away_competitor_image_path: str,
    ):
        self.competition = GameAsset(competition_image_url, competition_image_path)
        self.home_competitor = GameAsset(home_competitor_image_url, home_competitor_image_path)
        self.away_competitor = GameAsset(away_competitor_image_url, away_competitor_image_path)


# ---------------------------------------------------------------------------------------------------------------------------------------- #