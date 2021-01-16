import logging
from src.settings import SOURCE_DIR, ASSETS_DIR
logging.basicConfig(

    filename=SOURCE_DIR + ASSETS_DIR + "/log/AutoMatch_Log.txt",
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s : %(lineno)d : %(message)s"

                    )