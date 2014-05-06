import copy
import random
import math

PARTICLES = 108
TEMPERATURE = 2.0
DENSITY = 0.8
TIME_STEP = 0.001
ANDERSEN_FREQUENCY = 0.01
CUTOFF = 2.5

class Particle:

    #Particle properties
    position = [0, 0, 0]
    previous_position = None
    velocity = [0, 0, 0]
    force = [0, 0, 0]
    potential = 0

    def __init__(self, position, velocity, dt):
        """Initialize the particle with given position and velocity."""

        self.position = position
        self.velocity = velocity
        x = self.position[0] - self.velocity[0]*dt
        y = self.position[1] - self.velocity[1]*dt
        z = self.position[2] - self.velocity[2]*dt
        self.previous_position = [x, y, z]

    def get_squared_velocity(self):
        """Get the square of the velocity."""

        sumv2 = 0
        for n in range(len(self.velocity)):
            sumv2 += self.velocity[n]**2

        return sumv2

    def get_force(self):
        """Get the resultant force on the particle."""

        force = math.sqrt(self.force[0]**2 + self.force[1]**2 + self.force[2]**2)

        return force

class LJContainer:

    particles = []
    temperature = 0
    density = 0
    length = 0
    nu = ANDERSEN_FREQUENCY
    data = {"t" : [],
            "K" : [],
            "V" : [],
            "T" : [],
            "P" : [],
            "temp" : []}

    def __init__(self, density):
        """Set up the container."""

        #Calculate container dimensions from the density
        #Particle radius is set to 1
        self.length = (PARTICLES * 4.0/3.0 * math.pi / density)**(1.0/3)
        self.temperature = TEMPERATURE
        self.density = density
        self.timestep = TIME_STEP
        #Initialize particles
        self.initialize(PARTICLES, TIME_STEP)

    def initialize(self, number_of_particles, dt):
        """Initialize the container with particles."""

        #Calculate the spacing between particles
        spacing = self.length / 6.0

        #Generate starting velocities
        velocities = self.generate_velocities(number_of_particles)

        for n in range(number_of_particles):
            #Start with 3 layers of 6x6 particles
            x = (n%6 + 1) * spacing
            y = ((n-(n/36)*36)/6 + 1) * spacing
            z = (n/36 + 1) * spacing

            position = [x, y, z,]
            velocity = velocities.pop()
            particle = Particle(position, velocity, dt)

            self.particles.append(particle)

    def generate_velocities(self, number_of_particles):
        """Generate an initial velocity distribution of number_of_particles velocities."""

        dimensions = 3

        velocities = []
        vtot = [0] * dimensions
        v2tot = [0] * dimensions
        fs = [0] * dimensions

        #Generate velocities from a uniform distribution
        for i in range(number_of_particles):
            v = [0] * dimensions
            v2 = [0] * dimensions
            for d in range(dimensions):
                vn = random.uniform(-0.5, 0.5)
                v[d] = vn
                v2[d] = vn**2
                vtot[d] += vn
                v2tot[d] += vn**2
            velocities.append(v)

        #Calculate total velocity and scaling factor
        for d in range(dimensions):
            vtot[d] = vtot[d] / number_of_particles
            v2tot[d] = v2tot[d] / number_of_particles
            fs[d] = math.sqrt(self.temperature / v2tot[d])

        #Scale and shift velocities
        for i in range(number_of_particles):
            vn = [0] * dimensions
            for d in range(dimensions):
                vn[d] = (velocities[i][d] - vtot[d]) * fs[d]
            velocities[i] = vn

        return velocities

    def update_forces(self):
        """Update forces on all particles."""

        #Reset before generating new forces
        self.reset_particles()

        #Calculate cutoff potential
        rc = 2.5
        ecut = 4 * ((1/rc)**12 - (1/rc)**6)

        for i in range(0, len(self.particles) - 1):
            for j in range(i, len(self.particles)):
                if i != j:
                    dn = [self.particles[i].position[0] - self.particles[j].position[0],
                          self.particles[i].position[1] - self.particles[j].position[1],
                          self.particles[i].position[2] - self.particles[j].position[2]]
                    #Enforce PBC
                    dn[0] = dn[0] - self.length*round(dn[0]/self.length)
                    dn[1] = dn[1] - self.length*round(dn[1]/self.length)
                    dn[2] = dn[2] - self.length*round(dn[2]/self.length)

                    r2 = dn[0]**2 + dn[1]**2 + dn[2]**2
                    if r2 < rc**2:
                        r2i = 1/r2
                        r6i = r2i**3
                        u = 4 * r6i * (r6i - 1) - ecut
                        f = 48 * r2i * r6i * (r6i - 0.5)
                        self.particles[i].potential += u
                        self.particles[j].potential += u
                        for d in range(3):
                            self.particles[i].force[d] += f*dn[d]
                            self.particles[j].force[d] -= f*dn[d]

    def tick(self, rescale=False):
        """Perform one time step of the system."""

        #Andersen thermostat step 1
        self.update_positions(self.timestep, Andersen_phase=1)
        #Update forces
        self.update_forces()
        #Andersen thermostat step 2
        self.update_positions(self.timestep, Andersen_phase=2)

        #Rescale velocities
        if rescale:
            self.rescale()

    def rescale(self):
        """Rescale the velocities to match set temperature."""

        scale_factor = [0] * 3
        v2tot = [0] * 3
        for particle in self.particles:
            for dim in range(3):
                v2tot[dim] += particle.velocity[dim]**2
        for dim in range(3):
            v2tot[dim] = v2tot[dim] / len(self.particles)
            scale_factor[dim] = math.sqrt(self.temperature / v2tot[dim])
        for particle in self.particles:
            for dim in range(3):
                particle.velocity[dim] = particle.velocity[dim] * scale_factor[dim]

    def update_positions(self, dt, Andersen_phase=1):
        """Update the position of the particle according to the velocity Verlet algorithm."""

        if Andersen_phase == 1:
            for p in self.particles:
                for n in range(len(p.position)):
                    p.position[n] = p.position[n] + dt*p.velocity[n] + 0.5*p.force[n]*dt**2
                    p.position[n] = p.position[n] % self.length
                    p.velocity[n] = p.velocity[n] + 0.5*dt*p.force[n]
        elif Andersen_phase == 2:
            insttemp = 0
            for p in self.particles:
                for n in range(len(p.position)):
                    p.velocity[n] = p.velocity[n] + 0.5*dt*p.force[n]
                    insttemp += p.velocity[n]**2
            insttemp = insttemp/(3.0 * len(self.particles))
            sigma = math.sqrt(self.temperature)
            for p in self.particles:
                if random.uniform(0, 1) < self.nu*dt:
                    for n in range(len(p.position)):
                        p.velocity[n] = random.gauss(0, sigma)

    def reset_particles(self):
        """Reset forces and potential energy on all particles."""

        #Calculate tail correction for the energy
        rc = 2.5
        tail = 8.0/9.0 * math.pi * self.density * ((1/rc)**9 - 3*(1/rc)**3)

        for i in range(len(self.particles)):
            force = [0] * 3
            #Reset forces
            self.particles[i].force = force
            #Reset potential energy to tail correction
            self.particles[i].potential = tail

    def get_current_temperature(self):
        """Calculate instantaneous temperature."""

        K = 0
        #Calculate kinetic energy
        for particle in self.particles:
            K += particle.get_squared_velocity()
        #Get temperature from kinetic energy and degrees of freedom
        T = K / (3.0*len(self.particles))

        return T

    def sample(self, time):
        """Sample ensemble properties."""

        rc = 2.5
        Ptail = 32.0/9.0 * math.pi * self.density**2 *((1/rc)**9 - 3.0/2.0 * (1/rc)**3)
        self.data["t"].append(time)
        K = 0
        V = 0
        F = 0
        for particle in self.particles:
            K += particle.get_squared_velocity()
            V += particle.potential
            F += particle.get_force()
        #Calculate average force per particle
        F = F/len(self.particles)
        #Calculate pressure
        P = self.density * self.get_current_temperature() + 1/(3*self.length**3)*0.5*F
        self.data["K"].append(K/len(self.particles))
        self.data["V"].append(V/len(self.particles))
        self.data["T"].append((K + V)/len(self.particles))
        self.data["P"].append(P + Ptail)
        self.data["temp"].append(self.get_current_temperature())
