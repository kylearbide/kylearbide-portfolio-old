install.packages("corrplot")
install.packages("factoextra")
install.packages("rgl")
install.packages('class')
install.packages('gmodels')

library(tidyverse)
library(psych)

#Import Dataset
mushrooms_df <- read.table("data/agaricus-lepiota.data", stringsAsFactors=FALSE,sep = ",")
mushrooms_df[1:10,1:9]

mushrooms.names = c("class",'cap-shape','cap-surface','cap-color','bruises','odor','gill-attachment','gill-spacing','gill-size','gill-color','stalk-shape','stalk-root','stalk-surface-above-ring',
                    'stalk-surface-below-ring','stalk-color-above-ring','stalk-color-below-ring','veil-type','veil-color','ring-number','ring-type','spore-print-color','population','habitat')
mushrooms.names

str(mushrooms_df)

names(mushrooms_df) <- mushrooms.names
mushrooms_df[1:10,1:9]

mushrooms_df <- replace(mushrooms_df,mushrooms_df == '?',NA)
mushrooms_df <- na.omit(mushrooms_df)

summary(mushrooms_df)
describe(mushrooms_df)

plot(mushrooms_df[1:12]) #note: all the plots take a while to run, you can just refer to the pngs
plot(mushrooms_df[c(1,13:23)])
#Variables to drop : cap-surface, bruises, gill-spacing, gill-size, stalk-shape,
#Veil Type, veil color, ring number, ring type, stalk-surface-above-ring

# 2D relationship plot

ggplot(data = mushrooms_df)+
  aes(y = `stalk-surface-above-ring`
      , x = `stalk-surface-below-ring`)+
  geom_jitter() # apears to have a relationship

#3D relationship plot

library(rgl)

cap_shape_num = unclass(as.factor(mushrooms_df$`cap-shape`))
cap_color_num = unclass(as.factor(mushrooms_df$`cap-color`))
cap_surface_num = unclass(as.factor(mushrooms_df$`cap-surface`))

plot3d( 
  x=cap_shape_num, y=cap_color_num, z=cap_surface_num,
  type = 's', 
  radius = .1,
  xlab="cap shape", ylab="cap color", zlab="cap surface")

#subseting the data
mushrooms_reduced <- subset(mushrooms_df, select = -c(`cap-shape`,`cap-surface`, bruises, `gill-spacing`,`gill-size`, `gill-attachment`, `stalk-shape`,
                                                      `veil-color`,`veil-type`, `ring-number`))

plot(mushrooms_reduced)

#assigning numeric values


library(plyr)

mushrooms_reduced_num <- mushrooms_reduced
mushrooms_reduced_num$class <- as.numeric(mapvalues(mushrooms_reduced_num$class, c("e","p"), c(0,1), warn_missing = TRUE))

convert_ccolor= function(x) {
    A = factor(x, levels=c('n','y','w','g','e','p','b','u','c','r'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$`cap-color` = as.numeric(lapply(mushrooms_reduced_num$`cap-color`, convert_ccolor))
convert_odor= function(x) {
    A = factor(x, levels=c('p','a','l','n','f','c','y','s','m'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$odor = as.numeric(lapply(mushrooms_reduced_num$odor, convert_odor))

convert_gcolor= function(x) {
    A = factor(x, levels=c('k','n','g','p','w','h','u','e','b','r','y','o'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$`gill-color` = as.numeric(lapply(mushrooms_reduced_num$`gill-color`, convert_gcolor))

convert_sroot= function(x) {
    A = factor(x, levels=c('e','c','b','r','?'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$`stalk-root` = as.numeric(lapply(mushrooms_reduced_num$`stalk-root`, convert_sroot))
convert_ssar= function(x) {
    A = factor(x, levels=c('s','f','k','y'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$`stalk-surface-above-ring` = as.numeric(lapply(mushrooms_reduced_num$`stalk-surface-above-ring`, convert_ssar))
convert_ssbr= function(x) {
    A = factor(x, levels=c('s','f','k','y'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$`stalk-surface-below-ring` = as.numeric(lapply(mushrooms_reduced_num$`stalk-surface-below-ring`, convert_ssbr))
convert_scar= function(x) {
    A = factor(x, levels=c('w','g','p','n','b','e','o','c','y'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$`stalk-color-above-ring` = as.numeric(lapply(mushrooms_reduced_num$`stalk-color-above-ring`, convert_scar))
convert_scbr= function(x) {
    A = factor(x, levels=c('w','p','g','b','n','e','y','o','c'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$`stalk-color-below-ring` = as.numeric(lapply(mushrooms_reduced_num$`stalk-color-below-ring`, convert_scbr))
convert_rtype= function(x) {
    A = factor(x, levels=c('p','e','l','f','n'))
    values = c(seq(10,150,10))
    values[A]
}

mushrooms_reduced_num$`ring-type` = as.numeric(lapply(mushrooms_reduced_num$`ring-type`, convert_rtype))
convert_spc= function(x) {
    A = factor(x, levels=c('k','n','u','h','w','r','o','y','b'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$`spore-print-color` = as.numeric(lapply(mushrooms_reduced_num$`spore-print-color`, convert_spc))
convert_population= function(x) {
    A = factor(x, levels=c('s','n','a','v','y','c'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$population = as.numeric(lapply(mushrooms_reduced_num$population, convert_population))
convert_habitat= function(x) {
    A = factor(x, levels=c('u','g','m','d','p','w','l'))
    values = c(seq(10,150,10))
    values[A]
}
mushrooms_reduced_num$habitat = as.numeric(lapply(mushrooms_reduced_num$habitat, convert_habitat))

describe(mushrooms_reduced_num)
str(mushrooms_reduced_num)
#correlation plot

library(corrplot)

mush_cor <- cor(mushrooms_reduced_num)
mush_cor

corrplot(mush_cor)


#normalize the data

normalize <- function(x) {((x-min(x))/(max(x)-min(x)))}
normalize

mushrooms_normalized = as.data.frame(lapply(mushrooms_reduced_num[2:13], normalize))
mushrooms_normalized

poisonous = mushrooms_reduced_num[,1]# we dont want to normalize the classes
poisonous

# if we need to get the original values back
habitat_min = min(mushrooms_reduced_num$habitat)
habitat_max = max(mushrooms_reduced_num$habitat)

habitat_test = mushrooms_normalized$habitat[1]*(habitat_max-habitat_min)+habitat_min
habitat_test

#Z Score Normalization
zscore <- function(x){(x-mean(x))/sd(x)}
zscore(c(10,20,30,40,50))

mushrooms_Znormalized = as.data.frame(lapply(mushrooms_reduced_num[2:13], zscore))
mushrooms_Znormalized

#add back the classes
mushrooms_normalized$class <- poisonous

#Train/test splits
#70/30 split

sample_size = floor(0.7 * nrow(mushrooms_normalized))

train_index = sample(seq_len(nrow(mushrooms_normalized)),size = sample_size)

train1 = mushrooms_normalized[train_index,]
test1 = mushrooms_normalized[-train_index,]

#60/40 split
sample_size = floor(0.6 * nrow(mushrooms_normalized))

train_index = sample(seq_len(nrow(mushrooms_normalized)),size = sample_size)

train2 = mushrooms_normalized[train_index,]
test2 = mushrooms_normalized[-train_index,]

#50/50 split
sample_size = floor(0.5 * nrow(mushrooms_normalized))

train_index = sample(seq_len(nrow(mushrooms_normalized)),size = sample_size)

train3 = mushrooms_normalized[train_index,]
test3 = mushrooms_normalized[-train_index,]

#remove testing labels
test1_classes = test1[11] 
test2_classes = test2[11] 
test3_classes = test3[11]

test1_features <- subset(test1, select = -c(class))
test2_features <- subset(test1, select = -c(class))
test3_features <- subset(test1, select = -c(class))

#Clustering
# 2 clusters
mushrooms_normalized_features =  subset(mushrooms_normalized, select = -c(class))
mushrooms_k2 = kmeans(mushrooms_normalized_features, centers = 2)
str(mushrooms_k2)
mushrooms_k2


library("factoextra")

factoextra::fviz_cluster(mushrooms_k2,mushrooms_normalized_features, main = '2 clusters')

# We cant really read the point labels here so lets clear it up a bit
point_labels  = as.numeric(rownames(mushrooms_normalized_features))
point_labels_3 = list()
for (x in point_labels){
  if (x%%3 == 0){
    point_labels_3 <- append(point_labels_3,x)
  }
}
point_colors = mushrooms_k2$cluster
point_colors_3 = as.character(point_colors[c(as.character(point_labels_3))])

factoextra::fviz_cluster(mushrooms_k2,mushrooms_normalized_features, main = '2 clusters', geom = "point") +
  geom_text(aes(label = point_labels_3, colour = point_colors_3), data = . %>% filter(row_number() %% 3 == 0))

#Lets investigate two close features; 5436 (cluster 2) and 5142(cluster 1)

mushrooms_normalized[5436,]

mushrooms_normalized[5142,]
# These two cases are very similar, with the only difference being stalk surface below ring
#we also notice they are in the same class

# 3 clusters
mushrooms_k3 = kmeans(mushrooms_normalized_features, centers = 3)
str(mushrooms_k3)
mushrooms_k3

#relabel the points
point_colors = mushrooms_k3$cluster
point_colors_3 = as.character(point_colors[c(as.character(point_labels_3))])

factoextra::fviz_cluster(mushrooms_k3,mushrooms_normalized_features, main = '3 clusters', geom = "point") +
  geom_text(aes(label = point_labels_3, colour = point_colors_3), data = . %>% filter(row_number() %% 3 == 0))

#Lets investigate two close features; 5382 (cluster 2) and 5250(cluster 3)

mushrooms_normalized[5382,]

mushrooms_normalized[5250,]
# again, these are in the same class but different clusters

# 4 Clusters
mushrooms_k4 = kmeans(mushrooms_normalized_features, centers = 4)
str(mushrooms_k4)
mushrooms_k4

#relabel the points
point_colors = mushrooms_k4$cluster
point_colors_3 = as.character(point_colors[c(as.character(point_labels_3))])

factoextra::fviz_cluster(mushrooms_k4,mushrooms_normalized_features, main = '3 clusters', geom = "point") +
  geom_text(aes(label = point_labels_3, colour = point_colors_3), data = . %>% filter(row_number() %% 3 == 0))

# We can also look at the centers
mushrooms_k4$centers

# A high value in odor favors clusters 2 and 3. This does not mean as much to use since we know our features are categorical

# 5 Clusters
mushrooms_k5 = kmeans(mushrooms_normalized_features, centers = 5)
str(mushrooms_k5)
mushrooms_k5

#relabel the points
point_colors = mushrooms_k5$cluster
point_colors_3 = as.character(point_colors[c(as.character(point_labels_3))])

factoextra::fviz_cluster(mushrooms_k5,mushrooms_normalized_features, main = '3 clusters', geom = "point") +
  geom_text(aes(label = point_labels_3, colour = point_colors_3), data = . %>% filter(row_number() %% 3 == 0))

# 6 Clusters
mushrooms_k6 = kmeans(mushrooms_normalized_features, centers = 6 )
str(mushrooms_k6)
mushrooms_k6

#relabel the points
point_colors = mushrooms_k6$cluster
point_colors_3 = as.character(point_colors[c(as.character(point_labels_3))])

factoextra::fviz_cluster(mushrooms_k6,mushrooms_normalized_features, main = '3 clusters', geom = "point") +
  geom_text(aes(label = point_labels_3, colour = point_colors_3), data = . %>% filter(row_number() %% 3 == 0))

# 7 clusters
mushrooms_k7 = kmeans(mushrooms_normalized_features, centers = 7 )
str(mushrooms_k7)
mushrooms_k7

#relabel the points
point_colors = mushrooms_k7$cluster
point_colors_3 = as.character(point_colors[c(as.character(point_labels_3))])

factoextra::fviz_cluster(mushrooms_k7,mushrooms_normalized_features, main = '3 clusters', geom = "point") +
  geom_text(aes(label = point_labels_3, colour = point_colors_3), data = . %>% filter(row_number() %% 3 == 0))

# plotting within sum of squares
wssplot <- function(data, nc= 10, seed = 1234){
  wss <- (nrow(data)-1)*sum(apply(data,2,var))
  for (i in 2:nc){
    set.seed(seed)
    wss[i] <- sum(kmeans(data, center = i)$withinss)
  }
  plot (1:nc, wss, type = 'b',
        xlab = "Number of Clusters",
        ylab = "Within groups sum of squares")
}

wssplot(mushrooms_normalized_features, nc=10, seed = 1234)

# we can also plot using fviz

factoextra::fviz_nbclust(mushrooms_normalized_features,FUNcluster = kmeans, method = 'wss', k.max = 10, verbose = TRUE)
# it appears the optimal number of clusters is around 4-5

#Classification
# K_NN

#We already have our train test split, but we still need to drop the classes in those cases
train1_features = subset(train1, select = -c(class))

#now lets generate labels with 5 clusters

train_1_k5=kmeans(train1_features, centers = 5)
train_1_k5

#Apply knn to the test set
library(class)

knn_test_1_k5 = knn(train1_features,test1_features,train_1_k5$cluster,k=5)
knn_test_1_k5

#generate labels for the test
kmeans_test_1_k5 = kmeans(test1_features, centers = 5)
kmeans_test_1_k5

kmeans_test_1_k5$cluster
knn_test_1_k5

# The results in these two cases appear to be very different. When we investigate the Cluster means,
# it becomes obvious that the clusters in the test set do not follow the same qualities as those in the training set
# For example, in the test set 'odor' has the highest weight in cluster 3,
# but in training, 'odor' contains the highest weight for cluster 4.

#Lets move on to linear modeling

#We can regenerate the labels with clusters = 5
#This time, i want to create the labels for all the data before splitting the data

k5_classes = kmeans(mushrooms_normalized_features, centers = 5)
k5_classes

mushrooms_linear_5 = mushrooms_normalized_features
mushrooms_linear_5$target = k5_classes$cluster


sample_size = floor(0.7 * nrow(mushrooms_linear_5))

train_index = sample(seq_len(nrow(mushrooms_linear_5)),size = sample_size)

linear_train_5 = mushrooms_linear_5[train_index,]
linear_test_5 = mushrooms_linear_5[-train_index,]

linear_test_5_targets = linear_test_5$target
linear_test_5 = subset(linear_test_5, select = -c(target))

mushroom_glm_5 = glm(linear_train_5$target ~ ., family = gaussian, data = linear_train_5)
summary(mushroom_glm_5)

# and anova
mushroom_anova_5 = anova(mushroom_glm_5, test = 'Chisq')
mushroom_anova_5

#plot the fitted values
plot(mushroom_glm_5)

# There are some conclusions to be drawn from this plot
#Plot 1: Our residuals don't appear to be too far off, They also do not appear to have any kind of relationship
#with the predicted values. Note: the trends noticed are expected due to the nature of our data, since the true values
#are only whole numbers but our model can output decimal values

#Plot 2: This helps us check for normal distribution I believe. We follow the trend line roughly so this is ok

#Plot 3: Again, we expect a weird shape due to the nature of our true values

#Plot 4: In this plot, we look at the upper and lower right for influential values

#Now we perform our predictions
mushroom_pred_5 = predict(mushroom_glm_5, newdata = linear_test_5)
mushroom_pred_5
summary(mushroom_pred_5)

# We can display our confidence intervals
confint(mushroom_glm_5)

#Comparing vs prediction
mushroom_pred_5_kmean = kmeans(mushroom_pred_5, centers = 5)
mushroom_pred_5_kmean

#Compare our prediction to the true values
library(gmodels)
CrossTable(mushroom_pred_5_kmean$cluster, linear_test_5_targets, prop.chisq = TRUE)

#table of cluster counts
k5_cluster_counts = mushroom_pred_5_kmean$size
k5_cluster_counts = as.data.frame(k5_cluster_counts)

target_counts = as.data.frame(table(linear_test_5_targets))
k5_cluster_counts$target_counts = target_counts$Freq

k5_cluster_counts

#Now lets repeat with 7 clusters

k7_classes = kmeans(mushrooms_normalized_features, centers = 7)
k7_classes

mushrooms_linear_7 = mushrooms_normalized_features
mushrooms_linear_7$target = k7_classes$cluster

#Train/test split
sample_size = floor(0.7 * nrow(mushrooms_linear_7))

train_index = sample(seq_len(nrow(mushrooms_linear_7)),size = sample_size)

linear_train_7 = mushrooms_linear_7[train_index,]
linear_test_7 = mushrooms_linear_7[-train_index,]

linear_test_7_targets = linear_test_7$target
linear_test_7 = subset(linear_test_7, select = -c(target))

mushroom_glm_7 = glm(linear_train_7$target ~ ., family = gaussian, data = linear_train_7)
summary(mushroom_glm_7)

# and anova
mushroom_anova_7 = anova(mushroom_glm_7, test = 'Chisq')
mushroom_anova_7

#plot the fitted values
plot(mushroom_glm_7)

# There are some conclusions to be drawn from this plot
#Plot 1: Again, our residuals don't appear to be too far off, They also do not appear to have any kind of relationship
#with the predicted values.

#Plot 2: The normality appears to fit a bit worse than the last

#Plot 3: Again, we expect a weird shape due to the nature of our true values

#Plot 4: In this plot, we look at the upper and lower right for influential values

#Now we perform our predictions
mushroom_pred_7 = predict(mushroom_glm_7, newdata = linear_test_7)
mushroom_pred_7
summary(mushroom_pred_7)

# We can display our confidence intervals
confint(mushroom_glm_7)

#Comparing vs prediction
mushroom_pred_7_kmean = kmeans(mushroom_pred_7, centers = 7)
mushroom_pred_7_kmean

#Compare our prediction to the true values
CrossTable(mushroom_pred_7_kmean$cluster, linear_test_7_targets, prop.chisq = TRUE)

#table of cluster counts
k7_cluster_counts = mushroom_pred_7_kmean$size
k7_cluster_counts = as.data.frame(k7_cluster_counts)

target_counts = as.data.frame(table(linear_test_7_targets))
k7_cluster_counts$target_counts = target_counts$Freq

k7_cluster_counts

# And 9 clusters

k9_classes = kmeans(mushrooms_normalized_features, centers = 9)
k9_classes

mushrooms_linear_9 = mushrooms_normalized_features
mushrooms_linear_9$target = k9_classes$cluster

#Train/test split
sample_size = floor(0.7 * nrow(mushrooms_linear_9))

train_index = sample(seq_len(nrow(mushrooms_linear_9)),size = sample_size)

linear_train_9 = mushrooms_linear_9[train_index,]
linear_test_9 = mushrooms_linear_9[-train_index,]

linear_test_9_targets = linear_test_9$target
linear_test_9 = subset(linear_test_9, select = -c(target))

# train linear model
mushroom_glm_9 = glm(linear_train_9$target ~ ., family = gaussian, data = linear_train_9)
summary(mushroom_glm_9)

# and anova
mushroom_anova_9 = anova(mushroom_glm_9, test = 'Chisq')
mushroom_anova_9

#plot the fitted values
plot(mushroom_glm_9)

# There are some conclusions to be drawn from this plot
#Plot 1: here, our residuals appear to be a bit larger than with 5 and 7 clusters

#Plot 2: This normality fit isn't as good as 7 clusters

#Plot 3: Again, we expect a weird shape due to the nature of our true values

#Plot 4: In this plot, we look at the upper and lower right for influential values

#Now we perform our predictions
mushroom_pred_9 = predict(mushroom_glm_9, newdata = linear_test_9)
mushroom_pred_9
summary(mushroom_pred_9)

# We can display our confidence intervals
confint(mushroom_glm_9)

#Comparing vs prediction
mushroom_pred_9_kmean = kmeans(mushroom_pred_9, centers = 9)
mushroom_pred_9_kmean

#Compare our prediction to the true values
CrossTable(mushroom_pred_9_kmean$cluster, linear_test_9_targets, prop.chisq = TRUE)

#table of cluster counts
k9_cluster_counts = mushroom_pred_9_kmean$size
k9_cluster_counts = as.data.frame(k9_cluster_counts)

target_counts = as.data.frame(table(linear_test_9_targets))
k9_cluster_counts$target_counts = target_counts$Freq

k9_cluster_counts

# The 5 clusters model appeared to be the most accurate, lets repeat it with changing our params
# We've seen that color below and above ring are the least influential features, so lets remove them

mushrooms_new_features = subset(mushrooms_normalized_features, select = -c(stalk.color.above.ring, stalk.color.below.ring))

k5_classes_2 = kmeans(mushrooms_new_features, centers = 5)
k5_classes_2

mushrooms_linear_reduced = mushrooms_new_features
mushrooms_linear_reduced$target = k5_classes_2$cluster


sample_size = floor(0.7 * nrow(mushrooms_linear_reduced))

train_index = sample(seq_len(nrow(mushrooms_linear_reduced)),size = sample_size)

linear_train_red = mushrooms_linear_reduced[train_index,]
linear_test_red = mushrooms_linear_reduced[-train_index,]

linear_test_red_targets = linear_test_red$target
linear_test_red = subset(linear_test_red, select = -c(target))

mushroom_glm_red = glm(linear_train_red$target ~ ., family = gaussian, data = linear_train_red)
summary(mushroom_glm_red)

#plot the fitted values
plot(mushroom_glm_red)

# There are some conclusions to be drawn from this plot
# Similar patterns as described before, but our residuals appear to be a closer, except for a few extremes

#Now we perform our predictions
mushroom_pred_red = predict(mushroom_glm_red, newdata = linear_test_red)
mushroom_pred_red
summary(mushroom_pred_red)

#Comparing vs prediction
mushroom_pred_red_kmean = kmeans(mushroom_pred_red, centers = 5)
mushroom_pred_red_kmean

#Compare our prediction to the true values
library(gmodels)
CrossTable(mushroom_pred_red_kmean$cluster, linear_test_red_targets, prop.chisq = TRUE)

#table of cluster counts
k5_cluster_counts_red = mushroom_pred_red_kmean$size
k5_cluster_counts_red = as.data.frame(k5_cluster_counts_red)

target_counts = as.data.frame(table(linear_test_red_targets))
k5_cluster_counts_red$target_counts = target_counts$Freq

k5_cluster_counts_red
