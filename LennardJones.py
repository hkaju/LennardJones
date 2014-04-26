#!/usr/bin/env python

from fluid import LJContainer

PARTICLES = 108
TEMPERATURE = 0.728
DENSITY = 0.8442
TIME_STEP = 0.001
STEPS = 20

class LennardJones:

    t = 0

    def __init__(self):
        #Initialize the container
        container = LJContainer(PARTICLES, DENSITY, TEMPERATURE)
        #print container.generate_velocities(2)
        #Equilibriate the system
        #Start measuring
        while self.t < STEPS:
            container.reset_forces()
            container.update_forces()
            container.tick(TIME_STEP)
            container.sample(self.t)
            self.t += TIME_STEP
            #Sample averages
        #print container.data
        container.write_particles()
        f = open("output.csv", "w")
        f.write("t,K,V,T\n")
        for item in range(len(container.data["t"])):
            f.write("{0},{1},{2},{3}\n".format(container.data["t"][item], container.data["K"][item],
                container.data["V"][item], container.data["T"][item]))
        f.close()
        #Generate a plot of the energies (kinetic, potential, total)

if __name__ == "__main__":
    LennardJones()
