# WebSearch

Chinese Report for this experiment is [report.md](./report.md). Original news data crawled is ~1.9G, and will not be provided here. While you can download the [processed data](https://drive.google.com/file/d/1Snm6uNhU4FYfE4flS0hBDkuIjeR7Q4jO/view?usp=sharing).

To use this search engine, you need to extract `output.zip` to `./output` folder, and just run `bool_search.py` or `semantic_search.py`

## Dependencies

- Install pip dependencies

    `pip install -r requirements.txt`

- Download NLTK data and set `NLTK_DATA` to download path.

    [wordnet](https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet.zip) -> `NLTK_DATA/corpora/wordnet`

    [stopwords](https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/stopwords.zip) -> `NLTK_DATA/corpora/stopwords`

- Download pre-processed data(stated above)

You can adjust some parameters in source code to get better searching experience.