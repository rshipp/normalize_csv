# CSV Normalization

## Setup

1. On Ubuntu 16.04 LTS, install Python 3.6 and `pip` following [these steps][1],
   or by some other means.
2. Install pytz: `pip3 install pytz`.

## Usage

Run the script, redirecting stdin to the input file:

    ./normalize_csv.py < FILENAME

or

    cat FILENAME | ./normalize_csv.py

[1]: https://stackoverflow.com/questions/42662104/how-to-install-pip-for-python-3-6-on-ubuntu-16-10/44254088#44254088
