import copy
import random
import math

class Particle:

    #Particle properties
    _position = (0, 0, 0,)
    _previous_position = (0, 0, 0,)
    _velocity = (0, 0, 0,)
    _force = (0, 0, 0,)

    def __init__(self, position, velocity):
        """Initialize the particle with given position and velocity."""

        self._position = position
        self._velocity = velocity

    def set_force_to(self, force):
        self._force = force

    def update_position(self, dt):
        """Update the position of the particle according to the Verlet algorithm."""

        next_position = []
        next_velocity = []
        for n in len(self._position):
            dq = 2*self._position[n] - self._previous_position[n] + self._force[n]*dt**2
            dv = (dq - self._previous_position[n])/(2*dt)
            next_position.append(dq)
            next_velocity.append(dv)
        self._previous_position = copy.deepcopy(self._position)
        self._position = tuple(next_position)
        self._velocity = tuple(next_velocity)

    def get_squared_velocity(self):
        """Get the square of the velocity."""

        sumv2 = 0
        for n in len(self._velocity):
            sumv += self._velocity[n]**2
        return sumv2

class LJContainer:

    _particles = []
    _temperature = 0
    _density = 0
    _length = 0

    def __init__(self, number_of_particles, density, temperature):
        self._length = (number_of_particles / density)**(1.0/3)
        self._temperature = temperature
        self._density = density
        #self.initialize(number_of_particles)
        self.generate_velocities(108)
        #print(self._length)

    def initialize(self, number_of_particles):
        """Initialize the container."""

        #Calculate the spacing between particles
        spacing = self._length / 6.0
        velocities = self.generate_velocities(number_of_particles)
        for n in range(number_of_particles):
            #Start with 3 layers of 6x6 particles
            x = (n%6 + 1) * spacing
            y = ((n-(n/36)*36)/6 + 1) * spacing
            z = (n/36 + 1) * spacing
            position = (x, y, z,)
            velocity = velocities.pop()
            particle = Particle(position, velocity)
            self._particles.append(particle)

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
            fs[d] = math.sqrt(self._temperature / v2tot[d])
        for i in range(number_of_particles):
            vn = [0] * dimensions
            for d in range(dimensions):
                vn[d] = (velocities[i][d] - vtot[d]) * fs[d]
            velocities[i] = vn

        vtot = [0] * dimensions
        v2tot = [0] * dimensions
        for item in velocities:
            for dim in range(len(item)):
                vtot[dim] += item[dim]
                v2tot[dim] += item[dim]**2
        for dim in range(dimensions):
            v2tot[dim] = v2tot[dim] / number_of_particles
        print vtot, v2tot

    def update_forces(self):
        #Loop over all pairs
        #Use PBC
        #Test cutoff
        #Update force according to LJ
        #Update energy
        pass
