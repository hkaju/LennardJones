#!/usr/bin/env python

from fluid import LJContainer

PARTICLES = 108.0
TEMPERATURE = 2.0
DENSITY = 1.0
TIME_STEP = 0.001
STEPS = 2000

class LennardJones:

    _t = 0

    def __init__(self):
        #Initialize the container
        container = LJContainer(PARTICLES, DENSITY, TEMPERATURE)
        #Equilibriate the system
        #Start measuring
        while self._t < STEPS:
            #Calculate the forces
            #Integrate equations of motion
            self._t += TIME_STEP
            #Sample averages
        #Generate a plot of the energies (kinetic, potential, total)

if __name__ == "__main__":
    LennardJones()
