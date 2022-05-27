---
layout: frontpage
title: ArangoDB Projects
---

<div class="navbar">
  <div class="navbar-inner">
      <ul class="nav">
          <li><a href="#reddit">Reddit Graph Analysis</a></li>
      </ul>
  </div>
</div>

### <a name="reddit"></a>Reddit Graph Anaylsis

This project is a graph analysis of posts and comments from Reddit. The project consists of cleaning the raw data, converting the JSON data into vertex and edge collections compatible for ArangoDB insertion, hosting the graph database through Docker, and performing some simple analysis with AQL. The graph schema is shown in the presentation, and consists of post, comment, and user vertex collections and posted, commented, and commented_on edge collection, with a second graph that contains an additional comment_thread edge collection. Using these two graphs, AQL queries and traversals were used to answer questions such as the number of users with >5 comments, how far users from 'Daily Discussion' expand into the networks, and the number of users participating in conversations about a topic. 

[Presentation ![Crypto](/pages/icons16/ppt-icon.png)](https://github.com/kylearbide/reddit_graph_db/blob/main/Reddit%20Graph%20Analysis.pdf)
[Repository ![Crypto](/pages/icons16/github-icon.png)](https://github.com/kylearbide/reddit_graph_db)
