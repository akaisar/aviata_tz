import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import calendar
import json
from app.db.session import Session
from app.models.ticket import Ticket
from app.models.iata import IATA
from app.core.celery_app import celery_app
import logging
session = Session()
iatas = [
    ("ALA", "TSE"),
    ("TSE", "ALA"),
    ("ALA", "MOW"),
    ("MOW", "ALA"),
    ("ALA", "CIT"),
    ("CIT", "ALA"),
    ("TSE", "MOW"),
    ("MOW", "TSE"),
    ("TSE", "LED"),
    ("LED", "TSE"),
]
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_ticket(ticket):
    pass


def add_ticket_to_db(ticket, date_search):

    if session.query(IATA).filter_by(code=ticket["flyFrom"]).count() == 0:
        iata1 = IATA(code=ticket["flyFrom"])
        session.add(iata1)
    else:
        iata1 = session.query(IATA).filter_by(code=ticket["flyFrom"])[0]
    if session.query(IATA).filter_by(code=ticket["flyTo"]).count() == 0:
        iata2 = IATA(code=ticket["flyTo"])
        session.add(iata2)
    else:
        iata2 = session.query(IATA).filter_by(code=ticket["flyTo"])[0]
        session.add(iata2)
    session.commit()
    if session.query(Ticket).filter_by(date_search=date_search).count():
        old_tickets = session.query(Ticket).filter_by(date_search=date_search)
        for old_ticket in old_tickets:
            session.delete(old_ticket)
        session.commit()
    new_ticket = Ticket(fly_from=iata1, fly_to=iata2, date_from=ticket["date_from"], date_to=ticket["date_to"],
                        date_search=date_search, booking_token=ticket["booking_token"],
                        price=ticket["price"])
    session.add(new_ticket)
    session.commit()


def make_request(iata_from, iata_to, date_from):
    request = f"https://api.skypicker.com/flights?partner=picky&fly_from={iata_from}&fly_to={iata_to}&date_from=" \
              f"{date_from.strftime('%d/%m/%Y')}&adults=1"
    # print(request)
    return requests.get(request).json()


@celery_app.task
def caching():
    logger.info("Start, caching")
    date1 = date.today()
    print(date1.strftime('%Y-%m-%d'))
    date2 = date1 + relativedelta(months=+1)
    print(date2.strftime('%Y-%m-%d'))

    for iata1, iata2 in iatas:
        logger.info(f"{iata1} to {iata2} start")
        while date1 != date2:
            data = make_request(iata1, iata2, date1)
            data = data["data"]
            flag = False
            chipest_ticket = {}
            for ticket in data:
                # with open('data2.json', 'w', encoding='utf-8') as f:
                #     json.dump(ticket, f, ensure_ascii=False, indent=4)
                # exit(0)
                main_data_in_ticket = {
                    "booking_token": ticket["booking_token"],
                    "price": ticket["price"],
                    "flyFrom": ticket["flyFrom"],
                    "flyTo": ticket["flyTo"],
                    "date_from": datetime.utcfromtimestamp(int(ticket["dTime"])),
                    "date_to": datetime.utcfromtimestamp(int(ticket["aTime"])),
                }
                if not flag:
                    chipest_ticket = main_data_in_ticket
                    flag = True
                else:
                    if int(ticket["price"]) < int(chipest_ticket["price"]):
                        chipest_ticket = ticket
            add_ticket_to_db(ticket=chipest_ticket, date_search=date1)
            print(date1)
            date1 += relativedelta(days=1)
    logger.info("End, caching")
