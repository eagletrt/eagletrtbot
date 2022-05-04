from sqlalchemy import Column, Integer, Sequence, String

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler

from bot.database.base import Base
from bot.database.session import Session
from bot.utils import escape, only_eagle


class Points(Base):
    __tablename__ = "points"
    id = Column(Integer, Sequence("odg_id_seq"), primary_key=True)
    team = Column(String)
    score = Column(Integer)


teams = ["SW", "HW", "MT", "DMT", "EMT"]
positions = ["👑", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]


@only_eagle
def punti(update: Update, ctx: CallbackContext):
    if len(ctx.args) > 0:
        if ctx.args[0] == "reset":
            with Session() as session:
                session.query(Points).delete()
                session.commit()

            update.message.reply_text(
                f"Ok cara, ho cancellato tutti i punti",
                quote=True,
            )
            return

        team = ctx.args[0].upper()
        if team not in teams:
            update.message.reply_text(
                f"No cara, il team {escape(team)} non esiste...",
                quote=True,
            )
            return

        amount = 1
        if len(ctx.args) > 1:
            number = ctx.args[1]
            if not number.lstrip("-").isdigit():
                update.message.reply_text(
                    f'No cara, "{escape(number)}" non è un numero...',
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

    missing = teams[:]
    for point in points:
        missing.remove(point.team)

    missing_points_txt = ", ".join([f"*{team}*" for team in missing])
    points_txt = "\n\n".join(
        [
            f"{positions[index]} *{escape(item.team)}*\n✨ {escape(item.score)}"
            for index, item in enumerate(points)
        ]
    )

    update.message.reply_markdown_v2(
        f"{points_txt}\n\n{missing_points_txt} con 0 punti",
        quote=True,
    )


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("punti", punti))
