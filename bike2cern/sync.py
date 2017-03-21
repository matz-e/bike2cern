import argparse
import configparser
import datetime
import http.server
import keyring
import os
import sys
import urllib.parse
import xdg.BaseDirectory

from sharepoint import SharePointSite, basic_auth_opener
from stravalib.client import Client


class Sync(object):

    def __init__(self):
        configdir = xdg.BaseDirectory.load_first_config('bike2cern')
        config = configparser.ConfigParser()
        config.read(os.path.join(configdir, 'sync.cfg'))
        self.__client_id = config['strava']['client_id']
        self.__secret = config['strava']['secret']
        self.__token = keyring.get_password('bike2cern', 'strava')
        self.__user = config['cern']['username']
        self.__pass = keyring.get_password('bike2cern', 'cern')
        self.__list = config['cern']['list_id']

        if not self.__token:
            self.__fetch_token()
            self.__token = keyring.get_password('bike2cern', 'strava')
        if not self.__token:
            raise ValueError("could not access Strava token")

    def __fetch_token(self):
        host = '127.0.0.1'
        port = 5000

        client = Client()
        url = client.authorization_url(client_id=self.__client_id,
                                       redirect_uri='http://127.0.0.1:5000/authorization')
        print("follow this link (ctrl-c to cancel): {}".format(url))

        client_id = self.__client_id
        secret = self.__secret
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                code = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('code', None)[0]
                token = client.exchange_code_for_token(client_id=client_id,
                                                       client_secret=secret,
                                                       code=code)
                keyring.set_password('bike2cern', 'strava', token)

        s = http.server.HTTPServer((host, port), Handler)
        try:
            s.handle_request()
        except KeyboardInterrupt:
            pass
        s.server_close()

    def add_rides(self, start, end, nosave):
        client = Client(access_token=self.__token)

        url = 'https://social.cern.ch/community/BikeCommuters'
        opener = basic_auth_opener(url, self.__user, self.__pass)
        site = SharePointSite(url, opener)
        cal = site.lists[self.__list]

        total = 0
        for activity in client.get_activities(before=end, after=start):
            if not activity.commute:
                continue

            print("adding ride on {}".format(activity.start_date))
            cal.append({'Date': activity.start_date,
                        'Distance': float(activity.distance) / 1000})
            total += float(activity.distance) / 1000
        print("added {} km".format(total))
        if nosave:
            return
        cal.save()

def run():
    def date(s):
        return datetime.datetime.strptime(s, '%Y-%m-%d')

    parser = argparse.ArgumentParser(description="sync Strava rides to CERN Sharepoint")
    parser.add_argument("--dry-run", action="store_true", help="do nothing, just list rides")
    parser.add_argument("start", type=date, help="start date in the form YYYY-mm-dd")
    parser.add_argument("end", type=date, help="start date in the form YYYY-mm-dd")
    args = parser.parse_args()
    try:
        s = Sync()
    except Exception as e:
        print(e)
        sys.exit(1)
    s.add_rides(args.start, args.end, args.dry_run)

if __name__ == '__main__':
    run()
