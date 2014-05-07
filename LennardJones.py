#!/usr/bin/env python

import sys

from fluid import LJContainer
import util

MEASUREMENT_STEPS = 10000
EQUILIBRIATION_STEPS = 2000

class LennardJones:

    t = 0.0

    def __init__(self, density):
        """Initialize the simulation."""

        #Initialize the container
        container = LJContainer(density)

        #Equilibriate the system
        while self.t < EQUILIBRIATION_STEPS:
            sys.stdout.write("\rEquilibriating the container: {0:3.1f}%".format(
                self.t*100/EQUILIBRIATION_STEPS))
            sys.stdout.flush()

            #Do one 'tick' consisting of two integrations and a force update
            container.tick(rescale=True)

            #Increment time
            self.t += 1

        print("\n")
        self.t = 0.0

        #Start measuring
        while self.t < MEASUREMENT_STEPS:
            sys.stdout.write("\rCalculating averages: {0:3.1f}%".format(
                self.t*100/MEASUREMENT_STEPS))
            sys.stdout.flush()

            #Do one 'tick' consisting of two integrations and a force update
            container.tick(rescale=True)

            #Sample averages
            container.sample(self.t)

            #Increment time
            self.t += 1

        #Store sampling data
        util.write_data(container.data, density)

        #Generate a plot of the measured properties
        util.generate_report(density)

        #Print out the average value for the pressure
        pressure = util.calculate_average(container.data, "P")

        #Write calculated pressure to disk
        util.store_pressure(pressure, density)

        print("\nAverage pressure for density {0}: {1:6.4}".format(
            density, pressure))

if __name__ == "__main__":
    lj = None
    for i in sys.argv:
        if i[:2] == "dn":
            lj = LennardJones(density=float(i[2:]))
    if not lj:
        print("Please specify density!")
