import asyncio
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
    global serverSlave1, passwdSlave1, serverMaster, passwdMaster
    b = BDIAgent(serverSlave1, passwdSlave1, "slave.asl")
    b.bdi.set_belief("master", serverMaster)
    await b.start()

    a = BDIAgent(serverMaster, passwdMaster, "master.asl")
    a.bdi.set_belief("slave1", serverSlave1)
    await a.start()

    await asyncio.sleep(2)
    await a.stop()
    await b.stop()

if __name__ == "__main__":
    global serverSlave1, passwdSlave1, serverMaster, passwdMaster
    config = read_config('../config.txt')
    serverSlave1 = config['serverSlave1']
    passwdSlave1 = config['passwdSlave1']
    serverMaster = config['serverMaster']
    passwdMaster = config['passwdMaster']
    spade.run(main())

