FROM python:3

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install 

COPY . ./

ENTRYPOINT [ "poetry", "run", "python3", "bot.py" ]