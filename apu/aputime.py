#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Copyright (C) 2012 Maverick JS <mavjs01@gmail.com>
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import webbrowser
import pytz
import hashlib
import requests
from BeautifulSoup import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime


class APU(object):

    def __init__(self, intake, week):
        self.baseurl = 'http://webspace.apiit.edu.my/intake-timetable/intake-result.php'
        self.storage = 'APUTimeTable'
        self.homedir = os.path.expanduser('~')
        self.intake = intake
        self.week = week
        self.html = self.intake + '-' + self.week + '.html'
        self.ics = self.intake + '-' + self.week + '.ics'
        self.storagedir = os.path.join(self.homedir, self.storage)
        self.savehtml = os.path.join(self.storagedir, self.html)
        self.saveics = os.path.join(self.storagedir, self.ics)
        self.kl = pytz.timezone('Asia/Kuala_Lumpur')

    def scrape(self):
        payload = { 'week': self.week+'.xml', 'intake_Search_Week': self.intake, 'selectIntakeAll': self.intake }
        headers = {'User-Agent': 'aputime.py/1.0 (+https://github.com/mavjs/APUTimeTable)'}
        request = requests.post( self.baseurl, data=payload, headers=headers)
        parse_html = BeautifulSoup(request.text)
        final_html = parse_html.find('table', {'class': 'timetable-display'})
        return final_html

    def to_html(self):
        if not os.path.exists(self.storagedir):
            os.makedirs(self.storagedir)
        f = file(self.savehtml, 'wb')
        f.write(str('<!DOCTYPE html>\n<html>\n<title>%s</title>\n<body>\n' \
                % self.html))
        f.write(str(self.scrape()))
        f.write(str('\n<p>Generated by <a href="https://github.com/mavjs/APUTimeTable">aputime.py</a></p>'))
        f.write(str('\n</body>\n</html>'))
        f.close()
        return self.savehtml

    def open_html(self):
        try:
            browser = webbrowser.get('firefox')
        except webbrowser.Error:
            browser = webbrowser
        print('Opening html file')
        browser.open(self.to_html())

    def to_ics(self):
        if not os.path.exists(self.storagedir):
            os.makedirs(self.storagedir)
        cal = Calendar()
        cal.add('version', '2.0')
        cal.add('prodid', '-//A.P.U Timetable Synchronizer by MavJS// http://goog.gl/9FRHL //')
        final_html = self.scrape()
        for row in final_html.findAll('tr')[1:]:
            event = Event()
            col = row.findAll('td')
            date = col[0].font.string
            time = col[1].font.string
            classroom = col[2].font.string
            location = col[3].font.string
            subject = col[4].font.string
            lecturer = col[5].font.string
            record = (date, time, classroom, location, subject, lecturer)
            line = "|".join(record)
            #this is lot of unesswary work i know but i like it this way feel free to edit
            parts = line.split('|')
            #trying to find the time
            times = parts[1].split(' - ')
            title = parts[4]
            where = parts[2] + "\t" + parts[3]
            content = parts[5]
            begin_str = "%s %s:00" % (parts[0][4:].strip(""), times[0])
            end_str = "%s %s:00" % (parts[0][4:].strip(""), times[1])
            now = datetime.now()
            now_time = now.strftime('%Y%m%dT%H%M%SZ')
            begin_time = datetime.strptime(begin_str, '%d-%b-%y %H:%M:%S').strftime('%Y%m%dT%H%M%SZ')
            end_time = datetime.strptime(end_str, '%d-%b-%y %H:%M:%S').strftime('%Y%m%dT%H%M%SZ')
            #start gathering info for VEVENT
            summary = title + " by " + content + " at " + where
            desc = title
            start = begin_time
            end = end_time
            stamp = now_time
            event.add('dtstart', start, encode=0)
            event.add('dtend', end, encode=0)
            event.add('transp', 'TRANSPARENT')
            event.add('summary', summary)
            event.add('description', desc)
            event['uid'] = hashlib.md5(desc).hexdigest()
            event.add('dtstamp', stamp, encode=0)
            cal.add_component(event)
        f = file(self.saveics, 'wb')
        f.write(cal.as_string())
        f.close()
        return self.saveics
