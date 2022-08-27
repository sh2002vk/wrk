from twilio.rest import Client
import os

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
service = os.getenv('MESSAGING_SERVICE')
client = Client(account_sid, auth_token)


def send_notif(job_list):
    """

    :param job_list: list of jobs to be announced
    :return:
    """

    for i in job_list:
        company = i["company"]
        location = i["location"]
        date = i["date"]
        body = f"\nApply alert: \n{company} in {location}\n{date}"
        try:
            message = client.messages.create(
                                  body=body,
                                  from_=service,
                                  to='+17789977375'
                              )
        except Exception as e:
            print("twilio fail")

