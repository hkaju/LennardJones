pdf("reports/energies-dt{timestep}.pdf")

data <- read.csv("output.csv", header=T)

plot(data$t, data$T, ylim=c(-5.5, 3.5), xlab="Steps", ylab="Energy per particle", type="n", main=expression(paste("Step size ", delta, "t = {timestep}")))
lines(data$t, data$V, col="blue")
lines(data$t, data$T, col="black")
lines(data$t, data$K, col="red")

legend("right", cex=0.75, pch=NA, lty=c(1, 1, 1),
  col=c("red", "black", "blue"), legend=c("Kinetic", "Total", "Potential"))

plot(data$t, data$T, ylim=c(-5.5, 3.5), xlab="Steps", ylab="Energy per particle", type="n", main=expression(paste("Step size ", delta, "t = {timestep}")))
lines(data$t, data$T, col="black")

dev.off()
