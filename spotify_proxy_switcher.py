#imports
import urllib2
import json
import psutil
import os
import signal
import subprocess


#set your path for prefs file
file = '/Users/changeme/Library/Application Support/Spotify/prefs'
#Set Your country
country = "GB"
protocol1 = "socks5"
protocol2 = "socks4"
#Proxy-list
proxy="https://api.getproxylist.com/proxy?country[]=%s&protocol[]=%s&protocol[]=%s" % (country,protocol1,protocol2)
#proxy2="http://gimmeproxy.com/api/getProxy?country=%s" % country


#//TO DO:
#1.add support for changing network.proxy.mode in case of protocol version: done
#2.add support for universal proxy-list


info = []


def get_socks5_json(url):
    content = urllib2.urlopen(url).read()
    return content


def parse_socks5_json():
    x = get_socks5_json(proxy)
    j = json.loads(x)
    ip = j['ip']
    port = j['port']
    protocol = j['protocol']

    if protocol == "socks5":
        npm = "4"
    elif protocol == "socks4":
        npm = "3"
    elif protocol == "http":
        npm = "2"
    npa = str(ip) + ":" + str(port) + "@" + str(protocol)
    info.append(npa)
    info.append(npm)
    return info


def convert_prefs(prefs):
    parse_socks5_json()
    dictionary = dict(line.strip().split('=') for line in open(prefs))
    dictionary['network.proxy.mode'] = info[1]
    dictionary['network.proxy.addr'] = "\"" + info[0] + "\""
    return dictionary


def write_prefs(prefs2):
    d = convert_prefs(file)
    os.remove(file)
    new_prefs = open(prefs2, 'w')
    for k,v in d.items():
        new_prefs.write(k + "=" + v + "\n")
    new_prefs.close()


#write_prefs(file)


def kill_spotify():
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name() == "Spotify":
            os.kill(p.pid, signal.SIGTERM)


def start_spotify():
    subprocess.call(
        ["/usr/bin/open", "-W", "-n", "-a", "/Applications/Spotify.app"]
    )


def main():
    kill_spotify()
    write_prefs(file)
    start_spotify()


main()

