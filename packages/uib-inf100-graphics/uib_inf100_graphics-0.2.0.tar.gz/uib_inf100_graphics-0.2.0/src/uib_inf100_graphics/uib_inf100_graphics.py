# uib_inf100_graphics.py

# Require Python 3.10 or later
import sys
if ((sys.version_info[0] != 3) or (sys.version_info[1] < 10)):
    raise Exception('uib_inf100_graphics requires Python version 3.10 or later.')

from .version import __version__, __last_updated__

# Track version and file update timestamp
MAJOR_VERSION = int(__version__.split('.')[0])
MINOR_VERSION = float(__version__[(__version__.index('.')+1):])
LAST_UPDATED  = __last_updated__

from typing import Any
from tkinter import *
from tkinter import messagebox, simpledialog, filedialog
import inspect, copy, traceback
import sys, os
from io import BytesIO

def failed_import(importName, installName=None):
    installName = installName or importName
    print('**********************************************************')
    print(f'** Cannot import {importName} -- it seems you need to install {installName}')
    print(f'** This may result in limited functionality or even a runtime error.')
    print('**********************************************************')
    print()

try: from PIL import Image, ImageTk, ImageDraw, ImageFont
except ModuleNotFoundError: failed_import('PIL', 'pillow')

if sys.platform.startswith('linux'):
    try: import pyscreenshot as ImageGrabber
    except ModuleNotFoundError: failed_import('pyscreenshot')
else:
    try: from PIL import ImageGrab as ImageGrabber
    except ModuleNotFoundError: pass # Our PIL warning is already printed above

try: import requests
except ModuleNotFoundError: failed_import('requests')

def get_hash(obj):
    # This is used to detect MVC violations in redraw_all
    # @TODO: Make this more robust and efficient
    try:
        return get_hash(obj.__dict__)
    except:
        if (isinstance(obj, list)): return get_hash(tuple([get_hash(v) for v in obj]))
        elif (isinstance(obj, set)): return get_hash(sorted(obj))
        elif (isinstance(obj, dict)): return get_hash(tuple([obj[key] for key in sorted(obj)]))
        else:
            try: return hash(obj)
            except: return get_hash(repr(obj))

class WrappedCanvas(Canvas):
    # Enforces MVC: no drawing outside calls to redraw_all
    # Logs draw calls (for autograder) in canvas.logged_drawing_calls
    def __init__(wrapped_canvas, app):
        wrapped_canvas.logged_drawing_calls = [ ]
        wrapped_canvas.log_drawing_calls = True
        wrapped_canvas.in_redraw_all = False
        wrapped_canvas.app = app
        super().__init__(app._root, width=app.width, height=app.height)

    def log(self, method_name, args, kwargs):
        if (not self.in_redraw_all):
            self.app._mvc_violation('you may not use the canvas (the view) outside of redraw_all')
        if (self.log_drawing_calls):
            self.logged_drawing_calls.append((method_name, args, kwargs))

    def create_arc(self, *args, **kwargs): self.log('create_arc', args, kwargs); return super().create_arc(*args, **kwargs)
    def create_bitmap(self, *args, **kwargs): self.log('create_bitmap', args, kwargs); return super().create_bitmap(*args, **kwargs)
    def create_line(self, *args, **kwargs): self.log('create_line', args, kwargs); return super().create_line(*args, **kwargs)
    def create_oval(self, *args, **kwargs): self.log('create_oval', args, kwargs); return super().create_oval(*args, **kwargs)
    def create_polygon(self, *args, **kwargs): self.log('create_polygon', args, kwargs); return super().create_polygon(*args, **kwargs)
    def create_rectangle(self, *args, **kwargs): self.log('create_rectangle', args, kwargs); return super().create_rectangle(*args, **kwargs)
    def create_text(self, *args, **kwargs): self.log('create_text', args, kwargs); return super().create_text(*args, **kwargs)
    def create_window(self, *args, **kwargs): self.log('create_window', args, kwargs); return super().create_window(*args, **kwargs)

    def create_image(self, *args, **kwargs):
        self.log('create_image', args, kwargs);
        uses_image = 'image' in kwargs
        uses_pil_image = 'pil_image' in kwargs
        if ((not uses_image) and (not uses_pil_image)):
            raise Exception('create_image requires an image to draw')
        elif (uses_image and uses_pil_image):
            raise Exception('create_image cannot use both an image and a pil_image')
        elif (uses_pil_image):
            pil_image = kwargs['pil_image']
            del kwargs['pil_image']
            if (not isinstance(pil_image, Image.Image)):
                raise Exception('create_image: pil_image value is not an instance of a PIL/Pillow image')
            image = ImageTk.PhotoImage(pil_image)
        else:
            image = kwargs['image']
            if (isinstance(image, Image.Image)):
                raise Exception('create_image: image must not be an instance of a PIL/Pillow image\n' +
                    'You perhaps meant to convert from PIL to Tkinter, like so:\n' +
                    '     canvas.create_image(x, y, image=ImageTk.PhotoImage(image))')
        kwargs['image'] = image
        return super().create_image(*args, **kwargs)

class App(object):
    major_version = MAJOR_VERSION
    minor_version = MINOR_VERSION
    version = f'{major_version}.{minor_version}'
    last_updated = LAST_UPDATED
    _theRoot = None # singleton Tkinter root object

    ####################################
    # User Methods:
    ####################################
    def redraw_all(app, canvas): pass      # draw (view) the model in the canvas
    def app_started(app): pass           # initialize the model (app.xyz)
    def app_stopped(app): pass           # cleanup after app is done running
    def key_pressed(app, event): pass    # use event.key
    def key_released(app, event): pass   # use event.key
    def mouse_pressed(app, event): pass  # use event.x and event.y
    def mouse_released(app, event): pass # use event.x and event.y
    def mouse_moved(app, event): pass    # use event.x and event.y
    def mouse_dragged(app, event): pass  # use event.x and event.y
    def timer_fired(app): pass           # respond to timer events
    def size_changed(app): pass          # respond to window size changes

    ####################################
    # Implementation:
    ####################################

    def __init__(app, width=300, height=300, x=0, y=0, title=None, autorun=True, mvc_check=True, log_drawing_calls=True):
        app.winx, app.winy, app.width, app.height = x, y, width, height
        app.timer_delay = 100     # milliseconds
        app.mouse_movedDelay = 50 # ditto
        app._title = title
        app._mvc_check = mvc_check
        app._log_drawing_calls = log_drawing_calls
        app._running = app._paused = False
        app._mouse_pressed_outside_window = False
        if autorun: app.run()

    def __repr__(app):
        keys = set(app.__dict__.keys())
        key_values = [ ]
        for key in sorted(keys - app._ignoredFields):
            key_values.append(f'{key}={app.__dict__[key]}')
        return f'App({", ".join(key_values)})'

    def set_size(app, width, height):
        app._root.geometry(f'{width}x{height}')

    def set_position(app, x, y):
        app._root.geometry(f'+{x}+{y}')

    def show_message(app, message):
        messagebox.showinfo('show_message', message, parent=app._root)

    def get_user_input(app, prompt):
        return simpledialog.askstring('get_user_input', prompt)

    def load_image(app, path=None):
        if (app._canvas.in_redraw_all):
            raise Exception('Cannot call load_image in redraw_all')
        if (path is None):
            path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select file: ',filetypes = (('Image files','*.png *.gif *.jpg'),('all files','*.*')))
            if (not path): return None
        if (path.startswith('http')):
            response = requests.request('GET', path) # path is a URL!
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(path)
        return image

    def scale_image(app, image, scale, antialias=False):
        # antialiasing is higher-quality but slower
        resample = Image.ANTIALIAS if antialias else Image.NEAREST
        return image.resize((round(image.width*scale), round(image.height*scale)), resample=resample)

    def get_snapshot(app):
        app._show_root_window()
        x0 = app._root.winfo_rootx() + app._canvas.winfo_x()
        y0 = app._root.winfo_rooty() + app._canvas.winfo_y()
        result = ImageGrabber.grab((x0,y0,x0+app.width,y0+app.height))
        return result

    def save_snapshot(app):
        path = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Select file: ',filetypes = (('png files','*.png'),('all files','*.*')))
        if (path):
            # defer call to let filedialog close (and not grab those pixels)
            if (not path.endswith('.png')): path += '.png'
            app._deferred_method_call(afterId='save_snapshot', afterDelay=0, afterFn=lambda:app.get_snapshot().save(path))

    def toggle_paused(app):
        app._paused = not app._paused

    def quit(app):
        app._running = False
        app._root.quit() # break out of root.mainloop() without closing window!

    def __setattr__(app, attr, val):
        d = app.__dict__
        d[attr] = val
        canvas = d.get('_canvas', None)
        if (d.get('running', False) and
            d.get('mvc_check', False) and
            (canvas is not None) and
            canvas.in_redraw_all):
            app._mvc_violation(f'you may not change app.{attr} in the model while in redraw_all (the view)')

    def _print_user_traceback(app, exception, tb):
        stack = traceback.extract_tb(tb)
        lines = traceback.format_list(stack)
        in_redraw_all_wrapper = False
        print_lines = [ ]
        for line in lines:
            if (('"uib_inf100_graphics.py"' not in line) and
                ('/uib_inf100_graphics.py' not in line) and
                ('\\uib_inf100_graphics.py' not in line) and
                ('/tkinter/' not in line) and
                ('\\tkinter\\' not in line)):
                print_lines.append(line)
            if ('redraw_all_wrapper' in line):
                in_redraw_all_wrapper = True
        if (len(print_lines) == 0):
            # No user code in trace, so we have to use all the code (bummer),
            # but not if we are in a redraw_all_wrapper...
            if in_redraw_all_wrapper:
                print_lines = ['    No traceback available. Error occurred in redraw_all.\n']
            else:
                print_lines = lines
        print('Traceback (most recent call last):')
        for line in print_lines: print(line, end='')
        print(f'Exception: {exception}')

    def _safe_method(app_method):
        def m(*args, **kwargs):
            app = args[0]
            try:
                return app_method(*args, **kwargs)
            except Exception as e:
                app._running = False
                app._print_user_traceback(e, sys.exc_info()[2])
                if ('_canvas' in app.__dict__):
                    app._canvas.in_redraw_all = True # not really, but stops recursive MVC Violations!
                    app._canvas.create_rectangle(0, 0, app.width, app.height, fill=None, width=10, outline='red')
                    app._canvas.create_rectangle(10, app.height-50, app.width-10, app.height-10,
                                                 fill='white', outline='red', width=4)
                    app._canvas.create_text(app.width/2, app.height-40, text=f'Exception! App Stopped!', fill='red', font='Arial 12 bold')
                    app._canvas.create_text(app.width/2, app.height-20, text=f'See console for details', fill='red', font='Arial 12 bold')
                    app._canvas.update()
                app.show_message(f'Exception: {e}\nClick ok then see console for details.')
        return m

    def _method_is_overridden(app, method_name):
        return (getattr(type(app), method_name) is not getattr(App, method_name))

    def _mvc_violation(app, errMsg):
        app._running = False
        raise Exception('MVC Violation: ' + errMsg)

    @_safe_method
    def _redraw_all_wrapper(app):
        if (not app._running): return
        if ('deferred_redraw_all' in app._afterIdMap): return # wait for pending call
        app._canvas.in_redraw_all = True
        app._canvas.delete(ALL)
        width,outline = (10,'red') if app._paused else (0,'white')
        app._canvas.create_rectangle(0, 0, app.width, app.height, fill='white', width=width, outline=outline)
        app._canvas.logged_drawing_calls = [ ]
        app._canvas.log_drawing_calls = app._log_drawing_calls
        hash1 = get_hash(app) if app._mvc_check else None
        try:
            app.redraw_all(app._canvas)
            hash2 = get_hash(app) if app._mvc_check else None
            if (hash1 != hash2):
                app._mvc_violation('you may not change the app state (the model) in redraw_all (the view)')
        finally:
            app._canvas.in_redraw_all = False
        app._canvas.update()

    def _deferred_method_call(app, afterId, afterDelay, afterFn, replace=False):
        def afterFn_wrapper():
            app._afterIdMap.pop(afterId, None)
            afterFn()
        id = app._afterIdMap.get(afterId, None)
        if ((id is None) or replace):
            if id: app._root.after_cancel(id)
            app._afterIdMap[afterId] = app._root.after(afterDelay, afterFn_wrapper)

    def _deferred_redraw_all(app):
        app._deferred_method_call(afterId='deferred_redraw_all', afterDelay=100, afterFn=app._redraw_all_wrapper, replace=True)

    @_safe_method
    def _app_started_wrapper(app):
        app.app_started()
        app._redraw_all_wrapper()

    _keyNameMap = { '\t':'Tab', '\n':'Enter', '\r':'Enter', '\b':'Backspace',
                   chr(127):'Delete', chr(27):'Escape', ' ':'Space' }

    @staticmethod
    def _use_event_key(attr):
        raise Exception(f'Use event.key instead of event.{attr}')

    @staticmethod
    def _getEventKeyInfo(event, keysym, char):
        key = c = char
        has_control_key = (event.state & 0x4 != 0)
        if ((c in [None, '']) or (len(c) > 1) or (ord(c) > 255)):
            key = keysym
            if (key.endswith('_L') or
                key.endswith('_R') or
                key.endswith('_Lock')):
                key = 'Modifier_Key'
        elif (c in App._keyNameMap):
            key = App._keyNameMap[c]
        elif ((len(c) == 1) and (1 <= ord(c) <= 26)):
            key = chr(ord('a')-1 + ord(c))
            has_control_key = True
        if has_control_key and (len(key) == 1):
            # don't add control- prefix to Enter, Tab, Escape, ...
            key = 'control-' + key
        return key

    class EventWrapper(Event):
        def __init__(self, event):
            for key in event.__dict__:
                if (not key.startswith('__')):
                    self.__dict__[key] = event.__dict__[key]

    class MouseEventWrapper(EventWrapper):
        def __repr__(self):
            return f'Event(x={self.x}, y={self.y})'

    class KeyEventWrapper(EventWrapper):
        def __init__(self, event):
            keysym, char = event.keysym, event.char
            del event.keysym
            del event.char
            super().__init__(event)
            self.key = App._getEventKeyInfo(event, keysym, char)
            self.ctrl  = (event.state & 0x4) != 0
            self.alt   = (event.state & 0x8) != 0 or (event.state & 0x80) != 0
            self.shift = (event.state & 0x1) != 0
        def __repr__(self):
            return f'Event(key={repr(self.key)})'
        keysym = property(lambda *args: App._use_event_key('keysym'),
                          lambda *args: App._use_event_key('keysym'))
        char =   property(lambda *args: App._use_event_key('char'),
                          lambda *args: App._use_event_key('char'))

    @_safe_method
    def _key_pressed_wrapper(app, event):
        event = App.KeyEventWrapper(event)
        if (event.key == 'control-s'):
            app.save_snapshot()
        elif (event.key == 'control-p'):
            app.toggle_paused()
            app._redraw_all_wrapper()
        elif (event.key == 'control-q'):
            app.quit()
        elif (event.key == 'control-x'):
            os._exit(0) # hard exit avoids tkinter error messages
        elif (app._running and
              (not app._paused) and
              app._method_is_overridden('key_pressed') and
              (not event.key == 'Modifier_Key')):
            app.key_pressed(event)
            app._redraw_all_wrapper()

    @_safe_method
    def _key_released_wrapper(app, event):
        if (not app._running) or app._paused or (not app._method_is_overridden('key_released')): return
        event = App.KeyEventWrapper(event)
        if (not event.key == 'Modifier_Key'):
            app.key_released(event)
            app._redraw_all_wrapper()

    @_safe_method
    def _mouse_pressed_wrapper(app, event):
        if (not app._running) or app._paused: return
        if ((event.x < 0) or (event.x > app.width) or
            (event.y < 0) or (event.y > app.height)):
            app._mouse_pressed_outside_window = True
        else:
            app._mouse_pressed_outside_window = False
            app._mouse_is_pressed = True
            app._lastMousePosn = (event.x, event.y)
            if (app._method_is_overridden('mouse_pressed')):
                event = App.MouseEventWrapper(event)
                app.mouse_pressed(event)
                app._redraw_all_wrapper()

    @_safe_method
    def _mouse_released_wrapper(app, event):
        if (not app._running) or app._paused: return
        app._mouse_is_pressed = False
        if app._mouse_pressed_outside_window:
            app._mouse_pressed_outside_window = False
            app._size_changed_wrapper()
        else:
            app._lastMousePosn = (event.x, event.y)
            if (app._method_is_overridden('mouse_released')):
                event = App.MouseEventWrapper(event)
                app.mouse_released(event)
                app._redraw_all_wrapper()

    @_safe_method
    def _timer_fired_wrapper(app):
        if (not app._running) or (not app._method_is_overridden('timer_fired')): return
        if (not app._paused):
            app.timer_fired()
            app._redraw_all_wrapper()
        app._deferred_method_call(afterId='_timer_fired_wrapper', afterDelay=app.timer_delay, afterFn=app._timer_fired_wrapper)

    @_safe_method
    def _size_changed_wrapper(app, event=None):
        if (not app._running): return
        if (event and ((event.width < 2) or (event.height < 2))): return
        if (app._mouse_pressed_outside_window): return
        app.width,app.height,app.winx,app.winy = [int(v) for v in app._root.winfo_geometry().replace('x','+').split('+')]
        if (app._lastWindowDims is None):
            app._lastWindowDims = (app.width, app.height, app.winx, app.winy)
        else:
            newDims =(app.width, app.height, app.winx, app.winy)
            if (app._lastWindowDims != newDims):
                app._lastWindowDims = newDims
                app.update_title()
                app.size_changed()
                app._deferred_redraw_all() # avoid resize crashing on some platforms

    @_safe_method
    def _mouse_motion_wrapper(app):
        if (not app._running): return
        mouse_moved_exists = app._method_is_overridden('mouse_moved')
        mouse_dragged_exists = app._method_is_overridden('mouse_dragged')
        if ((not app._paused) and
            (not app._mouse_pressed_outside_window) and
            (((not app._mouse_is_pressed) and mouse_moved_exists) or
             (app._mouse_is_pressed and mouse_dragged_exists))):
            class MouseMotionEvent(object): pass
            event = MouseMotionEvent()
            root = app._root
            event.x = root.winfo_pointerx() - root.winfo_rootx()
            event.y = root.winfo_pointery() - root.winfo_rooty()
            event = App.MouseEventWrapper(event)
            if ((app._lastMousePosn !=  (event.x, event.y)) and
                (event.x >= 0) and (event.x <= app.width) and
                (event.y >= 0) and (event.y <= app.height)):
                if (app._mouse_is_pressed): app.mouse_dragged(event)
                else: app.mouse_moved(event)
                app._lastMousePosn = (event.x, event.y)
                app._redraw_all_wrapper()
        if (mouse_moved_exists or mouse_dragged_exists):
            app._deferred_method_call(afterId='mouse_motion_wrapper', afterDelay=app.mouse_movedDelay, afterFn=app._mouse_motion_wrapper)

    def update_title(app):
        app._title = app._title or type(app).__name__
        app._root.title(f'{app._title} ({app.width} x {app.height})')

    def get_quit_message(app):
        app_label = type(app).__name__
        if (app._title != app_label):
            if (app._title.startswith(app_label)):
                app_label = app._title
            else:
                app_label += f" '{app._title}'"
        return f"*** Closing {app_label}.  Bye! ***\n"

    def _show_root_window(app):
        root = app._root
        root.update(); root.deiconify(); root.lift(); root.focus()

    def _hide_root_window(app):
        root = app._root
        root.withdraw()

    @_safe_method
    def run(app):
        app._mouse_is_pressed = False
        app._lastMousePosn = (-1, -1)
        app._lastWindowDims= None # set in size_changed_wrapper
        app._afterIdMap = dict()
        # create the singleton root window
        if (App._theRoot is None):
            App._theRoot = Tk()
            App._theRoot.createcommand('exit', lambda: '') # when user enters cmd-q, ignore here (handled in key_pressed)
            App._theRoot.protocol('WM_DELETE_WINDOW', lambda: App._theRoot.app.quit()) # when user presses 'x' in title bar
            App._theRoot.bind("<Button-1>", lambda event: App._theRoot.app._mouse_pressed_wrapper(event))
            App._theRoot.bind("<B1-ButtonRelease>", lambda event: App._theRoot.app._mouse_released_wrapper(event))
            App._theRoot.bind("<KeyPress>", lambda event: App._theRoot.app._key_pressed_wrapper(event))
            App._theRoot.bind("<KeyRelease>", lambda event: App._theRoot.app._key_released_wrapper(event))
            App._theRoot.bind("<Configure>", lambda event: App._theRoot.app._size_changed_wrapper(event))
        else:
            App._theRoot.canvas.destroy()
        app._root = root = App._theRoot # singleton root!
        root.app = app
        root.geometry(f'{app.width}x{app.height}+{app.winx}+{app.winy}')
        app.update_title()
        # create the canvas
        root.canvas = app._canvas = WrappedCanvas(app)
        app._canvas.pack(fill=BOTH, expand=YES)
        # initialize, start the timer, and launch the app
        app._running = True
        app._paused = False
        app._ignoredFields = set(app.__dict__.keys()) | {'_ignoredFields'}
        app._app_started_wrapper()
        app._timer_fired_wrapper()
        app._mouse_motion_wrapper()
        app._show_root_window()
        root.mainloop()
        app._hide_root_window()
        app._running = False
        for afterId in app._afterIdMap: app._root.after_cancel(app._afterIdMap[afterId])
        app._afterIdMap.clear() # for safety
        app.app_stopped()
        print(app.get_quit_message())

####################################
# TopLevelApp:
# (with top-level functions not subclassses and methods)
####################################

class TopLevelApp(App):
    _apps = dict() # maps fnPrefix to app

    def __init__(app, fnPrefix:str='', width:int=300, height:int=200, title:str|None=None, **kwargs: Any):
        kwargs['width'] = width
        kwargs['height'] = height
        if (title != None):
            kwargs['title'] = title
        
        if (fnPrefix in TopLevelApp._apps):
            print(f'Quitting previous version of {fnPrefix} TopLevelApp.')
            TopLevelApp._apps[fnPrefix].quit()
        if ((fnPrefix != '') and ('title' not in kwargs)):
            kwargs['title'] = f"INF100 '{fnPrefix}'" # f"TopLevelApp '{fnPrefix}'" 
        elif ('title' not in kwargs):
            kwargs['title'] = "INF100"
        TopLevelApp._apps[fnPrefix] = app
        app._fnPrefix = fnPrefix
        app._callersGlobals = inspect.stack()[1][0].f_globals
        app.mode = None
        super().__init__(**kwargs)

    def _callFn(app, fn, *args):
        isAppStopped = fn == 'app_stopped'
        isUsingMode = (app.mode != None) and (app.mode != '')
        if isUsingMode:
            fn = app.mode + '_' + fn
        fn = app._fnPrefix + fn
        if (fn in app._callersGlobals): app._callersGlobals[fn](*args)
        if (isAppStopped and isUsingMode):
            # call the non-mode app_stopped if there is one
            fn = app._fnPrefix + 'app_stopped'
            if (fn in app._callersGlobals): app._callersGlobals[fn](*args)

    def redraw_all(app, canvas): app._callFn('redraw_all', app, canvas)
    def app_started(app): app._callFn('app_started', app)
    def app_stopped(app): app._callFn('app_stopped', app)
    def key_pressed(app, event): app._callFn('key_pressed', app, event)
    def key_released(app, event): app._callFn('key_released', app, event)
    def mouse_pressed(app, event): app._callFn('mouse_pressed', app, event)
    def mouse_released(app, event): app._callFn('mouse_released', app, event)
    def mouse_moved(app, event): app._callFn('mouse_moved', app, event)
    def mouse_dragged(app, event): app._callFn('mouse_dragged', app, event)
    def timer_fired(app): app._callFn('timer_fired', app)
    def size_changed(app): app._callFn('size_changed', app)


####################################
# run_app()
####################################

run_app = TopLevelApp

print(f'Loaded uib_inf100_graphics version {App.version} (last updated {App.last_updated})')
