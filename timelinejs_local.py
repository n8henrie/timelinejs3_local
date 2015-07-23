"""csv_to_json_timeline.py
Convert a csv file to json format for use with
[TimelineJS3](https://github.com/NUKnightLab/TimelineJS3). Also generates
the basic template CSV file to populate in the first place.
"""

import csv
import argparse
import json
import http.server
import socketserver
import webbrowser


def get_date(row, prefix=''):
    time = row["{}Time".format(prefix)].strip()

    if time == '':
        time_list = [None] * 4
    # Format "HHMM"
    elif len(time) == 4 and all([n.isdigit() for n in time]):
        time_list = [time[:2], time[2:]] + [None] * 2

    # Support formats HH:MM or HH:MM:SS or HH:MM:SS.ms
    elif ":" in time:
        # h, m, s, ms
        time_list = (time.split(":") + [None] * 4)[:4]

        if '.' in time_list[2]:
            time_list[2], time_list[3] = time_list[2].split('.')
            # Zero pad to make sure ms has 3 and only 3 digits
            time_list[3] = '{:<03}'.format(time_list[3])[:3]

    try:
        return {
            'year': row["{}Year".format(prefix)],
            'month': row["{}Month".format(prefix)],
            'day': row["{}Day".format(prefix)],
            'hour': time_list[0],
            'minute': time_list[1],
            'second': time_list[2],
            'millisecond': time_list[3]
        }
    except NameError as e:
        print(e)
        raise NameError("Unrecognized time format: {}".format(time))

def convert(args):
    json_data = main(args.csvfile)
    if args.outfile != 'data.json':
        print("Don't forget to change the data.json filename in index.html")
    with open(args.outfile, 'w') as f:
        json.dump(json_data, f, indent=4)


def main(infile):
    timeline_title = input("Timeline title? ")
    headline_subtext = input("Headline subtext? ")
    data = {
        'events': [],
        'title': {
            'text': {
                'headline': timeline_title,
                'text': headline_subtext
            }
        },
        'scale': 'javascript'
    }
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_date = get_date(row)
            end_date = get_date(row, prefix="End ")

            text = {
                'headline': row["Headline"],
                'text': row["Text"]
            }

            media = {
                'url': row['Media'],
                'caption': row["Media Caption"],
                'credit': row["Media Credit"],
                'thumb': row["Media Thumbnail"]
            }

            event = {
                'start_date': start_date,
                'end_date': end_date,
                'display_date': row["Display Date"],
                'text': text,
                'media': media,
                'type': row["Type"],
                'group': row["Group"],
                'background': row["Background"]
            }

            data['events'].append(event)
    return data


def runserver(args):
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("localhost", args.port), Handler)
    webbrowser.open_new_tab('http://localhost:' + str(args.port))
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    convert_parser = subparsers.add_parser('convert', help="Convert a file")
    convert_parser.add_argument("csvfile", help="File to convert")
    convert_parser.add_argument("-o", "--outfile", default='data.json',
                                help="Destination file")
    convert_parser.set_defaults(func=convert)

    runserver_parser = subparsers.add_parser('runserver', help="Run http "
                                             "server")
    runserver_parser.add_argument("-p", "--port", type=int, default=8000,
                                  help="Port to run on")
    runserver_parser.set_defaults(func=runserver)
    args = parser.parse_args()
    args.func(args)
