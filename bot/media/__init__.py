from pathlib import Path
from PIL import Image, ImageFont

base = Path(__file__).parent

DAY_SINCE_FIRE_FILE = "days_since_fire.jpg"
DAY_SINCE_FIRE = Image.open(base / DAY_SINCE_FIRE_FILE)

SIMIONE_FILE = "simione.jpg"
SIMIONE = Image.open(base / SIMIONE_FILE)

FONT_XL = ImageFont.truetype(str((base / "comic.ttf")), 140)
FONT_MD = ImageFont.truetype(str((base / "comic.ttf")), 50)

PARKING_SHORT_PATH = base / "parking.mp3"

LIKE_AND_SAVE = base / "like_and_save.webp"

TECS_PATHS = [
    base / "tecs/tecs_0.webp",
    base / "tecs/tecs_1.webp",
    base / "tecs/tecs_2.webp",
    base / "tecs/tecs_3.webp",
    base / "tecs/tecs_4.webp",
    base / "tecs/tecs_5.webp",
    base / "tecs/tecs_6.webp",
    base / "tecs/tecs_7.webp",
]
