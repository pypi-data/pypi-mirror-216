# metarace-roadmeet

Timing and result application for UCI Part 2 Road Races,
UCI Part 5 Cyclo-Cross, criterium, road handicap and
ad-hoc time trial events.

![roadmeet screenshot](screenshot.png "roadmeet")

## Requirements

   - Python >= 3.9
   - Gtk >= 3.0
   - metarace >= 2.1.1
   - tex-gyre fonts (optional, recommended)
   - evince (optional, recommended)
   - mosquitto (optional)


## Installation

### Debian 11+

Install system requirements for roadmeet and metarace with apt:

	$ sudo apt install python3-venv python3-pip python3-cairo python3-gi python3-gi-cairo
	$ sudo apt install gir1.2-gtk-3.0 gir1.2-rsvg-2.0 gir1.2-pango-1.0 tex-gyre
	$ sudo apt install python3-serial python3-paho-mqtt python3-dateutil python3-xlwt

If not already created, add a virtualenv for metarace packages:

	$ mkdir -p ~/Documents/metarace
	$ python3 -m venv --system-site-packages ~/Documents/metarace/venv

Activate the virtualenv and install ttstart with pip:

	$ source ~/Documents/metarace/venv/bin/activate
	(venv) $ pip3 install metarace-roadmeet

