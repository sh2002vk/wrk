from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from db import get_latest, update_latest, add_multiple, update_queue
from sms import send_notif, send_message
from scraper import get_jobs

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Starting server"}


@app.on_event("startup")
@app.get("/startup/on")
async def on():
    body = f"\nIntern notification server now running\n@svStudios"
    send_message(body)


@app.on_event("startup")
@app.get("/data_ingestion/update")
@repeat_every(seconds=60*30)
async def update():
    latest_company = get_latest()
    job_list, new_company = get_jobs(latest_intern=latest_company)
    if latest_company != new_company:
        update_latest(new_company)
        add_multiple(job_list)
        send_notif(job_list)
        print(f"Added {len(job_list)} jobs")
    else:
        print("No new jobs")


# TODO: Twilio notification system
# @app.get("/comms/notify_users")
# async def notify_users():

