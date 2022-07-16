### XMLTV
> Shows a list of TV programs that can be watched from the beginning, not from the middle.
> 
> Meaning, only shows that either started no more than 5 minutes ago, or will start within 10 minutes, that is, in the 15 minute range are displayed (Based on the settings for begging)

![Illustration](https://github.com/alexander1one1/xmltv/raw/master/xmltv.gif)
## Usage
The download of a new base is forced by the -f switch, or if it is not in the main directory.
Available commands:
```
optional arguments:
  -h, --help            show this help message and exit
  --xmltv_link_arch XMLTV_LINK_ARCH, -a XMLTV_LINK_ARCH
                        link of archive with xmltv
  --force_download FORCE_DOWNLOAD, -f FORCE_DOWNLOAD
                        force download archive even exist. 0 - disabled, 1 - enabled
  --timezone TIMEZONE, -t TIMEZONE
                        timezone from GMT (wo +)
  --target_minutes_ending TARGET_MINUTES_ENDING, -e TARGET_MINUTES_ENDING
                        minutes to end show
  --target_minutes_begining TARGET_MINUTES_BEGINING, -b TARGET_MINUTES_BEGINING
                        minutes to begin show
  --use_m3u USE_M3U, -p USE_M3U
                        Use m3u playlist file. 0 - disabled, 1 - enabled

```
The `timezone` does not work now, the data is taken from the TV program.

`--use_m3u` makes sense when run with `--force_download`, this writes the list of channels from the first found playlist in the directory to a text file in the `lists` directory.

In the same directory there are text files with stop words.

### The default values are:
  --xmltv_link_arch _first in `list_archives_tvprogram_link` in `settings.py`_

  --force_download _`0`_

  --timezone _`3`_

  --target_minutes_ending _`5`_

  --target_minutes_begining _`10`_

  --use_m3u _`0`_

### Examples of use:

Data output with recreate database:

`$ python3 main.py -f 1`

Data output with recreate database with channels in playlist (m3u file in directory require):

`$ python3 main.py -f 1 -p 1`

Data output with changed time parameters (-2 <= time_now <= 5):

`$ python3 main.py -e 2 -b 5`

Data output with default options:

`$ python3 main.py`

## Installation

```
git clone https://github.com/alexander1one1/xmltv.git
cd xmltv
pip3 install -r requirements.txt
```

Or just pip instead pip3 for windows