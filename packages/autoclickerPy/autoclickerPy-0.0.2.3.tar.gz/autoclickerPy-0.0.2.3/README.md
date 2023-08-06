# Autoclicker

Simple autoclicker in python.

## How to use

Running the autoclicker for some time

```python
from autoclickerPy import Autoclicker
from pynput.mouse import Button

clicker = Autoclicker(delay=0.1)

# Runs autoclicker for 1 second
clicker.run(1)
```

Starting and stoping the autoclicker

```python
from autoclickerPy import Autoclicker
from pynput.mouse import Button
import time

clicker = Autoclicker(delay=0.1)

clicker.start(button=Button.middle)
 ... some code ...
clicker.stop()
```