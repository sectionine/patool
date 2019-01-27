patool
======

python script for running tcpdump and pipe output to tshark to convert pcap to either xml or json format and then print to either file or stdout. tcpdump and tshark run on thier own processes, and buffer works for persistent non-stop captures (haven't tested with saturated input, but could fail depending on cpu and mem available). Could have included pypcap to better handle cpu resource, but it's a nightmare to install on various distros. Working on adding logstash and elasticsearch / kibana instructions and config file examples.

Aaron Connell
aaron.a.connell@gmail.com
317-847-5091

Dependencies/Prerequisites:
dpkt-1.8 - http://code.google.com/p/dpkt/downloads/list
python 2.6+ - https://www.digitalocean.com/community/articles/how-to-set-up-python-2-7-6-and-3-3-3-on-centos-6-4
tshark (wireshark cli) - http://pkgs.org/download/wireshark 
tcpdump - http://www.tcpdump.org
libpcap - http://www.tcpdump.org

Python Script Files:
patool_xml.py - used for xml output via stdout, or xml output to file
patool_json.py - used for json output via stdout, or json output to file
xml2json.py - called with patool_json.py to convert xml to json
patool.cfg - use to set tcpdump variables and buffered test.pcap file

Configure patool.cfg:
*Edit patool.cfg before use

You can configure any standard tcpdump switches in this file. The current config shows:
tcpdump -i eth0 -s0 host 0.0.0.0 and port 12345
common buffer_file.pcap

This current configuration example will capture using interface (-i) eth0 (without this switch tcpdump will default to the lowest eth device which is usually eth0 anyway), and won't truncate packet size (-s0), and will only capture host ip address 0.0.0.0 on port 12345.
The common (buffered) capture output will be buffer_file.pcap. This file is not normally used, however is require for script functionality.

You can use the -c switch to limit packet count (and similar switches such as file size) (i.e. -c 10000 to limit to 10000 packets), however, you will need to manually stop the process when the buffer file stops building (as well as monitor the output file build size if using output file option and not stdout as default). This can be a bit tricky and depends on amount of traffic being captured and filters used in tcpdump, etc.

Usage:
*All scripts must be ran as root in order to function. Examples are from CentOS 6.
*Suggest placing all script files in directory like /var/tmp/patool/
*All script files will need to be made executable (#chmod +x filename.py)
*All dependencies need to be installed prior to executing scripts
*patool.cfg needs edited before use (i.e. host is 0.0.0.0 and port 12345 can be edited or removed to get all ip's and ports) in order to work correctly (#vi patool.cfg / then do "Esc : w! Enter" to save / then do "Esc : q Enter" to quit back to shell)

Run the process:
"sudo -s ./patool_xml.py" - prints real-time output to stdout in xml format from packet to /packet
"sudo -s ./patool_xml.py" outputfile.xml - will write an .xml file (no xml header or xml close tag included)
"sudo -s ./patool_json.py" - prints real-time output to stdout in json format (xml header and close tag included for each packet to /packet then output via xml2json script is printed without error)
"sudo -s ./patool_json.py outputfile.json" - will write an .json file (xml header and close tag included for each packet to /packet then output via xml2json script is printed without error)

Stop the process: 
"ctrl + z"

Notes:
You will need to manually stop the process when finished (i.e. want to stop capturing packets, or file output was used and want to stop the printing of additional packets to the file)

Upcoming experiments:
Working on stdin using logstash and output from logstash to elasticsearch and kibana for GUI. Will include scripts, configuration files, instruction for making this work.


