from pymongo import MongoClient
from pandas import DataFrame
import os

connection_str = os.getenv("mongoConnection")
client = MongoClient(connection_str)


def get_latest():
    """Gets latest intern role"""

    data_filter = {
        'id': 'latest_intern'
    }

    result = DataFrame(client['job_list']['intern'].find(
        filter=data_filter
    )).to_dict('records')

    return result[0]["hash"]


def add_single(job: dict):
    """Adds a single role to the db"""

    try:
        client['job_list']['intern'].insert_one(job)
        return True
    except Exception as e:
        print(f"MONGO INSERTION ERROR - single - {e}")
    return False


def add_multiple(job_list: list):
    """Adds multiple jobs to the db"""

    try:
        client['job_list']['intern'].insert_many(job_list)
        return True
    except Exception as e:
        print(f"MONGO INSERTION ERROR - multiple - {e}")
    return False


def find_company(company_title: str):
    """Finds a company"""

    data_filter = {
        'company': company_title
    }

    result = client['job_list']['intern'].find(
        filter=data_filter
    )
    result_df = DataFrame(result).to_dict('records')

    if len(result_df) >= 1:
        return result_df
    return {}


def update_latest(company: str):
    """Updates the latest intern role"""

    myquery = {
        "id": "latest_intern"
    }

    newValue = {
        "$set": {
            "id": "latest_intern",
            "hash": company
        }
    }

    try:
        client['job_list']['intern'].update_one(myquery, newValue)
        return True
    except Exception as e:
        print(f"LATEST ROLE UPDATE FAILED - {e}")
    return False


def update_queue(job_list):
    """Updates the queue for roles that need to be sent out"""

    try:
        client['job_list']['announce_queue'].insert_many(job_list)
        return True
    except Exception as e:
        print(f"MONGO INSERTION ERROR - multiple - {e}")
    return False


def clear_queue():
    """Sends out messages"""

    jobs = client['job_list']['announce_queue'].find()
    jobs_df = DataFrame(jobs)
    # TODO: twilio api integration



