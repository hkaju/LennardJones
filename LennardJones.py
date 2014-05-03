#!/usr/bin/env python

import sys

from fluid import LJContainer

PARTICLES = 108
TEMPERATURE = 0.728
DENSITY = 0.8442
TIME_STEP = 0.005
STEPS = 3000

class LennardJones:

    t = 0.0

    def __init__(self):
        #Initialize the container
        container = LJContainer(PARTICLES, DENSITY, TEMPERATURE)
        #Equilibriate the system
        #Start measuring

        while self.t < STEPS:
            sys.stdout.write("\rCalculating: {0:3.1f}%".format(self.t*100/STEPS))
            sys.stdout.flush()
            container.tick(TIME_STEP)
            container.sample(self.t)
            self.t += 1
            #Sample averages
        f = open("output.csv", "w")
        f.write("t,K,V,T,P\n")
        for item in range(len(container.data["t"])):
            f.write("{0},{1},{2},{3},{4}\n".format(container.data["t"][item], container.data["K"][item],
                container.data["V"][item], container.data["T"][item], container.data["P"][item]))
        f.close()
        #Generate a plot of the energies (kinetic, potential, total)

if __name__ == "__main__":
    LennardJones()
