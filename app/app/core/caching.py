import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
import json
from app.db.session import Session
from app.models.ticket import Ticket
from app.models.iata import IATA
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


def add_ticket_to_db(ticket):
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
    if session.query(Ticket).filter_by(date_search=ticket["date_search"]).count():
        old_ticket = session.query(Ticket).filter_by(date_search=ticket["date_search"])
        session.delete(old_ticket)
        session.commit()
    new_ticket = Ticket(fly_from=iata1, fly_to=iata2, date_from=ticket["date_from"], date_to=ticket["date_to"],
                        date_search=ticket["date_search"], booking_token=ticket["booking_token"],
                        price=ticket["price"])
    session.add(new_ticket)
    session.commit()


def make_request(iata_from, iata_to, date_from):
    request = f"https://api.skypicker.com/flights?partner=picky&fly_from={iata_from}&fly_to={iata_to}&date_from=" \
              f"{date_from.strftime('%d/%m/%Y')}&adults=1"
    # print(request)
    return requests.get(request).json()


def caching():
    date1 = date.today()
    print(date1.strftime('%Y-%m-%d'))
    date2 = date1 + relativedelta(months=+1)
    print(date2.strftime('%Y-%m-%d'))

    for iata1, iata2 in iatas:
        while date1 != date2:
            data = makeRequest(iata1, iata2, date1)
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
                    "iata1": ticket["flyFrom"],
                    "iata2": ticket["flyTo"],
                    "date_from": ticket["dTime"],
                    "date_to": ticket["aTime"],
                    "date_search": date1.strftime('%d/%m/%Y'),
                }
                if not flag:
                    chipest_ticket = main_data_in_ticket
                    flag = True
                else:
                    if int(ticket["price"]) < int(chipest_ticket["price"]):
                        chipest_ticket = ticket
            add_ticket_to_db(ticket=chipest_ticket)
            print(date1)
            date1 += relativedelta(days=1)
