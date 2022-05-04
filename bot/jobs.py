from tzlocal import get_localzone

import warnings

warnings.simplefilter("ignore")

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore

jobstores = {
    "default": SQLAlchemyJobStore(url="sqlite:///data/jobs.sqlite"),
    "volatile": MemoryJobStore(),
}

scheduler = BackgroundScheduler(jobstores=jobstores, timezone=get_localzone())
