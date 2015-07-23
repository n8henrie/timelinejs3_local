# timelinejs3_local

Template to make local timelines with TimelineJS3.

## Introduction

I often want to make timelines for presentations. Unfortunately, I haven't
found many ways to do this easily with free software. I did come across
[TimelineJS](timeline.knightlab.com), which looks awesome, but it is primarily
set up to use their server. I prefer to keep things local if possible, so I
figured out how to use TimelineJS locally. Because it looks like
[TimelineJS3](http://timeline3.knightlab.com) is the direction they are going,
this is set up for v3 and not v2.

Unfortunately, while it has a really convenient option to import a CSV file
from Google Drive, it seems that the only way to do this is (again) to share
the doc URL and use their server, which is problematic if you're dealing with
sensitive data.

So I decided to make this repository with a template csv file, a Python
script to convert your data to the expected json format, and a template HTML
file pointed at the proper resources.

## Prerequisites

- Python3

## Installation

```bash
git clone https://github.com/n8henrie/timelinejs3_local.git
cd timelinejs3_local
git submodule update --init --recursive
git submodule foreach git pull origin master
```

## Usage

`python3 timelinejs3_local.py -h`

Edit your csv file in your spreadsheet editor of choice. When it's ready,
`python3 timelinejs3_local.py convert`. Unless you specify an `outfile`, you
will overwrite the local `data.json` file.

You will be prompted for a title and subheading for the main timeline. If you
want to add other fancy features, it should be fairly easy to edit the .json
file directly for the details -- this should get you most of the way by
importing all the events.

After converting, run a local HTTP server `python3 -m http.server` or use the
builtin `python3 timelinejs3_local.py runserver` to run and open a new browser
window to view `index.html`.

## TODO
- Tests

## Changelog

### v0.1
- Initial commit

