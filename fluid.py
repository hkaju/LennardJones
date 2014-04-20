import copy

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

    def __init__(self, density, temperature):
        pass

    def initialize(self, atoms):
        #Place particles
        #Give random velocities
        #Update CoM velocity
        #Update total kinetic energy
        #Shift velocities so that CoM velocity is zero
        #Scale velocities according to the equipartition theorem
        pass

    def update_forces(self):
        #Loop over all pairs
        #Use PBC
        #Test cutoff
        #Update force according to LJ
        #Update energy
        pass
