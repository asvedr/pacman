# For Xenia:

use this code to run logic module in parallel process
```python
logic = Logic.load_file(...)
```
you can get `Field` object using
```python
logic.field
```
For getting actual information about ghosts pacman and eated dots use
```python
info = logic.get_info()
# info is tuple of
(pacman, ghosts, eated_dots) = info
# where pacman is
(x,y) = pacman
# ghosts is list of 
[..., (x, y, color), ...] = ghosts
# and eated dots is list of
[..., (x,y), ...] = eated_dots
```