# py-random-useragent

Generate a random User Agent

### Installation

```
pip install py-random-useragent
```

### Usage

``` python
from py_random_useragent import UserAgent

# Обновление списка наиболее популярных браузеров
UserAgent().update_ua()

# Получение UserAgent
ua = UserAgent().get_ua()
print(ua)
```
