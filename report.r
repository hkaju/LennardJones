pdf("energies.pdf")

data <- read.csv("output.csv", header=T)

plot(data$t, data$K, ylim=c(-5, 3.5), xlab="Time", ylab="Energy per particle", type="n")
lines(data$t, data$V)
lines(data$t, data$T)
lines(data$t, data$K)

dev.off()
