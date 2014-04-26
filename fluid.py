import copy
import random
import math

DEBUG = True

class Particle:

    #Particle properties
    position = [0, 0, 0]
    previous_position = None
    velocity = [0, 0, 0]
    force = [0, 0, 0]
    potential = 0

    def __init__(self, position, velocity):
        """Initialize the particle with given position and velocity."""

        self.position = position
        self.velocity = velocity

    def update_position(self, dt):
        """Update the position of the particle according to the Verlet algorithm."""

        #If this is the first time the particle moves, generate a previous position
        #based on current speed
        if not self.previous_position:
            x = self.position[0] - self.velocity[0]*dt
            y = self.position[1] - self.velocity[1]*dt
            z = self.position[2] - self.velocity[2]*dt
            self.previous_position = [x, y, z]

        #Calculate updated position and velocity
        next_position = []
        next_velocity = []
        for n in range(len(self.position)):
            dq = 2*self.position[n] - self.previous_position[n] + self.force[n]*dt**2
            dv = (dq - self.previous_position[n])/(2*dt)
            next_position.append(dq)
            next_velocity.append(dv)

        #Update particle properties
        self.previous_position = copy.deepcopy(self.position)
        self.position = next_position
        self.velocity = next_velocity

    def get_squared_velocity(self):
        """Get the square of the velocity."""

        sumv2 = 0
        for n in range(len(self.velocity)):
            sumv2 += self.velocity[n]**2
        return sumv2

class LJContainer:

    particles = []
    temperature = 0
    density = 0
    length = 0
    data = {"t" : [],
            "K" : [],
            "V" : [],
            "T" : []}

    def __init__(self, number_of_particles, density, temperature):
        self.length = (number_of_particles * 4.0/3.0 * math.pi / density)**(1.0/3)
        self.temperature = temperature
        self.density = density
        self.initialize(number_of_particles)
        #self.write_particles()

    def write_particles(self):
        f = open("grid.csv", "w")
        f.write("x,y,z\n")
        for particle in self.particles:
            f.write("{0},{1},{2}\n".format(particle.position[0], particle.position[1], particle.position[2]))
        f.close()

    def initialize(self, number_of_particles):
        """Initialize the container."""

        #Calculate the spacing between particles
        spacing = self.length / 6.0
        velocities = self.generate_velocities(number_of_particles)

        for n in range(number_of_particles):
            #Start with 3 layers of 6x6 particles
            x = (n%6 + 1) * spacing
            y = ((n-(n/36)*36)/6 + 1) * spacing
            z = (n/36 + 1) * spacing

            position = (x, y, z,)
            velocity = velocities.pop()
            particle = Particle(position, velocity)
            self.particles.append(particle)

    def generate_velocities(self, number_of_particles):
        """Generate an initial velocity distribution of number_of_particles velocities."""

        dimensions = 3

        velocities = []
        vtot = [0] * dimensions
        v2tot = [0] * dimensions
        fs = [0] * dimensions

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
        for d in range(dimensions):
            vtot[d] = vtot[d] / number_of_particles
            v2tot[d] = v2tot[d] / number_of_particles
            fs[d] = math.sqrt(self.temperature / v2tot[d])
        for i in range(number_of_particles):
            vn = [0] * dimensions
            for d in range(dimensions):
                vn[d] = (velocities[i][d] - vtot[d]) * fs[d]
            velocities[i] = vn

        if DEBUG:
            vtot = [0] * dimensions
            v2tot = [0] * dimensions
            for item in velocities:
                for dim in range(len(item)):
                    vtot[dim] += item[dim]
                    v2tot[dim] += item[dim]**2
            for dim in range(dimensions):
                v2tot[dim] = v2tot[dim] / number_of_particles
            print vtot, v2tot

        return velocities

    def update_forces(self):
        rc2 = 2.5**2
        ecut = 4 * ((1/2.5)**12 - (1/2.5)**6)
        for i in range(0, len(self.particles) - 1):
            for j in range(i, len(self.particles)):
                if i != j:
                    dn = [self.particles[i].position[0] - self.particles[j].position[0],
                          self.particles[i].position[1] - self.particles[j].position[1],
                          self.particles[i].position[2] - self.particles[j].position[2]]
                    dn[0] = dn[0] - self.length*round(dn[0]/self.length)
                    dn[1] = dn[1] - self.length*round(dn[1]/self.length)
                    dn[2] = dn[2] - self.length*round(dn[2]/self.length)
                    r2 = dn[0]**2 + dn[1]**2 + dn[2]**2
                    if r2 < rc2:
                        r2i = 1/r2
                        r6i = r2i**3
                        u = 4 * r6i * (r6i - 1)  - ecut
                        f = 48 * r2i * r6i * (r6i - 0.5)
                        self.particles[i].potential += u
                        self.particles[j].potential += u
                        for d in range(3):
                            self.particles[i].force[d] += f*dn[d]
                            self.particles[j].force[d] -= f*dn[d]

    def tick(self, time_step):
        for p in self.particles:
            p.update_position(time_step)

    def reset_forces(self):
        for i in range(len(self.particles)):
            force = [0] * 3
            self.particles[i].force = force
            self.particles[i].potential = 0

    def sample(self, time):
        self.data["t"].append(time)
        K = 0
        V = 0
        for particle in self.particles:
            K += particle.get_squared_velocity()
            V += particle.potential
        self.data["K"].append(K/len(self.particles))
        self.data["V"].append(V/len(self.particles))
        self.data["T"].append((K + V)/len(self.particles))
