# Box and whisker plots with tukey's Honestly Significant Differences groups
## Written by Noelle Patterson, 2018
library(multcompView)
library(ggplot2)

# Set your working directory where you keep the input data
workingDir <- "/Users/noellepatterson/apps/Ecogeo-code"
setwd(workingDir)

# ensure that file name is consistent with name below
input_file <- "boxplot_input.csv"

data_values <- read.csv(input_file, header = TRUE, check.names = FALSE, na.strings=c("","NA"))
tuk_df <- data.frame(data_values)

tuk_df$SP_Mag <- tuk_df$SP_Mag*0.028316847

names(tuk_df)[1] <- "groups"

groups <- c("Jensen", "Yampa", "Greendale") # 3 stations
groups <- as.factor(groups) 
# Assign your data matrix or dataframe
tuk_df$groups <- as.factor(tuk_df$groups)
metrics <- names(tuk_df)

metric_units <- c("Timing","Duration (days)","Rate of Change (percent)","Flow (cms)","Duration (days)")

for (j in 1:(ncol(tuk_df)-1)) {
  # Box and whisker plots for chosen attributes/metrics
  att_name <- names(tuk_df[j+1])
  # Formula for specific attribute as it relates to defined groups
  f <- paste(att_name, "~", "groups")
  aov_fit <- aov(as.formula(f), data=tuk_df) # analysis of variance
  
  # define boxplot colors for 9-class or 3-wyt categories
  colors = c("#b22727", "#f26209", "#FFCC00") # red, orange, yellow
 
  metric_col <- tuk_df[,j+1]
  
  a=boxplot(metric_col ~ tuk_df$groups, yaxt ='n')
  a=boxplot(metric_col ~ tuk_df$groups,ylab=metric_units[j], main=metrics[j+1], na.rm=TRUE, col=colors, las=0, outline = FALSE)
  # axis(2, at=c(230,242.5,255,267.5,280), labels=c('May 19','Jun 1','Jun 13','Jun 26','Jul 8'))
  # axis(2, at=c(0,60,122,183,244,305), labels=c('Oct','Jan','Apr','Apr','Jul','Oct'))
  # axis(2, at=c(0,30,61,91), labels=c('Oct','Nov','Jan','Feb'))
  # setwd("/Users/noellepatterson/apps/FFC_bootstrapping/Outputs/tukey_wyt/tukey_by_wyt/wet")
  # dev.copy(png, filename = paste0("plot_", metrics[j+1], ".png"))
  dev.copy2pdf(file=paste0("plot_", metrics[j+1], ".pdf"), width=8,height=6)
  dev.off()
}

setwd("/Users/noellepatterson/apps/FFC_bootstrapping/Outputs/Summary_tables/total")
write.csv(summary_table, file="total.csv")