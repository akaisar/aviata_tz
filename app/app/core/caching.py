import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import calendar
import json
from app.models.ticket import Ticket
from app.models.iata import IATA
from app.core.celery_app import celery_app
from app.db.session import db_session
import logging

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
    request = (
        f"https://booking-api.skypicker.com/api/v0.1/check_flights?v=2&booking_token={ticket['booking_token']}&"
        f"pnum=1&bnum=0"
    )
    response = requests.get(request).json()
    return response


def add_ticket_to_db(ticket, date_search):
    # logger.info(f"Ticket {ticket['booking_token']} start updload to db")
    ticket_info = check_ticket(ticket)
    if ticket_info["flights"][0]["invalid"] == 1:
        return
    ticket["price"] = ticket_info["flights_price"]
    new_ticket = Ticket(
        fly_from=iata1,
        fly_to=iata2,
        date_from=ticket["date_from"],
        date_to=ticket["date_to"],
        date_search=date_search,
        booking_token=ticket["booking_token"],
        price=ticket["price"],
    )
    db_session.add(new_ticket)
    db_session.commit()
    # logger.info(f"Ticket {ticket['booking_token']} succes updload to db")


def add_iata_to_db(iata):
    if db_session.query(IATA).filter_by(code=iata).count() == 0:
        iata_model = IATA(code=iata)
        db_session.add(iata_model)
        db_session.commit()
        return iata_model
    else:
        return db_session.query(IATA).filter_by(code=iata)[0]


def make_request(iata_from, iata_to, date_from):
    request = (
        f"https://api.skypicker.com/flights?partner=picky&fly_from={iata_from}&fly_to={iata_to}&date_from="
        f"{date_from.strftime('%d/%m/%Y')}&adults=1"
    )
    # print(request)
    return requests.get(request).json()


def caching():
    logger.info(f"Start, caching time {datetime.now()}")
    for iata_from, iata_to in iatas:
        iata_from_model = add_iata_to_db(iata_from)
        iata_to_model = add_iata_to_db(iata_to)
        iterator_date = date.today()
        date_end = iterator_date + relativedelta(months=+1)
        logger.info(f"{iata_from} to {iata_to} start")
        while iterator_date != date_end:
            logger.info(f"{iterator_date} start caching")
            if (
                db_session.query(Ticket)
                .filter_by(
                    date_search=iterator_date,
                    fly_from=iata_from_model,
                    fly_to=iata_to_model,
                )
                .count()
            ):
                iterator_date += relativedelta(days=1)
                continue
            data = make_request(iata_from, iata_to, iterator_date)
            data = data["data"]
            flag = False
            chipest_ticket = {}
            for ticket in data:
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
            logger.info(f"kek3")
            add_ticket_to_db(ticket=chipest_ticket, date_search=iterator_date)
            print(iterator_date)
            iterator_date += relativedelta(days=1)
            logger.info(f"{iterator_date} end caching")
    logger.info("End, caching")


@celery_app.task
def reload_cache():
    tickets = db_session.query(Ticket).all()
    for ticket in tickets:
        db_session.delete(ticket)
    db_session.commit()
    caching()
