import subprocess
import os

def write_data(data):
    f = open("output.csv", "w")
    f.write("t,K,V,T,P,temp\n")
    for item in range(len(data["t"])):
        f.write("{0},{1},{2},{3},{4},{5}\n".format(data["t"][item], data["K"][item], data["V"][item], data["T"][item], data["P"][item], data["temp"][item]))
    f.close()

def generate_report(timestep):
    if not os.path.exists("reports"):
        os.mkdir("reports")
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    template = open("templates/energies.template.r", "r").read()
    report = open("tmp/report.r", "w")
    report.write(template.format(timestep=timestep))
    report.close()
    subprocess.call(['R', '-f tmp/report.r'])
    print("Report generated!")

def write_particles(self, particles):
    f = open("grid.csv", "w")
    f.write("x,y,z\n")
    for particle in particles:
        f.write("{0},{1},{2}\n".format(particle.position[0], particle.position[1], particle.position[2]))
    f.close()
