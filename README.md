# WebSearch

## 实现思路

#### 数据处理

步骤如下：

1. preprocess
   - lowercase
   - 移除符号、utf8 字符、email 等

2. tokenize

   英文分词可使用 python `nltk` 库提供的，但实际上 `split(' ')` 已经足够（英文不太需要分词）

3. stop words

   可以直接从网上下载停用词表

4. lemmatize

   可以使用 CoreNLP 的 lemma 或者 nltk 的 PorterStemmer

   这个部分一般是耗时最多的，可以考虑进行缓存优化

处理完的数据可以考虑存起来

ref: [学长实验报告](https://github.com/hardyho/WebInfo-Lab/blob/main/lab1/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.md) [Build your semantic document search engine with TF-IDF and Google-USE](https://medium.com/analytics-vidhya/build-your-semantic-document-search-engine-with-tf-idf-and-google-use-c836bf5f27fb)

#### bool search

步骤同教材一样：

1. 计算、存储倒排表

   注意存储空间优化，比如为文件分配唯一的短uuid、存储文档间距、使用变长编码（同教材，类似 UTF 系列编码的实现方式）等

2. bool search

   可以进行 AND/OR 计算先后次序的优化，类似于矩阵连乘优化算法

   记得支持括号表示，表达式具体解析实现就用栈

### semantic search

   - [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) 可以和倒排表一起计算，也可以在倒排表算完以后根据倒排表提供的索引计算
   - 查询时计算相关性不用计算距离，建议计算（ref2）向量夹角来判断相关性，计算可以使用 `numpy` 简化