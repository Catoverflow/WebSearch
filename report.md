# Web 信息处理与应用 实验一

## 实验目的

本实验要求以给定的财经新闻数据集为基础,实现一个新闻搜索引擎。对于给定的查询,能够以精确查
询或模糊语义匹配的方式返回最相关的一系列新闻文档。

## 实验要求

### 实现 bool 检索和语义检索 

- [x]  对预处理文档集合生成倒排索引表，并以合适的方式存储生成的倒排索引文件

- [x]  对于给定的 bool 查询规则，根据生成的倒排表返回符合查询规则的文档集合

- [x]  根据预处理文档集合，计算每个文档的 tf-idf 向量并以矩阵形式存储

- [x]  对于给定的语义查询，根据文档向量与查询向量的相似度返回前10个最相关的文档

### 选做内容

- [x] 对于倒排索引进行时/空复杂度优化

  近义词合并、压缩算法、紧凑数据结构

  通过并行计算引入了常数级优化

- [x] 采用外部知识库优化索引效果

  采用了预标记近义词表

- [ ] 采用 `word2vec` 等其他语义表征方式表征查询和文档，并选用合适的案例与 `tf-idf` 的结果进行对比分析。

  太费时间了摸了

- [x] 对于给定的语义查询，返回10张最相关图片

  > 对应代码为 `utils/img.py`

## 实验过程

### 目录结构

~~~~bash
├── bool_search.py
├── dataset
│   └── english_synonyms_and_antonyms.csv
├── output
│   ├── dictionary.zstd
│   ├── headerdata.zstd
│   ├── header_tf_idf_matrix.zstd
│   ├── inverted_index.zstd
│   ├── metadata.zstd
│   └── tf_idf_matrix.zstd
├── process.py
├── README.md
├── report.md
├── requirements.txt
├── semantic_search.py
└── utils
    ├── config.py
    ├── data_process.py
    ├── img.py
    ├── __init__.py
    ├── inverted_index.py
    ├── __pycache__
    │   ├── data_process.cpython-39.pyc
    │   ├── img.cpython-39.pyc
    │   ├── __init__.cpython-39.pyc
    │   ├── inverted_index.cpython-39.pyc
    │   └── tf_idf.cpython-39.pyc
    └── tf_idf.py
~~~~

`utils` 下存放相关工具，根目录下的 `semantic_search.py` 和 `bool_search.py` 为本次实验的查询程序

### Bool 检索和语义检索

#### 设计思路

##### 数据结构

> 本部分对应代码 `utils/inverted_index.py`、`utils/tf_idf.py`

倒排表和教材上的实现方法相同（有序表），但并没有加入跳表指针，因为会增加数据结构复杂度，并且目前没有跳表指针的情况下搜索延迟已经令人满意。

TF-IDF 矩阵由于是非常稀疏的矩阵，采用修改的三元组方式存储，数据结构为

`[文档1],[文档2],[文档3],...,[文档306000]`

文档数据结构为

`词1:值1,词2:值2,...词1000:值1000`

##### 数据处理

> 本部分对应代码 `utils/data_process.py`

从原文档到目标数据的处理过程如下：

1. 预处理

   小写化、使用正则替换过滤不需要的字段（链接、邮箱、时间、标点和非 ASCII 字符等）

2. 分词

   本实验直接根据空格分词。对于英文不是很有必要调用分词引擎（如 `nltk` 提供的）

3. 去除停用词

   使用 `nltk` 提供的停用词表

4. 标准化 Lemmatize

   在实验初尝试了 `nltk` 库和 `spacy` 库提供的不同标准化引擎，比较发现 `spacy` 提供的引擎速度过慢，于是最后采用 `nltk` 提供的引擎

   __并行处理__

   在解决了倒排表计算复杂度的问题之后，标准化成为了数据处理的瓶颈。由于在数个小时的处理后误删了生成文件（以为索引了重复文档，实际上是爬取的文档存在重复），作者不得不写了并行优化，参见 `multi_process` 函数。在实践中对全部文档的总处理时间降到了 1h 以内。

5. 计算倒排表

   > 本部分对应代码 `utils/inverted_index.py`

   由于计算 TF-IDF 时用到的 IDF 可以很方便地通过倒排表长取得，故先生成倒排表。计算过程非常简单，遍历即可

   在实验中碰到的问题在于：在文档中遇到一个单词，判断该文档 id 是否在该单词倒排表里时，起初采用了 `if docid in inverted_index[wordid]` 的表达式，测试时由于数据规模小顺利完成。直到对全部数据进行处理时才发现这样的操作时间复杂度为 `o(doc)`，与外部循环一起提供 `o(doc^2)`，造成复杂度爆炸。由于倒排表是有序数据结构，后来改为了 `if docid != inverted_index[wordid][-1]`，直接与表尾比较，总复杂度优化为了 `o(n)`，才顺利进行下去

6. 计算 TF-IDF 表

   > 本部分对应代码 `utils/tf_idf.py`

   通过之前的倒排表直接取得单词的 IDF 值，然后乘以 TF 便得到结果。

   需要注意的地方在于 TF-IDF 是稀疏表，三元组比矩阵更适合用来表示 TF-IDF。在本次实验之初就已迁移到三元组

##### 存储结构（时空优化）

> 本部分对应代码 `./process.py`

由于设计紧凑的数据结构不如在外部调用压缩算法，本实验的存储过程为：

建立单词-id 映射 -> 序列化数据结构（pickle） -> 压缩数据流（zstd）-> 存储到文件

存储的文件为：映射表、文档和标题各自的 TF-IDF 表、合并后的倒排表和元数据表（供返回可读的搜索结果）

单独维护一个单词-id 的映射表（在后续实验中也方便了同义词定向），存储索引和仅含 id 的数据，减少了单词带来的空间开销（虽然这样的开销很容易被外层压缩算法优化，但是可以优化占用内存空间）

序列化数据结构采用了现有的 pickle 库，省去了现场造轮子的工作量。不过 pickle 库存在安全问题，由于在本次实验中不会带来影响所以仍然采用。

压缩算法会带来压缩/解压的时间开销。由于本次实验在生成数据时的开销不影响搜索体验，仅需关注解压的时间开销即可。为了最小化解压时间开销，本实验使用了工业界的高速解压算法 zstd，相关的 benchmark 可在[主页](http://facebook.github.io/zstd/)上找到，解压速度相较同类算法有较大提升，在搜索时也确实大幅降低了延迟。

##### 近义词合并

> 本部分对应数据 `dataset/english_synonyms_and_antonyms.csv`
> 对应代码 `utils/data_process.py`

在 bool 检索中加入近义词合并可以提升搜索准确率。本实验采用了[预标记近义词表](*github.com/SuzanaK/english_synonyms_antonyms_list*)，在数据处理时就合并近义词，使其指向同一个独立单词 id（映射关系存储在 `output/dictionary` 下）。在提高搜索准确率的同时也带来了略微的存储空间优化。

__word2vec__

一开始本实验打算使用 word2vec 来进行近义词筛选，在下载了 [Google News 的数据集](https://github.com/RaRe-Technologies/gensim-data/releases/download/word2vec-google-news-300)后，发现结果非常不尽如人意，故转而采用预标记近义词表。

##### 优化结果

~~~~bash
ls -l output 
total 552628
-rw-r--r-- 1 catoverflow catoverflow   9693454 Oct 30 17:40 dictionary.zstd
-rw-r--r-- 1 catoverflow catoverflow    155657 Oct 30 15:45 headerdata.zstd
-rw-r--r-- 1 catoverflow catoverflow  14987918 Oct 30 17:40 header_tf_idf_matrix.zstd
-rw-r--r-- 1 catoverflow catoverflow  90656838 Oct 30 17:37 inverted_index.zstd
-rw-r--r-- 1 catoverflow catoverflow  20280883 Oct 30 17:40 metadata.zstd
-rw-r--r-- 1 catoverflow catoverflow 430092912 Oct 30 17:40 tf_idf_matrix.zstd
~~~~

处理后的倒排表大小约 90MB，TF-IDF 矩阵总大小约为 445 MB，索引表大小为 9.6 MB。

#### 搜索过程

- Bool 检索

  > 本部分对应代码为 `./bool_search.py`

  直接根据表达式依次合并各单词的倒排表得到结果，用栈处理括号优先级，从左到右完成计算。

  一开始使用了 `set` 作为数据结构，使用现成的 `union` 等方法完成计算。但由于这些方法无法很好地利用倒排表的有序性，时间复杂度为 `o(nlogn)` 高于 `o(n)`，后来改为手动直接合并。

  起初合并时参考了矩阵连乘优化方法，打算通过变更计算次序来优化计算量。但后来发现 `and or not` 的组合是不满足交换律的，故放弃。且直接合并速度已经让人满意。

- 语义检索

  > 本部分对应代码为 `./semantic_search.py`

  直接计算文档 TF-IDF 向量与查询词 TF 向量相似度，返回最相似的结果。

  在计算复杂度的优化中采用了剪枝：如果命中单词过少直接抛弃结果（line 32 `threshold`）

  __夹角相似度的问题__

  使用 [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) 来[计算文档与查询词的相关性](https://medium.com/analytics-vidhya/build-your-semantic-document-search-engine-with-tf-idf-and-google-use-c836bf5f27fb)其实是一种问题很大的算法。

  因为正常人在搜索的时候都不会把一个搜索词写两遍，结果就是每个词的权重（TF 值）相等。这种情况下用 cosine similarity 去计算只能得到每个词出现率乘以倒排值最相近的文档，而不是出现率最高的（一个比较极端但是确实占据了测试结果一半的例子是：两个词各出现一次，在倒排值相同的情况下）。

  本实验为了避免该问题，引入了长度的权重（line 32 `len_weight`）与使用 min-max scaling标准化处理（参见 `utils/td_idf.py normalization`）之后的 TF-IDF 夹角进行合并。另一种方法是计算加权乘积或者直接优雅地使用向量点积。

- 标题检索

  由于标题囊括了整个文档的信息，不加入检索就太浪费了呢。

  bool 检索中标题内容与文档内容合并加入倒排表计算，语义检索中标题拥有独立的权重（line 32 `header_weight`）

- 轮子使用

  倒排表和 TF-IDF 都有很多库提供了现成的方法，如 `ski-learn`, `gensim`, `nltk` 等。但由于计算中如果使用现有标准无法进行数据结构优化（如使用阈值进行剪枝等），且直接实现复杂度不高，故在本次实验中搜索部分没有采用现成的库。
