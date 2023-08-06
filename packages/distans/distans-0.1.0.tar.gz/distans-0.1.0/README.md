# distans
Different distances for Python


## Install

```sh
pip install distans
```

## Usage

### Lp distance

```py
from distans import lp

a = [1, -2, 3]
b = [3, 4, -5]

norm = lp(a, p=4)
dist = lp(a, b, p=3)
```

### Edit similarity

```py
from distans import jaro_sim, jaro_winkler_sim

jaro_sim('hello', 'helo')
jaro_winkler_sim('hi', 'hey')
```
