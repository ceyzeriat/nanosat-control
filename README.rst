.. NanoCTRL

Dear radio-amateur, if you are interested in unpacking the raw-frames of the PICSAT mission, you are (almost) at the right place. Please have a read here: https://github.com/ceyzeriat/nanosat-control/issues/1

:Name: NanoCTRL
:Website: `www.nanosat-control.com`_
:Author: Guillaume Schworer
:Version: 0.1beta

.. Ground-Segment Software for CubeSats

What is NanoCTRL?
=================

NanoCTRL is a Ground Segment Software (GSS) which allows the listening, decoding, and storage of the satellite downlink data, as well as the sending of commands in order to control the satellite in real-time.

It is designed to be a ground segment framework for nano-satellite projects primarely, as it may not cope well with large dowlink rates (>1 Mbytes/sec) or complex systems inter-dependencies.

It shows in real-time the telecommands (TC), their acknowledgements, and telemetries (TM) which transit through the antenna.

It decodes the TC/TM in real-time and saves them to a database, as well as on a hard-drive (local or server-based).

It forwards all TCs and TMs to a port, encoded in standard data-format: any third-party application can retrieve this information, or query the database, in order to provide additional functionality.


What it is not
==============

NanoCTRL is not a turnkey solution to communicate with a satellite: having a couple of walky-talky does not ensure good communication as there is the language barrier. This software is a framework that requires substantial parametrization, based on a communication protocol (CCSDS) that should be customized to the specific needs of the mission. Don’t think you can get away without such communication protocol, though; any satellite that reacts on specific commands needs one.

This software is no hardware: it reads and writes bytes from/to a port (serial, usb, tcp/ip), and this is where it interfaces with hardware, e.g. Terminal Node Controller (TNC).

It does not control the antenna nor predicts the next transit, which is `Gpredict`_‘s task.

Don't forget to check out the website: `www.nanosat-control.com`_.

.. _`www.nanosat-control.com`: http://www.nanosat-control.com/
.. _`Gpredict`: http://gpredict.oz9aec.net/
