import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib

link = "https://www.cscareers.dev/job-postings"
page = requests.get(link)
soup = BeautifulSoup(page.content, "html.parser")
company_location_class = "flex space-x-4"
category_class = "px-2 mt-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-indigo-100 text-indigo-800"
date_class = "mt-2 flex items-center text-sm text-gray-500 sm:mt-0"

python_jobs = soup.find_all("div", class_="md:px-4 py-4")


def get_jobs(latest_intern):
    """
    :param latest_intern: latest intern role in db
    :return: list of new jobs to add to db and the new latest intern
    """

    job_list = []
    newHash = latest_intern

    for i in python_jobs:
        company_location = list(i.find("div", class_=company_location_class))
        company = company_location[0].text
        location = company_location[1].text
        category = i.find("p", class_=category_class).text
        date = i.find("time").text

        my_string_bits = str(company+location+category).encode('utf-8')
        hash = hashlib.sha256(my_string_bits).hexdigest()

        if category == "Intern":
            if hash == latest_intern:
                print("breaking")
                break
            else:
                job_list.append({
                    "company": company,
                    "location": location,
                    "category": category,
                    "date": date,
                    "hash": hash
                })

    if len(job_list) > 0:
        newHash = job_list[0]["hash"]

    return job_list, newHash


def convert_epoch(date):
    p = '%Y-%m-%d'
    origin = datetime(1970, 1, 1)
    try:
        epoch = (datetime.strptime(date, p) - origin).total_seconds()
        return epoch
    except Exception as e:
        print("date exception")
    return 0
