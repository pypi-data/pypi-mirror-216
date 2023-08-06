# UiB INF100 Graphics

## Installation

**Prerequisites**

Python 3.10 or above.

For Linux users only, the package [pyscreenshot](https://github.com/ponty/pyscreenshot) must be installed for all features to work.

**Installation with pip through the Terminal**

1. Ensure your Python version is version 3.10 or higher. The command
```
python --version
```
should print "Python 3.10.4" or something similar. As long as it is 3.10 or higher, you're ok. If it does not immediately work, you may also try to replace "python" with `python3` or simply `py` (if so, you must make the same replacement for the commands below).

2. Ensure you are using an updated version of pip. Run
```
python -m pip install --upgrade pip
```

3. Install uib-inf100-graphics
```
python -m pip install uib-inf100-graphics
```

The command above will automatically install the following dependencies:

* [requests](https://requests.readthedocs.io/) version 2.28.0 or higher
* [Pillow](https://pillow.readthedocs.io/) version 9.2.0 or higher


**Alternative installation by running a script**

Copy and paste the following code into a python file, and then run it.

```python
import sys
from subprocess import run

package_name = "uib-inf100-graphics"

if ((sys.version_info[0] != 3) or (sys.version_info[1] < 10)):
    raise Exception(f"{package_name} requires Python 3.10 or later. "
            + "Your current version is: "
            + f"{sys.version_info[0]}.{sys.version_info[1]}")

ans = input(f"\n\nType 'yes' to install {package_name}: ")
if ((ans.lower() == "yes") or (ans.lower() == "y")):
    print()
    cmd_pip_update = f"{sys.executable} -m pip install --upgrade pip"
    print(f"Will attempt to update pip now with command: {cmd_pip_update}")
    run(cmd_pip_update.split())
    
    print()
    cmd_install = f"{sys.executable} -m pip install {package_name}"
    print(f"Will attempt to install {package_name} now with command: {cmd_install}")
    run(cmd_install.split())
else:
    print(f"Did not attempt to install {package_name} now")
print("\n")
```


## Sample usage

### Open a blank window

```python
from uib_inf100_graphics import run_app
run_app(width=400, height=200)
```

### Open a window and display something


```python
from uib_inf100_graphics import run_app

def redraw_all(app, canvas):
    canvas.create_rectangle(100, 50, 300, 150, fill='maroon')
    canvas.create_oval(100, 50, 300, 150, fill='purple', outline='white')
    canvas.create_line(100, 50, 150, 150, fill='#68ebff', width=5)
    canvas.create_polygon(100, 30, 200, 50, 300, 30, 200, 10, 
                          fill='#fed', width = 5, outline='black')
    canvas.create_text(200, 100, text='INF100', fill='yellow',
                       font='Helvetica 26 bold underline')

run_app(width=400, height=200)
```


### Animate with a timer

```python
from uib_inf100_graphics import run_app

def app_started(app):
    # Define variables to use
    app.x_offset = 0

def timer_fired(app):
    # Update variable periodically with a timer
    app.x_offset += 10
    if (app.x_offset > 300):
        app.x_offset = 0

def redraw_all(app, canvas):
    # Draw a ball, and position it depending on state of variables
    x1 = 10 + app.x_offset
    y1 = 50
    x2 = x1 + 20
    y2 = y1 + 20
    canvas.create_oval(x1, y1, x2, y2, fill="yellow")

run_app(width=400, height=100)
```

### React to keyboard input


```python
from uib_inf100_graphics import run_app

def app_started(app):
    # Define variables to use
    app.x_offset = 0
    app.y_offset = 0
    app.radius = 20

def key_pressed(app, event):
    # Update variables when a key is pressed
    if   (event.key == "Left"):  app.x_offset -= 10
    elif (event.key == "Right"): app.x_offset += 10
    elif (event.key == "Up"):    app.y_offset -= 10
    elif (event.key == "Down"):  app.y_offset += 10
    elif (event.key == "Space"): app.radius += 1
    elif (event.key == "m"):     app.radius -= 1

def redraw_all(app, canvas):
    # Draw a ball, and position it depending on state of variables
    cx = (app.width / 2) + app.x_offset
    cy = app.height / 2 + app.y_offset
    r = app.radius
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="yellow")

run_app(width=400, height=100)
```


### React to mouse input

```python
from uib_inf100_graphics import run_app

def app_started(app):
    # Define variables to use, and set initial values
    app.cx = app.width / 2
    app.cy = app.height / 2
    app.radius = 20

def mouse_pressed(app, event):
    # Update variables when mouse is pressed
    app.cx = event.x
    app.cy = event.y

def redraw_all(app, canvas):
    # Draw a ball, and position it depending on state of variables
    canvas.create_oval(
        app.cx - app.radius, 
        app.cy - app.radius,
        app.cx + app.radius,
        app.cy + app.radius,
        fill="yellow"
    )

run_app(width=400, height=100)
```


### Use with type hints

```python
from uib_inf100_graphics import run_app
from uib_inf100_graphics.types import AppBase, MouseEvent, KeyEvent, Canvas

class App(AppBase):
    # Define types of variables to use
    cx: float
    cy: float
    radius: float

def app_started(app: App) -> None:
    # Set initial values of all variables
    app.cx = app.width / 2
    app.cy = app.height / 2
    app.radius = 20

def timer_fired(app: App) -> None:
    # Update variables every time timer fires
    app.cx += 1
    app.cy += 1

def key_pressed(app: App, event: KeyEvent) -> None:
    # Update variables if keys are pressed
    if event.key == "Up":
        app.radius += 1
    elif event.key == "Down":
        app.radius -= 1

def mouse_pressed(app: App, event: MouseEvent) -> None:
    # Update variables when mouse is pressed
    app.cx = event.x
    app.cy = event.y

def redraw_all(app: App, canvas: Canvas) -> None:
    # Draw a ball, and position it depending on state of variables
    canvas.create_oval(
        app.cx - app.radius, 
        app.cy - app.radius,
        app.cx + app.radius,
        app.cy + app.radius,
        fill="yellow"
    )

run_app(width=400, height=100)
```