import re

import arrow
from bs4 import BeautifulSoup
import requests
import sys

from ics import Calendar
from ics import Event


def parse_event(event):
    new_event = Event()

    new_event.name = event.find('h3', attrs={'class': 'card__title'}).getText().strip()
    new_event.location = event.findAll('p')[1].getText().strip()
    times = event.findAll('time')

    new_event.begin = arrow.get(times[1]['datetime'])
    new_event.end = arrow.get(times[2]['datetime'])

    return new_event


def main(argv):
    url = 'http://www.bbk.ac.uk/events/?tag=1&b_start:int={0}#events-listing'

    if len(argv) > 1:
        url = argv[1]

    calendar = Calendar()

    for page in range(1, 4):
        url_to_use = url.format(page * 12)

        html = requests.get(url_to_use)

        soup_object = BeautifulSoup(html.text, 'lxml')
        meta = soup_object.find(name='div', attrs={'class': 'row v-space-2'})

        if not meta:
            break

        events = meta.findAll(name='div', attrs={'class': 'column medium-4 large-3'})

        for event in events:
            calendar.events.add(parse_event(event))

    print(calendar)


if __name__ == "__main__":
    main(sys.argv)
