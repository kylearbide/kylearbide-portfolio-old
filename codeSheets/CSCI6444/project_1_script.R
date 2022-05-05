library(igraph)
library(sna)

###Part 1&2
#import dataset and plot the graph
CA.GrQc = read.delim("CA-GrQc.txt", comment.char="#")
graph = graph_from_data_frame(CA.GrQc)
plot.igraph(graph, edge.arrow.size=0.1, vertex.size=5)

###Part 3
##Simplification
#Step 1
verticies_lt20 = V(graph)[igraph::degree(graph)<20]
graph1 = igraph::delete.vertices(graph,verticies_lt20) #remove nodes (degree <=20)
plot.igraph(graph1, edge.arrow.size=0.3, vertex.size=10, vertex.label.cex=0.5)

#Step 2
graph1_df = as_data_frame(graph1, what="edges") #convert igraph object to dataframe
graph2_df = graph1_df[1:200,] #choose the first 200 edges
graph2 = graph_from_data_frame(graph2_df)
plot.igraph(graph2, edge.arrow.size=0.3, vertex.size=10, vertex.label.cex=0.5)

#Step 3
verticies_lt2 <- V(graph2)[igraph::degree(graph2)<2]
graph.sim = igraph::delete.vertices(graph2, verticies_lt2)
plot.igraph(graph.sim, edge.arrow.size=0.3, vertex.size=10, vertex.label.cex=0.5)

## Applying Functions to the Graph
#verticies of the graph
V(graph.sim) 
#edges of the graph
E(graph.sim)

#Adjacency matrix
as.matrix(get.adjacency(graph.sim))

#Density
graph.sim.adj = as.matrix(get.adjacency(graph.sim))
graph.sim.density <- gden(graph.sim.adj)
graph.sim.density 
edge_density(graph.sim)
edge_density(graph.sim, loops=T)

#Egocentric Network
graph.sim.ego<- ego.extract(graph.sim.adj)
graph.sim.ego["8612"]
graph.sim.ego["6610"]

#Betweenness Centrality
igraph::centr_betw(graph.sim)

#Closneness Centrality
igraph::centr_clo(graph.sim)

#Shortest Paths
igraph::shortest.paths(graph.sim)
igraph::get.shortest.paths(graph.sim,"6610")

# Geodesic
geodist(graph.sim.adj)

#Number of Paths Between Nodes
graph.sim.adj%*%graph.sim.adj

#Histogram
hist(igraph::degree(graph.sim))

#Diameter
igraph::diameter(graph.sim)

#Max Cliques
node <- c(1)
graph.sim.1clique = igraph::max_cliques(graph.sim, min=NULL, max=NULL, subset=node)
graph.sim.1clique

#Largest Cliques
igraph::clique_num(graph.sim)

#Alpha centrality
alpha_centrality(graph.sim, alpha = 0.9)

#Walktrap Community
wc_g<-walktrap.community(graph.sim)
plot(wc_g,graph.sim, vertex.size=0.5, layout=layout.fruchterman.reingold)


###Part 4
#1. Look at more available layouts in igraph
layouts = grep("^layout_", ls("package:igraph"), value=TRUE)[-1]
layouts = layouts[!grepl("bipartite|merge|norm|sugiyama|tree", layouts)] # Remove layouts that do not apply to our graph.
par(mfrow=c(3,3), mar=c(1,1,1,1))
for (layout in layouts) {
  print(layout)
  l = do.call(layout, list(graph.sim))
  plot(graph.sim, edge.arrow.mode=0, layout=l, main=layout, vertex.label = NA) }

#2. reset the graphical parameters
dev.off()
par(mfrow=c(1,1))

#3. Interact with the plotting of networks
tkid = tkplot(graph.sim)  #tkid is the id of the tkplot that will open
l = tkplot.getcoords(tkid)  # grab the coordinates from tkplot

#4. Create a heatmap of the network matrix
palf = colorRampPalette(c("gold", "dark orange"))
heatmap(graph.sim.adj, Rowv = NA, Colv = NA, col = palf(5),
        scale="none", margins=c(10,10) )

#5. Reciprocity: The proportion of reciprocated ties
reciprocity(graph.sim)

#6. Transitivity: 
transitivity(net, type="global") #global - ratio of triangles (direction disregarded) to connected triples.
transitivity(net, type="local") #local - ratio of triangles to connected triples each vertex is part of.

#7. In igraph, diameter() returns the distance, while get_diameter() returns the nodes along the first found path of that distance.
diam = get_diameter(net, directed=T)

#8. Color nodes along the diameter:
vcol = rep("gray40", vcount(graph.sim))
vcol[diam] = "gold"
ecol = rep("gray80", ecount(graph.sim))
ecol[E(graph.sim, path=diam)] = "orange"
ew = rep(2, ecount(graph.sim))
ew[E(graph.sim, path=diam)] = 4
plot(graph.sim, vertex.color=vcol, edge.color=ecol, edge.arrow.size=0.3, vertex.size=10, vertex.label.cex=0.5)

#9. Values of the first eigenvector of the graph matrix.
centr_eigen(graph.sim, directed=T, normalized=T)

#10. Average path length
mean_distance(graph.sim, directed=T)

#11. Hubs Score (contain a large number of outgoing links) and Authorities Score (contain many incoming links from hubs)
hs <- hub_score(graph.sim, weights=NA)$vector
as <- authority_score(graph.sim, weights=NA)$vector
par(mfrow=c(1,2))
plot(graph.sim, vertex.size=hs*25, main="Hubs", edge.arrow.size=0.3, vertex.label.cex=0.5)
plot(graph.sim, vertex.size=as*15, main="Authorities", edge.arrow.size=0.3, vertex.label.cex=0.5)


###Part 5
#(a) central nodes(s)
d = degree(graph.sim)
d = as.data.frame(d) #sort


#(b) longest path(s)
igraph::diameter(graph.sim)
diam = get_diameter(graph.sim, directed=T)
diam


#(c) largest clique(s)
vcol = rep("grey80", vcount(graph.sim))
vcol[unlist(largest_cliques(graph.sim))] = "gold"
plot(as.undirected(graph.sim), vertex.color=vcol, vertex.label.cex=0.5, vertex.size=15)

#(d) ego(s)
ego(graph.sim)
ego(graph.sim,nodes=V(graph.sim)["6610"])

#(e) power centrality
#power_centrality takes a graph (data) and returns the Boncich power centralities of positions (selected by nodes).
pc = power_centrality(graph.sim, exponent = 0.9)
pc_df = as.data.frame(pc)
pc_df <- cbind(node = rownames(pc_df), pc_df)
rownames(pc_df) <- 1:nrow(pc_df)
pc_df[which.max(pc_df$pc),]
