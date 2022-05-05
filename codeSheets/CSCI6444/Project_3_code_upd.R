install.packages("tm")
install.packages('wordcloud')
install.packages('quanteda')
install.packages('syuzhet')

library(tm)
library(tidyverse)
library(RColorBrewer)
library(wordcloud)
library(quanteda)
library(syuzhet)

setwd("C:/Users/thatb/intro_to_big_data")
getwd()

## Part 1
# Loading the data
god_of_mars <- VCorpus(DirSource("./txt", ignore.case = TRUE, mode = 'text'))
str(god_of_mars)

god_of_mars

# Extracting the text
mars_text <- god_of_mars[[1]]
mars_text

mars_text[1]

# Separating first 2 chapters

dir.create('chapters')

index_ch1 <- which(mars_text$content == "CHAPTER I", arr.ind = TRUE)
index_ch2 <- which(mars_text$content == "CHAPTER II", arr.ind = TRUE)
index_ch3 <- which(mars_text$content == "CHAPTER III", arr.ind = TRUE)

book_chapter1 <- mars_text$content[(index_ch1+1):(index_ch2-1)]
book_chapter2 <- mars_text$content[(index_ch2+1):(index_ch3-1)]

write.table(book_chapter1, file = "chapters/god_of_mars_chapter1.txt", sep = "\t", row.names=FALSE, col.names=FALSE,quote=FALSE)
write.table(book_chapter2, file = "chapters/god_of_mars_chapter2.txt", sep = "\t", row.names=FALSE, col.names=FALSE,quote=FALSE)

god_of_mars_chapters <- VCorpus(DirSource("chapters", ignore.case = TRUE, mode = 'text'))
str(god_of_mars_chapters)

## Part 2
# Get 10 longest words
get_10_longest_words <- function(chapter){
  all_lengths = data.frame(word = character(),
                           length = integer())
  for (line in chapter){
    chars = str_split(line, " ")
    for (char in chars){
      char_length = str_length(char)
      all_lengths = all_lengths %>%
        add_row(word = char, length = char_length)
    }
    
  }
  
  ordered = all_lengths[order(all_lengths$length, decreasing = TRUE),]
  
  top_10 = ordered[1:10,]
  return(top_10)
}

words_ch1 = get_10_longest_words(book_chapter1)
words_ch2 = get_10_longest_words(book_chapter2)

# Get 10 longest sentences
get_10_longest_sentences <- function(chapter){
  
  all_lengths = data.frame(sentence = character(),
                           length = integer())
  
  one_text = paste(chapter, collapse="")
  sentences = str_split(one_text, pattern = '[.!?]')
  
  for (sentence_ in sentences){
    sent_length = str_length(sentence_)
    all_lengths = all_lengths %>%
      add_row(sentence = sentence_, length = sent_length)
    
  }
  
  ordered = all_lengths[order(all_lengths$length, decreasing = TRUE),]
  
  top_10 = ordered[1:10,]
  return(top_10)
}

sentences_ch1 <- get_10_longest_sentences(book_chapter1)
sentences_ch2 <- get_10_longest_sentences(book_chapter2)

## Part 3
# Document Term Matrix
gom_DTM <- DocumentTermMatrix(god_of_mars_chapters)
gom_DTM
inspect(gom_DTM)
str(gom_DTM)

# Term Document Matrix
gom_TDM <- TermDocumentMatrix(god_of_mars_chapters)
gom_TDM
inspect(gom_TDM)
str(gom_TDM)

# Convert to DataFrame
mars_ch1_text <- god_of_mars_chapters[[1]]
mars_ch2_text <- god_of_mars_chapters[[2]]

ch1_df <- data.frame(mars_ch1_text[1])
ch2_df <- data.frame(mars_ch2_text[1])

ch1_df[1]
god_of_mars_chapters[[1]]$content

# Remove Numbers and punctuation
removeQuote <- function(x) gsub('[\"]', '', x)
god_of_mars_chapters_cl <- tm::tm_map(god_of_mars_chapters, content_transformer(removeQuote))

removeNumPunct <- function(x) gsub("[^[:alpha:][:space:]]*","",x)
god_of_mars_chapters_cl <- tm::tm_map(god_of_mars_chapters_cl, content_transformer(removeNumPunct))

str(god_of_mars_chapters_cl)

inspect(god_of_mars_chapters)
inspect(god_of_mars_chapters_cl)

# Lower Case
god_of_mars_chapters_lower <- tm_map(god_of_mars_chapters_cl, content_transformer(tolower))
str(god_of_mars_chapters_lower)
inspect(god_of_mars_chapters_lower)

# Document Term Matrix (using cleaned data)
gom_DTM <- DocumentTermMatrix(god_of_mars_chapters_lower)
gom_DTM
str(gom_DTM)
inspect(gom_DTM)

# Remove Stop Words
myStopWords <- c(tm::stopwords("english"))
myStopWords

god_of_mars_chapters_stop <- tm_map(god_of_mars_chapters_lower, removeWords, myStopWords)
inspect(god_of_mars_chapters_stop[[1]])

# Term document matrix (no stop words)
gom_ch_stop_TDM <- TermDocumentMatrix(god_of_mars_chapters_stop)
gom_ch_stop_TDM

freq_terms <- findFreqTerms(gom_ch_stop_TDM, lowfreq = 6)
freq_terms

nchar(freq_terms[8])
freq_terms[8]

gom_ch1_tf <- termFreq(god_of_mars_chapters_stop[[1]])
gom_ch1_tf

gom_ch2_tf <- termFreq(god_of_mars_chapters_stop[[2]])
gom_ch2_tf

inspect(gom_ch_stop_TDM)

# Create dendrogram (From Term Document Matrix)
gom_ch1_df <- as.data.frame(gom_ch_stop_TDM[[1]])
gom_ch2_df <- as.data.frame(gom_ch_stop_TDM[[2]])

gom_ch1_dist <- dist(gom_ch1_df)
gom_ch2_dist <- dist(gom_ch2_df)

gom_ch1_DG <- hclust(gom_ch1_dist, method = 'ward.D2')
gom_ch2_DG <- hclust(gom_ch2_dist, method = 'ward.D2')
str(gom_ch1_DG)
plot(gom_ch1_DG)
str(gom_ch2_DG)
plot(gom_ch2_DG)
findMostFreqTerms(gom_ch_stop_TDM, n = 100)

# The dendrogram is very cluttered, we can try to remove more stop words (work in progress)
newstopwords = c('one','even','a','will','may','soon',
                 'can','as','much','just','now','certain',
                 'quite','merely','shall','take','well','great',
                 'though','two','quite','ten','three','four','might','right',
                 'either','last','however','thus','without','like','upon','across',
                 'almost','another','back','base','become','behind', 'beneath', 'better',
                 'cause','centre')

god_of_mars_chapters_stopnew <- tm_map(god_of_mars_chapters_stop, removeWords, newstopwords)
gom_ch_stop_NewTDM <- TermDocumentMatrix(god_of_mars_chapters_stopnew)
str(gom_ch_stop_NewTDM)
findMostFreqTerms(gom_ch_stop_NewTDM, n = 100)

gom_ch1_newdf <- as.data.frame(gom_ch_stop_NewTDM[[1]])
gom_ch2_newdf <- as.data.frame(gom_ch_stop_NewTDM[[2]])

gom_ch1_Newdist <- dist(gom_ch1_newdf)
gom_ch2_Newdist <- dist(gom_ch2_newdf)

gom_ch1_NewDG <- hclust(gom_ch1_Newdist, method = 'ward.D2')
gom_ch2_NewDG <- hclust(gom_ch2_Newdist, method = 'ward.D2')
inspect(gom_ch_stop_NewTDM)
plot(gom_ch1_NewDG)
plot(gom_ch2_NewDG)


# Word Clouds
gom_ch1_ntf <- termFreq(god_of_mars_chapters_stopnew[[1]])
gom_ch2_ntf <- termFreq(god_of_mars_chapters_stopnew[[2]])
words_ch1 <- names(gom_ch1_ntf)
words_ch2 <- names(gom_ch2_ntf)

pal1<- brewer.pal(9,'BuGn')
pal2<- brewer.pal(9,'Spectral')

str(pal1)
str(pal2)

png("wordcloud_packages.png", width=12,height=8, units='in', res=400)
gom_WC_ch1 <- wordcloud(words_ch1, gom_ch1_ntf, colors = pal1[-(1:4)], min.freq=3,
                        max.words=Inf, random.order=FALSE)
gom_WC_ch2 <- wordcloud(words_ch2, gom_ch2_ntf, colors = pal2, min.freq=3,
                        max.words=Inf, random.order=FALSE)
dev.off()

# quanteda
gomText1 = god_of_mars_chapters_stopnew[[1]]
gomText2 = god_of_mars_chapters_stopnew[[2]]
gomText1$content <- gomText1$content[gomText1$content != ""] # delete the blank lines
gomText2$content <- gomText2$content[gomText2$content != ""]
gomText1$content
gomText2$content

gomTokens1 = quanteda::tokens(gomText1$content)
gomTokens2 = quanteda::tokens(gomText2$content)
str(gomTokens1)
str(gomTokens2)

gomDFM1 = quanteda::dfm(gomTokens1)
gomDFM2 = quanteda::dfm(gomTokens2)
str(gomDFM1)
str(gomDFM2)

gomDocFreq1 = quanteda::docfreq(gomDFM1)
gomDocFreq2 = quanteda::docfreq(gomDFM2)
str(gomDocFreq1)
str(gomDocFreq2)
gomDocFreq1
gomDocFreq2

gomWeights1 = dfm_weight(gomDFM1)
gomWeights2 = dfm_weight(gomDFM2)
str(gomWeights1)
str(gomWeights2)
gomWeights1
gomWeights2

gomTFIDF1 = dfm_tfidf(gomDFM1, scheme_tf = "count", scheme_df = "inverse")
gomTFIDF2 = dfm_tfidf(gomDFM2, scheme_tf = "count", scheme_df = "inverse")
gomTFIDF1
gomTFIDF2

# syuzhet
gomTextdf1 = as.data.frame(gomText1$content)
gomTextdf2 = as.data.frame(gomText2$content)
gomTextdf1
gomTextdf2

gomAsString1 = get_text_as_string("./chapters/god_of_mars_chapter1.txt")
gomAsString2 = get_text_as_string("./chapters/god_of_mars_chapter2.txt")
gomAsString1
gomAsString2

gomS1 = get_sentences(gomAsString1)
gomS2 = get_sentences(gomAsString2)
gomS1
gomS2
str(gomS1)
str(gomS2)

gomSSentiment1 = get_sentiment(gomS1, "syuzhet")
gomSSentiment2 = get_sentiment(gomS2, "syuzhet")
gomSSentiment1
gomSSentiment2

gomSBing1 = get_sentiment(gomS1, "bing")
gomSBing2 = get_sentiment(gomS2, "bing")
gomSBing1
gomSBing2

gomSDictionary = get_sentiment_dictionary()
gomSDictionary


gomSDictionaryBing1 = get_sentiment_dictionary("bing")
gomSDictionaryBing2 = get_sentiment_dictionary("bing")
gomSDictionaryBing1
gomSDictionaryBing2

gomSum1 = sum(gomSSentiment1)
gomSum2 = sum(gomSSentiment2)
gomSum1
gomSum2

gomBingSum1 = sum(gomSBing1)
gomBingSum2 = sum(gomSBing2)
gomBingSum1
gomBingSum2

gomMean1 = mean(gomSSentiment1)
gomMean2 = mean(gomSSentiment2)
gomMean1
gomMean2

gomBingMean1 = mean(gomSBing1)
gomBingMean2 = mean(gomSBing2)
gomBingMean1
gomBingMean2

summary(gomSDictionary)

plot(gomSSentiment1, main="The God of Mars Plot trajectory - Chapter 1", xlab="Narrative", ylab="Emotianl valence")
plot(gomSSentiment2, main="The God of Mars Plot trajectory - Chapter 2", xlab="Narrative", ylab="Emotianl valence")
plot(gomSBing1, main="The God of Mars Plot trajectory - Chapter 1: Bing", xlab="Narrative", ylab="Emotianl valence")
plot(gomSBing2, main="The God of Mars Plot trajectory - Chapter 2: Bing", xlab="Narrative", ylab="Emotianl valence")

gomSSentimentPctvalue1 = get_percentage_values(gomSSentiment1, bin=10)
gomSSentimentPctvalue2 = get_percentage_values(gomSSentiment2, bin=10)
structure(gomSSentimentPctvalue1)
structure(gomSSentimentPctvalue2)
plot(gomSSentimentPctvalue1, main="TheGodOfMars PCTValue 10 Bins - Chapter 1", xlab="Narrative", ylab="Emotianl valence", col='red')
plot(gomSSentimentPctvalue2, main="TheGodOfMars PCTValue 10 Bins - Chapter 2", xlab="Narrative", ylab="Emotianl valence", col='red')

gomSSentimentPctvalue1 = get_percentage_values(gomSSentiment1, bin=40)
gomSSentimentPctvalue2 = get_percentage_values(gomSSentiment2, bin=40)
structure(gomSSentimentPctvalue1)
structure(gomSSentimentPctvalue2)
plot(gomSSentimentPctvalue1, main="TheGodOfMars PCTValue 40 Bins - Chapter 1", xlab="Narrative", ylab="Emotianl valence", col='red')
plot(gomSSentimentPctvalue2, main="TheGodOfMars PCTValue 40 Bins - Chapter 2", xlab="Narrative", ylab="Emotianl valence", col='red')

# 3 additional function for tm package

# strip whitespace function (strips extra white space in teh documents)
god_of_mars_tm_ws <- tm::tm_map(god_of_mars_chapters_stop, content_transformer(stripWhitespace))
god_of_mars_tm_ws[[1]][1]

# find most frequent terms (used to find n most frequent words in each chapter)
findMostFreqTerms(gom_ch_stop_TDM, n = 10)

# tm_term_score (returns the number of times a term appears in each document)
tm_term_score(gom_ch_stop_TDM, terms = 'tree')
tm_term_score(gom_ch_stop_TDM, terms = 'book')
tm_term_score(gom_ch_stop_TDM, terms = 'cliff')

# 3 additional function for quanteda packages

#tokens sample takes a sample of the sentences from the chapter
set.seed(123)
gom_ch1_sample = tokens_sample(gomTokens1, size = 100)
gom_ch1_sample

# tokens_ngrams, returns the all the n_grams from our sample
n_grams_quanteda = tokens_ngrams(gom_ch1_sample)
n_grams_quanteda

# we can then find the top n_grams in the sample
topfeatures(dfm(n_grams_quanteda))

# 2 additional function for syuzhet package

# nrc sentiment of each sentence
get_nrc_sentiment(gomS1)

# get the 'emotional entropy'
mixed_messages(gomS1)
gomS1[4]
mixed_messages(gomS1[4])

