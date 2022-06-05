FROM mcr.microsoft.com/playwright:focal

RUN apt-get update && apt-get install -y python3-pip

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install 

RUN python -m playwright install

COPY . ./

ENTRYPOINT [ "poetry", "run", "python3", "bot.py" ]