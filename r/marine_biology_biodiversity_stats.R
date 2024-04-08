# # Author: Olivia Drukker 
# Date: Nov 29, 2018
# Marine Biology
# Question: Is there a difference in H', S, etc
# between locations / current speeds? 
# Type of Analysis: ANOVA

# Load data and libraries

dockData <- read.csv("Dock Percent Coverage Data.csv", header=TRUE)
head(dockData)
  
library(lattice)
lattice.options(default.theme=standard.theme(color=FALSE))
library(car)
library(mosaic)
library(ggplot2)

# Check the levels

levels(dockData$sample_name)
levels(dockData$current_speed)
levels(dockData$S)
levels(dockData$N)
levels(dockData$H)

dockData$current_speed <- factor(dockData$current_speed)
levels(dockData$current_speed)

# First, looking at S - Number of Species
# Explore the data 

densityplot(~S, group=sample_name, data=dockData,
            auto.key = TRUE, col="black")

boxplot(list("DT"=subset(dockData, sample_name=="DT")$S,
             "FI"=subset(dockData, sample_name=="FI")$S,
             "PD"=subset(dockData, sample_name=="PD")$S),
             horizontal = T, pch=16, xlab="Number of Species")
  
# Fit the model

SModel <- lm(S~sample_name, data=dockData)
summary(SModel)        

# Check the SVAs -- 
#Normal distribution of the residuals - DT two pts not in 90% lines, good enough!

qqPlot(subset(residuals(SModel), dockData$sample_name=="DT"),
       ylab="Dockton residuals", pch=16)
qqPlot(subset(residuals(SModel), dockData$sample_name=="FI"),
       ylab="Fox Island residuals", pch=16)
qqPlot(subset(residuals(SModel), dockData$sample_name=="PD"),
       ylab="Point Defiance residuals", pch=16)

# Equal variances of the residuals -- all good!

densityplot(~residuals(SModel), group=sample_name,
            auto.key = TRUE, data=dockData)

# Tukey Post-hoc Test -- calculate and plot the CI

TukeyHSD(aov(SModel))
plot(TukeyHSD(aov(SModel)))

# Bar plot

barchart = ggplot(dockData, aes(sample_name, S)) +
  stat_summary(fun.y = mean, geom = "bar", position = "dodge") +
  stat_summary(fun.data = mean_cl_normal, geom = "errorbar", position = position_dodge(width = 0.9), width = 0.2) +
  theme_classic() +
  xlab("Location") + ylab("Number of Species")
barchart


# Now looking at H' - Species Evenness
# Explore the data 

densityplot(~H..loge., group=sample_name, data=dockData,
            auto.key = TRUE, col="black")

boxplot(list("DT"=subset(dockData, sample_name=="DT")$H..loge.,
             "FI"=subset(dockData, sample_name=="FI")$H..loge.,
             "PD"=subset(dockData, sample_name=="PD")$H..loge.),
        horizontal = T, pch=16, xlab="Species Evenness")

# Remove the Dockton outlier

dockData <- subset(dockData, H..loge.>0.5)

densityplot(~H..loge., group=sample_name, data=dockData,
            auto.key = TRUE, col="black")

boxplot(list("DT"=subset(dockData, sample_name=="DT")$H..loge.,
             "FI"=subset(dockData, sample_name=="FI")$H..loge.,
             "PD"=subset(dockData, sample_name=="PD")$H..loge.),
        horizontal = T, pch=16, xlab="Species Evenness")

# Fit the model

HModel <- lm(H..loge.~sample_name, data=dockData)
summary(HModel) 

# Check the SVAs -- 
#Normal distribution of the residuals - all with 90% lines!

qqPlot(subset(residuals(HModel), dockData$sample_name=="DT"),
       ylab="Dockton residuals", pch=16)
qqPlot(subset(residuals(HModel), dockData$sample_name=="FI"),
       ylab="Fox Island residuals", pch=16)
qqPlot(subset(residuals(HModel), dockData$sample_name=="PD"),
       ylab="Point Defiance residuals", pch=16)

# Equal variances of the residuals -- good enough!

densityplot(~residuals(HModel), group=sample_name,
            auto.key = TRUE, data=dockData)

# Tukey Post-hoc Test -- calculate and plot the CI

TukeyHSD(aov(HModel))
plot(TukeyHSD(aov(HModel)))

# Bar plot

barchart = ggplot(dockData, aes(sample_name, H..loge.)) +
  stat_summary(fun.y = mean, geom = "bar", position = "dodge") +
  stat_summary(fun.data = mean_cl_normal, geom = "errorbar", position = position_dodge(width = 0.9), width = 0.2) +
  theme_classic() +
  xlab("Location") + ylab("Species Evenness")
barchart

# N - Percent Coverage
# Explore the data 

densityplot(~N, group=sample_name, data=dockData,
            auto.key = TRUE, col="black")

boxplot(list("DT"=subset(dockData, sample_name=="DT")$N,
             "FI"=subset(dockData, sample_name=="FI")$N,
             "PD"=subset(dockData, sample_name=="PD")$N),
        horizontal = T, pch=16, xlab="Number of Species")

# Fit the model

NModel <- lm(N~sample_name, data=dockData)
summary(NModel)        

# Check the SVAs -- 
#Normal distribution of the residuals - DT two pts not in 90% lines, good enough!

qqPlot(subset(residuals(NModel), dockData$sample_name=="DT"),
       ylab="Dockton residuals", pch=16)
qqPlot(subset(residuals(NModel), dockData$sample_name=="FI"),
       ylab="Fox Island residuals", pch=16)
qqPlot(subset(residuals(NModel), dockData$sample_name=="PD"),
       ylab="Point Defiance residuals", pch=16)

# Equal variances of the residuals -- all good!

densityplot(~residuals(NModel), group=sample_name,
            auto.key = TRUE, data=dockData)

# Tukey Post-hoc Test -- calculate and plot the CI

TukeyHSD(aov(NModel))
plot(TukeyHSD(aov(NModel)))

# Bar plot

barchart = ggplot(dockData, aes(sample_name, N)) +
  stat_summary(fun.y = mean, geom = "bar", position = "dodge") +
  stat_summary(fun.data = mean_cl_normal, geom = "errorbar", position = position_dodge(width = 0.9), width = 0.2) +
  theme_classic() +
  xlab("Location") + ylab("Percent Coverage")
barchart
