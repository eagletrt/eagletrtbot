import re
from sqlalchemy import Column, Integer, Sequence, String

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler
from bot.commands.brao import volpe

from bot.database.base import Base
from bot.database.session import Session
from bot.utils import escape, only_eagle


class Points(Base):
    __tablename__ = "points"
    id = Column(Integer, Sequence("points_id_seq"), primary_key=True)
    team = Column(String)
    score = Column(Integer)


teams = ["SW", "HW", "MT", "DMT", "PR", "MGT"]
positions = ["👑", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
banned = [
    68827761,  # @CapoElettronico
]


re_points = re.compile("^([+-]?[1-9]\d*|0)$")


@only_eagle
def punti(update: Update, ctx: CallbackContext):
    if len(ctx.args) == 2:
        if update.effective_user.id in banned:
            volpe(update, ctx)
        team = ctx.args[0].upper()
        if team not in teams:
            update.message.reply_text(
                f"No cara, il team {team} non esiste...",
                quote=True,
            )
            return

        number = ctx.args[1]
        if re_points.match(number) is None:
            update.message.reply_text(
                f'No cara, "{number}" non è un numero intero...',
                quote=True,
            )
            return
        amount = int(number)

        with Session() as session:
            points = session.query(Points).filter_by(team=team).first()
            if points is None:
                points = Points(team=team, score=0)
                session.add(points)
            points.score += amount
            session.commit()

    with Session() as session:
        points = session.query(Points).order_by(Points.score.desc()).all()

    points_txt = "\n\n".join(
        [
            f"{positions[index]} *{escape(item.team)}*\n✨ {escape(item.score)}"
            for index, item in enumerate(points)
        ]
    )

    missing = teams[:]
    for point in points:
        missing.remove(point.team)

    if len(missing) > 0:
        missing_points_txt = ", ".join([f"*{team}*" for team in missing])
        points_txt = f"{points_txt}\n\n{missing_points_txt} con 0 punti"

    update.message.reply_markdown_v2(points_txt, quote=True)


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("punti", punti))
