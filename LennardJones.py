#!/usr/bin/env python

import sys

from fluid import LJContainer
import util

PARTICLES = 108
TEMPERATURE = 0.728
DENSITY = 0.8442
TIME_STEP = 0.005
STEPS = 3000

class LennardJones:

    t = 0.0

    def __init__(self, timestep=TIME_STEP):
        #Initialize the container
        container = LJContainer(PARTICLES, DENSITY, TEMPERATURE)
        #Equilibriate the system
        #Start measuring
        while self.t < STEPS:
            sys.stdout.write("\rCalculating: {0:3.1f}%".format(self.t*100/STEPS))
            sys.stdout.flush()
            container.tick(timestep)
            container.sample(self.t)
            self.t += 1
            #Sample averages
        util.write_data(container.data)
        util.generate_report(timestep)
        #Generate a plot of the energies (kinetic, potential, total)

if __name__ == "__main__":
    lj = None
    for i in sys.argv:
        if i[:2] == "dt":
            lj = LennardJones(timestep=float(i[2:]))
    if not lj:
        LennardJones()
