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
    global server, passwd
    a = BDIAgent(server, passwd, "basic.asl")

    await a.start()

    a.bdi.set_belief("moto", "amarillo")
    a.bdi.set_belief("car", "azul")

    await asyncio.sleep(1)
    await a.stop()

    a.bdi.remove_belief("truck", "azul")
    print(a.bdi.get_beliefs())

if __name__ == "__main__":
    global server, passwd
    config = read_config('../config.txt')
    server = config['server']
    passwd = config['passwd']

    spade.run(main())
