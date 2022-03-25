from arrival_test.models.bear import Bear
from arrival_test.utils.logger import Logger


def generate_bear(bear_type=None, bear_name=None, bear_age=None):
    Logger.info("Generating bear...")
    bear = Bear(bear_type=bear_type, bear_name=bear_name, bear_age=bear_age)
    Logger.info(f"Bear was successfully generated. {bear}")
    return bear
