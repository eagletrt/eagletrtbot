import threading, time, os, pyairtable, sys, json

AIRTABLE_UPDATER_MUTEX = threading.Lock()
LAST_ATTENDANCES_UPDATE = time.time()
MIN_DELTA_REQUESTS = 2
AIRTABLE_TOKEN = os.environ["SECRET_AIRTABLE_TOKEN"]
HR_BASE_ID = os.environ["AIRTABLE_HR_BASE_ID"]
LAB_ATTENDANCES_TABLE_ID=os.environ["AIRTABLE_LAB_ATTENDANCES_TABLE_ID"]
PEOPLE_TABLE_ID=os.environ["AIRTABLE_PEOPLE_TABLE_ID"]
PEOPLE_TABLE_CACHE_FP = "telegram_people_table_cache.json"
TELEGRAM_TO_EMAIL_CACHE_FP = "telegram_to_email_cache.json"
LAB_ATTENDANCES_CACHE_FD = "lab_attendances_cache.json"


def update_all_caches() -> bool:
    telegram_to_email_cache = {}
    try:
        AIRTABLE_API = pyairtable.Api(AIRTABLE_TOKEN)
        LAB_ATTENDANCES_TABLE = AIRTABLE_API.table(HR_BASE_ID, LAB_ATTENDANCES_TABLE_ID)
        PEOPLE_TABLE = AIRTABLE_API.table(HR_BASE_ID, PEOPLE_TABLE_ID)
    except:
        sys.stdout.write("Error updating caches!")
        return False
    lab_att_cache = LAB_ATTENDANCES_TABLE.all()
    all_people_table = PEOPLE_TABLE.all()
    for record in all_people_table:
        record_data = record["fields"]
        telegram_handle = record_data.get("@Telegram")
        email = record_data.get("Email")
        telegram_to_email_cache[telegram_handle] = email
    with open(LAB_ATTENDANCES_CACHE_FD, "w") as fp:
        json.dump(lab_att_cache, fp)
        fp.close()
    with open(TELEGRAM_TO_EMAIL_CACHE_FP, "w") as fp:
        json.dump(telegram_to_email_cache, fp)
        fp.close()
    with open(PEOPLE_TABLE_CACHE_FP, "w") as fp:
        json.dump(all_people_table, fp)
        fp.close()
    return True


def airtable_caches_updater():
    global LAST_ATTENDANCES_UPDATE
    current_time = time.time()
    if (current_time - LAST_ATTENDANCES_UPDATE) > MIN_DELTA_REQUESTS:
        LAST_ATTENDANCES_UPDATE = current_time
        if not update_all_caches():
            return False
    return True

