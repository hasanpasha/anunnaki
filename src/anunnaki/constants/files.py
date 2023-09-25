from anunnaki.constants.paths import AppPaths
from anunnaki.constants.strings import AppStrings
from os import path

class AppFiles:
    def __init__(self) -> None:
        self.DB = path.join(AppPaths().DATA_PATH, 
                f"{AppStrings.APP_NAME}_{AppStrings.APP_ORG_NAME}_{AppStrings.APP_VERSION}.json")