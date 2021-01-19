# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
import os

# Pip
from jsoncodable import JSONCodable

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: GameAsset ----------------------------------------------------------- #

class GameAsset(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        url: str,
        path: str
    ):
        self.url = url
        self.path = path


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def is_donwloaded(self) -> bool:
        return os.path.exists(self.path)


# ---------------------------------------------------------------------------------------------------------------------------------------- #