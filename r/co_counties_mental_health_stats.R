# Author: Olivia Drukker
# Date: March, 2023
# Question: What variables will help us predict mental health index in CO 
#           counties?
# Type of Analysis: Multiple Linear Regression
# Data: Data taken from the CO Department of Public Health and the
#       Environment
#----------------------------------------------

# Set working directory

# Load libraries and data

library(lattice)
lattice.options(default.theme=standard.theme(color=FALSE))
library(mosaic)
library(car)
install.packages("lm.beta")
library(lm.beta)

mental_health <- read.csv("mental_health.csv", header=TRUE)

summary(mental_health$mental_health)

# Look at density plots & histograms of potential variables
# Check for skew 

densityplot(mental_health$mental_health)
densityplot(mental_health$mhi)
densityplot(mental_health$phys_activity)
densityplot(mental_health$heavy_drinking)
densityplot(mental_health$education)
densityplot(mental_health$unemployment)
densityplot(mental_health$pollution)
densityplot(mental_health$housing_burden)
densityplot(mental_health$disability)

histogram(mental_health$mental_health)
histogram(mental_health$mhi)
histogram(mental_health$phys_activity)
histogram(mental_health$heavy_drinking)
histogram(mental_health$education)
histogram(mental_health$unemployment)
histogram(mental_health$pollution)
histogram(mental_health$housing_burden)
histogram(mental_health$disability)

# Perform log transformations on skewed variables
# phys_activity positively skewed - log transform

densityplot(mental_health$log_phys_activity)
histogram(mental_health$log_phys_activity)

# Scatterplot matrix

pairs(subset(mental_health, select=c(mental_health, mhi, log_phys_activity, 
                                     heavy_drinking,education, unemployment,
                                     pollution, housing_burden, 
                                     disability)), pch=16)

# No visible correlation btw mental_health and pollution / housing_burden
# Remove pollution and housing burden from model
# Look at scatterplot again

pairs(subset(mental_health, select=c(mental_health, mhi, log_phys_activity, 
                                     heavy_drinking, education, unemployment,
                                     disability)), pch=16)

# Correlation coefficient matrix for variables of interest

cor(mental_health[c("mental_health", "mhi", "log_phys_activity", 
                    "heavy_drinking", "education", "disability")])

# heavy_drinking has very low correlation coefficient
# Remove heavy_drinking from model

# Creating a few potential models with different variables

mh_model1 <- lm(mental_health~mhi + log_phys_activity + unemployment 
                + education + disability, data=mental_health)
summary(mh_model1)

mh_model2 <- lm(mental_health~mhi + unemployment + disability, 
                data=mental_health)
summary(mh_model2)

mh_model3 <- lm(mental_health~mhi + log_phys_activity + disability
                + unemployment, data=mental_health)
summary(mh_model3)

# Check the residual plots of all models

plot(rstandard(mh_model1)~fitted(mh_model1), pch=16,
     xlab="Fitted Values", ylab="Standard Resuduals",
     main="Residuals Plot, Model 1")
abline(h=0)

plot(rstandard(mh_model2)~fitted(mh_model2), pch=16,
     xlab="Fitted Values", ylab="Standard Resuduals",
     main="Residuals Plot, Model 2")
abline(h=0)

plot(rstandard(mh_model3)~fitted(mh_model3), pch=16,
     xlab="Fitted Values", ylab="Standard Resuduals",
     main="Residuals Plot, Model 3")
abline(h=0)

# Check AICs of all models

AIC(mh_model1, mh_model2, mh_model3)

# Check the standardized beta weights of variables in best model

lm.beta(mh_model2)

# Check the VIFs of best model

vif(mh_model2)

# Decision - use model 2

summary(mh_model3)