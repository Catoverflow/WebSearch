# WebSearch

Chinese Report for this experiment is [report.md](./report.md). Original news data crawled is ~1.9G, and will not be provided here. While you can download the [processed data](https://drive.google.com/file/d/1Snm6uNhU4FYfE4flS0hBDkuIjeR7Q4jO/view?usp=sharing).

To use this search engine, you need to extract `output.zip` to `./output` folder, and just run `bool_search.py` or `semantic_search.py`, `process.py` is used for process raw data and generated output only.

> Note: The code quality is broken including but not limited to ill-formed class methods, mixed OPP and OOP codes, etc. Please issue pull requests if you want to make it better, the authors are just too busy or lazy to fix these.

## Dependencies

- Install pip dependencies

    `pip install -r requirements.txt`

- Download NLTK data and set `NLTK_DATA` to download path.

    [wordnet](https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet.zip) -> `NLTK_DATA/corpora/wordnet`

    [stopwords](https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/stopwords.zip) -> `NLTK_DATA/corpora/stopwords`

- Download pre-processed data(stated above)

You can adjust some parameters in source code to get better searching experience.

## Credits

Thanks to [SuzanaK](https://github.com/SuzanaK) for synonyms list (licensed under [BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/)), and all open source tools used in this project.