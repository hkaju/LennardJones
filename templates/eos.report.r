pdf("reports/equation-of-state.pdf")

colors = c("red", "blue")

densities <- c(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.05)
johnson <- c(0.17762, 0.3291, 0.4892, 0.7003, 1.0714, 1.751, 3.0287, 5.2857, 9.121, 15.202, 19.462)
calculated <- c(0.189820462424, 0.374597965904, 0.589149082055, 0.903453970713, 1.28746708283, 2.15319217419, 3.60913486736, 5.95818633856, 9.95992640723, 16.1002464076, 20.4923246502)

plot(densities, calculated, xlab=expression(paste(rho)), col=colors[1], ylab="P", main="Lennard-Jones equation of state at T=2.0")
lines(densities, johnson, col=colors[1])
points(densities, johnson, col=colors[1])
points(densities, calculated, col=colors[2])
lines(densities, calculated, col=colors[2])

legend("topleft", pch=NA, lty=c(1, 1, 1),
  col=colors, legend=c("Johnson et al.", "Calculated"))

dev.off()
