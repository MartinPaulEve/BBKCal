import re

import arrow
from bs4 import BeautifulSoup
import requests
import sys

from ics import Calendar
from ics import Event


def parse_event(event):
    new_event = Event()

    new_event.name = event.find('h3', attrs={'class': 'heading'}).getText().strip()
    new_event.location = event.find('b', text=re.compile('.*?Location.+')).parent.getText().strip()[10:]
    new_event.begin = arrow.get(
        event.find('b', text=re.compile('.*?Start.+')).parent.find('span').getText().strip().replace(' ', '').replace(
            '\n', ''),
        'DDMMMYYYYHH:mm')
    new_event.end = arrow.get(
        event.find('b', text=re.compile('.*?Finish.+')).parent.find('span').getText().strip().replace(' ', '').replace(
            '\n', ''),
        'DDMMMYYYYHH:mm')

    return new_event


def main(argv):
    url = 'http://www.bbk.ac.uk/events-calendar?browseby=School+of+Arts&item=Subject&portal_type=BBKEvent'

    if len(argv) > 1:
        url = argv[1]

    calendar = Calendar()

    for page in range(0, 4):
        url_to_use = url + '&next={0}'.format(page * 12)

        html = requests.get(url_to_use)

        soup_object = BeautifulSoup(html.text, 'lxml')
        meta = soup_object.find(name='ul', attrs={'class': 'listing event-listing'})
        events = meta.findAll(name='li', attrs={'class': 'item'})

        for event in events:
            calendar.events.append(parse_event(event))

    print(calendar)


if __name__ == "__main__":
    main(sys.argv)
