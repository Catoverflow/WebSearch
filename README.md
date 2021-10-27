# WebSearch

## 数据集说明

使用默认的 NLTK lemma 工具时需要先下载 [wordnet](https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet.zip) 和 [stopwords](https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/stopwords.zip)，分别解压到 `nltk_data/corpora/wordnet` 和 `nltk_data/corpora/stopwords`，然后配置环境变量 `NLTK_DATA` 为 `nltk_data` 的位置。当然也可以使用 nltk 自带的 download 功能，不过需要挂代理
## 实现思路

### 数据处理

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
   
5. 为后续检索计算、存储数据集

   - 倒排表

     考虑教材上提供的压缩存储方案，比如为文件分配唯一的短uuid、存储文档间距、使用变长编码（类似 UTF 系列编码的实现方式）等

   - tf-idf

     <s>计算过程没什么好说的，暴力就完事了</s>

     存储的时候记得想办法兼得精确度和空间

6. word2vec 训练（optional）

   要做近义词就进行这一步，具体作用于 semantic search

   将训练完的向量空间进行存储

处理完的数据可以考虑存起来

ref: [学长实验报告](https://github.com/hardyho/WebInfo-Lab/blob/main/lab1/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.md) [Build your semantic document search engine with TF-IDF and Google-USE](https://medium.com/analytics-vidhya/build-your-semantic-document-search-engine-with-tf-idf-and-google-use-c836bf5f27fb)

### bool search

- 可以进行 AND/OR 计算先后次序的优化，类似于矩阵连乘优化算法

- 记得支持括号表示，表达式具体解析实现就用栈

### semantic search

- 检索时计算查询词向量与 tf-idf 夹角 cos 值来判断相关性

- 如果做了 word2vec，在计算夹角时可以考虑纳入 k 个相关词，然后取与文档最近+权重（近义词相关系数乘以 tf-idf 取最大者）最大的加入计算

## 代码框架

仓库结构

~~~~bash
.
├── bool_search.py
├── process.py
├── README.md
├── requirements.txt
├── semantic_search.py
├── utils
│   ├── config.py
│   ├── data_process.py
│   ├── __init__.py
│   ├── inverted_index.py
│   └── tf_idf.py
└── data #this is not tracked by git
    └── 2018-0*
        └── news_*.json
~~~~

`bool_search.py` `semantic_search.py` 是主搜索程序，完成搜索功能

`process.py` 负责一键解析数据集，输出倒排表和 tf-idf 表

`utils` 里为上述程序的后端

`utils/config.py` 负责本次实验的一些配置存储/读取，例如数据集和倒排表位置等

`utils/data_process.py` 负责数据处理，包括处理原文件、解析词根、输出词表等

`utils/tf_idf` 作为 tf-idf 和 semantic search 相关后端

`utils/inverted_index.py` 作为倒排表和 bool search 相关后端

`data` 下存放本次实验的原新闻数据，仅保留在本地

## Todos

- bool search 的近义词支持 by word2vec

- semantic search 加入标题的权重