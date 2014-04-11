#!/usr/bin/python
#

import sys, subprocess, getopt, dpkt, fcntl, os, struct, xml2json, optparse

dumpcfg=[]
tfile=""
odest=""

ff=open('patool.cfg','r')

def extract_packet_from_data(data):
    packet_end = data.find('</packet>')
    if packet_end != -1:
	packet_end+=len('</packet>')
	packet_start=data.find('<packet>')
	return data[packet_start:packet_end],data[packet_end:]
    return None,data

def packets_from_stdin(fd):
    data=""
    while True:
	new_data=fd.read(1000)
	data+=new_data
	packet, data=extract_packet_from_data(data)
	if packet:
	    return packet

def main():
    global tfile
    ix=0
    options=optparse.Values({"pretty":False})
    cmd=[]
    cmd.append('tcpdump')
    cmd.append('-w')
    cmd.append('-')
    cmd.append('-U')
    for item in dumpcfg:
	cmd.append(item)

    t=subprocess.Popen(cmd,bufsize=0,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    fdx=t.stdout.fileno()
    fl=fcntl.fcntl(fdx,fcntl.F_GETFL)
    fcntl.fcntl(fdx,fcntl.F_SETFL, fl | os.O_NONBLOCK)
    while True:
	tpkt=""
	try:
	    tpkt=t.stdout.read()
	except:
	    tpkt=""
	if tpkt!="":
	    if ix!=0:
		ai=0
		while ai<len(tpkt):
		    npkt=tpkt[ai+8:ai+12]
		    bi=struct.unpack('I',npkt)[0]
		    pkt=tpkt[ai+16:bi]
		    ai=ai+bi+16
		    fr=open(tfile,'wb')
		    ofr=dpkt.pcap.Writer(fr)
		    ofr.writepkt(pkt)
		    ofr.close()
		    fr=open("ex.pcap",'wb')
		    fr.write(tpkt)
		    fr.close()
		    p=subprocess.Popen(['tshark','-T','pdml','-r',tfile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		    packet=packets_from_stdin(p.stdout)
		    jpacket=xml2json.xml2json(packet,options,strip_ns=0)
		    if odest=="":
			print jpacket
		    else:
			fr=open(odest,"a")
			fr.write(jpacket)
			fr.close()
	    else: ix=1

if __name__ == '__main__':
    if len(sys.argv)>1:
	odest=sys.argv[1]
    for line in ff:
	a=line.split()
	if a[0]=='tcpdump':
	    b=len(a)
	    for c in range(1,b):
		dumpcfg.append(a[c])
	if a[0]=='common':
	    tfile=a[1]
    main()
