#!/usr/bin/env python

import sys

from fluid import LJContainer
import util

STEPS = 1000

class LennardJones:

    t = 0.0

    def __init__(self, density=0.8):

        #Initialize the container
        container = LJContainer(density)

        #Generate forces for the initial configuration
        #container.update_forces()

        #Equilibriate the system
        #container.equilibriate()

        #Start measuring
        while self.t < STEPS:
            sys.stdout.write("\rCalculating: {0:3.1f}%".format(self.t*100/STEPS))
            sys.stdout.flush()

            #Do one 'tick' consisting of two integrations and a force update inbetween
            container.tick()

            #Sample averages
            container.sample(self.t)

            self.t += 1

        #Store sampling data
        util.write_data(container.data)

        #Generate a plot of the energies (kinetic, potential, total)
        util.generate_report(0)

if __name__ == "__main__":
    lj = None
    for i in sys.argv:
        if i[:2] == "dn":
            lj = LennardJones(density=float(i[2:]))
    if not lj:
        LennardJones()
