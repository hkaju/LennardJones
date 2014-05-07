pdf("reports/results-dn{density}.pdf")

data <- read.csv("data/data-dn{density}.csv", header=T)

plot(data$t, data$T, ylim=c(-10, 10), xlab="Steps", ylab="Energy per particle", type="n", main=expression(paste("Step size ", delta, "t = {density}")))
lines(data$t, data$V, col="blue")
lines(data$t, data$T, col="black")
lines(data$t, data$K, col="red")

legend("topright", cex=0.75, pch=NA, lty=c(1, 1, 1),
  col=c("red", "black", "blue"), legend=c("Kinetic", "Total", "Potential"))

plot(data$t, data$temp, xlab="Steps", ylab="Temperature", type="n", main=expression(paste("Temperature at ", rho, " = {density}")))
lines(data$t, data$temp, col="black")

plot(data$t, data$P, xlab="Steps", ylab="Pressure", type="n", main=expression(paste("Pressure at ", rho, " = {density}")))
lines(data$t, data$P, col="black")

dev.off()
