import asyncio

import agentspeak
import spade

from spade_bdi.bdi import BDIAgent

def strip_comments(line, delimiters=('#', ';')):
    for delimiter in delimiters:
        line = line.split(delimiter, 1)[0]
    return line.strip()

def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            original_line = line.strip()
            if not original_line or original_line[0] in ['#', ';']:
                continue  # Skip comment lines and empty lines
            line = strip_comments(original_line)
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
        return config

async def main():
    global serverSender, passwdSender, serverReceiver, passwdReceiver
    b = BDIAgent(serverReceiver, passwdReceiver, "receiver.asl")
    b.bdi.set_belief("sender", serverSender)
    await b.start()

    a = BDIAgent(serverSender, passwdSender, "sender.asl")
    a.bdi.set_belief("receiver", serverReceiver)
    await a.start()

    await asyncio.sleep(5)

    await b.stop()
    await a.stop()


if __name__ == "__main__":
    global serverSender, passwdSender, serverReceiver, passwdReceiver
    config = read_config('../config.txt')
    serverSender = config['serverSender']
    passwdSender = config['passwdSender']
    serverReceiver = config['serverReceiver']
    passwdReceiver = config['passwdReceiver']

    spade.run(main())
