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

class CounterAgent(BDIAgent):
    async def setup(self):
        template = Template(metadata={"performative": "B1"})
        self.add_behaviour(self.UpdateCounterBehav(period=0.5, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B2"})
        self.add_behaviour(self.ResetCounterBehav(period=2, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B3"})
        self.add_behaviour(self.SwitchBeliefBehav(period=1, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B4"})
        self.add_behaviour(self.RemoveBeliefsBehav(start_at=datetime.now() + timedelta(seconds=4.5)), template)

    class UpdateCounterBehav(PeriodicBehaviour):
        async def on_start(self):
            self.counter = self.agent.bdi.get_belief_value("counter")[0]

        async def run(self):
            if self.counter != self.agent.bdi.get_belief_value("counter")[0]:
                self.counter = self.agent.bdi.get_belief_value("counter")[0]
                print(self.agent.bdi.get_belief("counter"))

    class ResetCounterBehav(PeriodicBehaviour):
        async def run(self):
            self.agent.bdi.set_belief('counter', 0)

    class SwitchBeliefBehav(PeriodicBehaviour):
        async def run(self):
            try:
                type = self.agent.bdi.get_belief_value("type")[0]
                if type == 'inc':
                    self.agent.bdi.set_belief('type', 'dec')
                else:
                    self.agent.bdi.set_belief('type', 'inc')
            except Exception as e:
                print("No belief 'type'.")

    class RemoveBeliefsBehav(TimeoutBehaviour):
        async def run(self):
            self.agent.bdi.remove_belief('type', 'inc')
            self.agent.bdi.remove_belief('type', 'dec')


async def main():
    global server, passwd

    a = CounterAgent(server, passwd, "counter.asl")
    await a.start()

    await asyncio.sleep(5)
    await a.stop()


if __name__ == "__main__":
    global server, passwd
    config = read_config('../config.txt')
    server = config['server']
    passwd = config['passwd']

    spade.run(main())
