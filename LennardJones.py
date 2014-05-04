#!/usr/bin/env python

import sys

from fluid import LJContainer
import util

PARTICLES = 108
TEMPERATURE = 2.0
DENSITY = 0.8442
TIME_STEP = 0.004
STEPS = 10000

class LennardJones:

    t = 0.0

    def __init__(self, timestep=TIME_STEP):

        #Initialize the container
        container = LJContainer(PARTICLES, DENSITY, TEMPERATURE)

        #Generate forces for the initial configuration
        #container.update_forces()

        #Equilibriate the system
        #container.equilibriate()

        #Start measuring
        while self.t < STEPS:
            sys.stdout.write("\rCalculating: {0:3.1f}%".format(self.t*100/STEPS))
            sys.stdout.flush()

            #Do one 'tick' consisting of two integrations and a force update inbetween
            container.tick(timestep)

            #Sample averages
            container.sample(self.t)

            self.t += 1

        #Store sampling data
        util.write_data(container.data)

        #Generate a plot of the energies (kinetic, potential, total)
        util.generate_report(timestep)

if __name__ == "__main__":
    lj = None
    for i in sys.argv:
        if i[:2] == "dt":
            lj = LennardJones(timestep=float(i[2:]))
    if not lj:
        LennardJones()
