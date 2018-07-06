#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from icalendar import Calendar, Event
from datetime import datetime
import pytz
import re
import os
import glob
# import tempfile

timezone = "Europe/London"
timefmt = '%Y%m%dT%H%M%S'
conf_year = 2018
conf_month = 7

directory = '/home/rkhbvs/works/tmp/p-18_02_28-lphys/schedules_py/'
filenames = glob.glob(directory + "*.md")
# print(filenames)

cal = Calendar()


def display(cal):  # {{{
    """
    Helper function to display cal
    """
    return cal.to_ical().replace('\r\n', '\n').strip()


# }}}
def convert_date(day, start):  # {{{
    """ Converts day and start-time to proper format

    :day: string with day number
    :start: string with "hh:mm"
    :returns: datetime object to match ical needs

    """

    hour, minute = start.split(':')
    # return "TZID="+timezone+":"+
    return datetime(conf_year, conf_month, int(day), int(hour),
                    int(minute), 0, tzinfo=pytz.timezone(timezone))


# }}}
def add_talk(day, start, finish, presenter, title):  # {{{
    """ Helper function to add event to the calendar

    :day: TODO
    :start: TODO
    :finish: TODO
    :presenter: TODO
    :title: TODO
    :returns: TODO

    """

    hour, minute = start.split(':')

    # We first initialize an empty event
    event = Event()
    # Populate it with properties
    event.add('dtstart', convert_date(day, start))
    event.add('dtend', convert_date(day, finish))
    event.add('summary', presenter)
    if title:
        event.add('description', title)

    # Add the event to the calendar
    cal.add_component(event)


# }}}
def parse_line(lstr):  # {{{
    """ Grabs the line and either sets some global variables or adds an event to calendar

    :lstr: TODO
    :returns: TODO

    """

    global day
    global session
    # The day and session variables will travel across talks anounced in
    # different lines so the variables are global

    # print('Parsing ' + lstr.strip())

    day_line = re.search(r'.*#####.*?day, (\d\d) July.*', lstr)
    # If there is the day, the function sets the global variable day and exits
    # otherwise it will try to extract the information about the scheduled talk
    if day_line:
        day = int(day_line.group(1))
        return

    chair_line = re.search(
        r'([SPl\d]*\.\d).*[(](\d\d:\d\d...\d\d:\d\d)[)].*[*]{2}: ([a-zA-Z ()]*)', lstr)
    talk_line = re.search(
        r'.*\[\[(\d\d:\d\d . \d\d:\d\d) \].*?\[([^\[]*?)\]{style="text-decoration: underline"}.*?]{style="display: block;"}(.*?)\[\[Abstr', lstr)
    # The lines announcing chairs and talks should match these patterns
    # If anything is matched, the block below parses some relevant data
    if chair_line:
        st_fn = chair_line.group(2).split()
        session = chair_line.group(1)
        author = 'Chair: ' + chair_line.group(3)
        title = ''
    elif talk_line:
        st_fn = talk_line.group(1).split()
        author = talk_line.group(
            2) + ' "' + talk_line.group(3).replace("*", "").strip() + '"'
        title = ''
    else:
        # If line matches none, the function does not return anything
        return

    start = st_fn[0]
    finish = st_fn[-1]

    # If the data is populated, we add event to the calendar
    add_talk(day, start, finish, session + ' ' + author, title)
    return


# }}}
def parse_file(fname):  # {{{
    """ Takes markdown with schedule and outputs ical

    :fname: TODO
    :returns: TODO

    """

    bsname = os.path.splitext(os.path.basename(fname))[0]
    # print(bsname)
    calname = bsname + '.ics'

    global cal
    cal = Calendar()
    cal.add('prodid', 'andrey.rakhubovsky@gmail.com')
    cal.add('version', '2.0')
    global day
    day = 0

    with open(fname) as f:
        for line in f.readlines():
            parse_line(line)

    fe = open(os.path.join(directory, calname), 'wb')
    # print(fe)
    fe.write(cal.to_ical())
    fe.close()


# }}}


for filename in filenames:
    parse_file(filename)
