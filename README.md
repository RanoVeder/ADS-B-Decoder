# ADS-B-Decoder

This ADS-B Decoder is developed as a bonus assignment for the class "AE1205, Programming & Scientific Computing in Python" at the TU Delft.

To run this program, a rtl-sdr is needed, which can be found [*here*.](http://www.dx.com/en/p/rtl2832u-r820t-mini-dvb-t-dab-fm-usb-digital-tv-dongle-black-170541#.Vzcxk3V955F)

Before starting, the following dependencies will have to be installed:

* Python 2.7.x
* [pyrtlsdr](https://github.com/roger-/pyrtlsdr)
* [numpy](http://www.numpy.org/)
* [cherrypy](http://www.cherrypy.org/)
* [pyqt4](https://www.riverbankcomputing.com/software/pyqt/download)

After which the program can be run by executing 'Main.py'.


A huge thanks to [Junzi Sun's ADS-B decoding guide](http://adsb-decode-guide.readthedocs.io/en/latest/). This helped us enormously in easily decoding the received ADS-B messages.


This program was made by Rano Veder and Vincent Meijer.
