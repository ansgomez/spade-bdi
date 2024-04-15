import asyncio
from datetime import datetime, timedelta

import spade
from spade.behaviour import PeriodicBehaviour, TimeoutBehaviour
from spade.template import Template

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

class MasterAgent(BDIAgent):
    async def setup(self):
        template = Template(metadata={"performative": "Modify"})
        self.add_behaviour(self.Modify(period=1, start_at=datetime.now()), template)

        template = Template(metadata={"performative": "Ending"})
        self.add_behaviour(self.RemoveBeliefsBehav(start_at=datetime.now() + timedelta(seconds=5)), template)

    class Modify(PeriodicBehaviour):
        async def run(self):
            if self.agent.bdi_enabled:
                try:
                    count_type = self.agent.bdi.get_belief_value("type")[0]
                    if count_type == 'inc':
                        self.agent.bdi.set_belief('type', 'dec')
                    else:
                        self.agent.bdi.set_belief('type', 'inc')
                except Exception as e:
                    self.kill()

    class RemoveBeliefsBehav(TimeoutBehaviour):
        async def run(self):
            self.agent.bdi.remove_belief('type', 'inc')
            self.agent.bdi.remove_belief('type', 'dec')


async def main():
    global serverSlave1, passwdSlave1, serverSlave2, passwdSlave2, serverMaster, passwdMaster
    b = BDIAgent(serverSlave1, passwdSlave1, "slave.asl")
    b.bdi.set_belief("master", serverMaster)
    await b.start()

    c = BDIAgent(serverSlave2, passwdSlave2, "slave.asl")
    c.pause_bdi()
    await c.start()

    a = MasterAgent(serverMaster, passwdMaster, "master.asl")
    a.bdi.set_belief("slave1", serverSlave1)
    a.bdi.set_belief("slave2", serverSlave2)
    a.bdi.set_belief('type', 'dec')
    await a.start()

    await asyncio.sleep(2)
    print("Enabling BDI for slave2")
    c.set_asl("slave.asl")
    c.bdi.set_belief("master", serverMaster)
    await asyncio.sleep(4)
    print("Disabling BDI for slave2")
    c.pause_bdi()

    await a.stop()
    await b.stop()
    await c.stop()


if __name__ == "__main__":
    global serverSlave1, passwdSlave1, serverSlave2, passwdSlave2, serverMaster, passwdMaster
    config = read_config('../config.txt')
    serverSlave1 = config['serverSlave1']
    passwdSlave1 = config['passwdSlave1']
    serverSlave2 = config['serverSlave2']
    passwdSlave2 = config['passwdSlave2']
    serverMaster = config['serverMaster']
    passwdMaster = config['passwdMaster']
    spade.run(main())
