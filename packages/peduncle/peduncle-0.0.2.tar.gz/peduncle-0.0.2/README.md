# peduncle

very very very simple DOM based HTML content extraction tool, get rid of boilerplate dressing of a web page[1].

easy but useable

work with python 3.7+



[1] the word comes from [dragnet](https://github.com/dragnet-org/dragnet).

## install

```shell
pip install peduncle
```

## usage

```Python
import requests
from peduncle.peduncle import extract_text

# obtain the raw html
url="https://blog.rust-lang.org/2023/05/29/RustConf.html"
html = requests.get(url).text

# extract
print(extract_text(html))
```

## benchmark

### data

benchmark data comes from [dragnet_data](https://github.com/seomoz/dragnet_data), which contains 1381 web pages.

### result

|        | similarity         | 95%hit_rate | avg_length_gap(char) | length_gap_std     |
| ------ | ------------------ | ----------- | -------------------- | ------------------ |
| a=0.01 | 0.5767456743946341 | 0.22        | -4673.118            | 15343.704819895227 |
| a=025  | 0.8451692708814662 | 0.548       | -2082.988            | 14502.183923390849 |
| a=0.5  | 0.8226224698726087 | 0.47        | -368.696             | 8452.075615349402  |
| a=0.99 | 0.7527591593485807 | 0.292       | 1614.306             | 7917.618208044891  |

- a: alpha, control how much the content extractor tens to extract larger content piece
- similarity: cosine similarity between sparse vectors of answer and extracted text
- 95hit rate: percentage of similarity larger than 95%
- length gap: extracted text length - answer text length
- std: std
