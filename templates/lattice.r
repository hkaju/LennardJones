library(scatterplot3d)

pdf("lattice.pdf")

data <- read.csv("grid.csv", header=T)

scatterplot3d(data$x, data$y, data$z, xlab="X", ylab="Y", zlab="Z")

dev.off()
