from mongo_utils import get_db, update_status_based_on_fields ,get_not_sent_today ,get_not_sent_ready_today, get_and_reschedule_not_sent_today
from sendTodayEmails import process_applications
import csv , json , time

# Connect to MongoDB
db = get_db()

collection_name = "job_apps"








# -------Getting today scheduling application
try:
    # -------Process the data
    update_status_based_on_fields(db, collection_name, get_not_sent_today(db , collection_name))

    process_applications(get_not_sent_ready_today(db, collection_name), db, collection_name)
    time.sleep(10)
    get_and_reschedule_not_sent_today(db, collection_name)

except Exception as e:
    print("Error during processing:", e)
