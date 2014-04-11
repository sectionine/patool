patool
======

python script for running tcpdump and pipe output to tshark to convert pcap to either xml or json format and then print to either file or stdout. tcpdump and tshark run on thier own processes, and buffer works for persistent non-stop captures (haven't tested with saturated input, but could fail depending on cpu and mem available). Could have included pypcap to better handle cpu resource, but it's a nightmare to install on various distros. Working on adding logstash and elasticsearch / kibana instructions and config file examples.

Aaron Connell
aaron.a.connell@gmail.com
