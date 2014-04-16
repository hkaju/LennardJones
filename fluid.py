class Particle:

    #Particle mass
    _m = 1

    #Position
    x = 0
    y = 0
    z = 0

    #Velocity
    vx = 0
    vy = 0
    vz = 0

    #Force
    fx = 0
    fy = 0
    fz = 0

    def __init__(self, position, velocity):

        #Set initial position and velocity from provided tuples
        self.x, self.y, self.z = position
        self.vx, self.vy, self.vz = velocity

    def set_force_to(self, force):
        self.fx, self.fy, self.fz = force

    def update_position(self, dt):
        pass

class LJContainer:

    _particles = []

    def __init__(self, density, tempoerature):
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
