# peduncle

very very very simple DOM based HTML content extraction tool (less than 100 line)

easy but useable

work with python 3.7+

## usage

```Python
import requests
from grader import Grader

# obtain the raw html
url="https://blog.rust-lang.org/2023/05/29/RustConf.html"
html = requests.get(url).text

# then you get content
G = Grader(html)
print(G.main_node.text)
```

