from pathlib import Path
from PIL import Image, ImageFont

base = Path(__file__).parent

DAY_SINCE_FIRE_FILE = "days_since_fire.jpg"
DAY_SINCE_FIRE = Image.open(base / DAY_SINCE_FIRE_FILE)
FONT = ImageFont.truetype(str((base / "comic.ttf")), 140)

PARKING_SHORT_PATH = base / "parking.mp3"

TECS_PATHS = [
    base / "tecs/tecs_0.webp",
    base / "tecs/tecs_1.webp",
    base / "tecs/tecs_2.webp",
    base / "tecs/tecs_3.webp",
    base / "tecs/tecs_4.webp",
    base / "tecs/tecs_5.webp",
    base / "tecs/tecs_6.webp"
]