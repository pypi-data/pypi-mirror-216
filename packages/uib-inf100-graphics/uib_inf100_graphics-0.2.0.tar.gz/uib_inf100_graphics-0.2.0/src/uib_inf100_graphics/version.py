# version.py
import datetime

__version__ = "0.2.0"
__last_updated__ = datetime.date(year=2023, month=6, day=27)

# Version 0.2.0
#  * Added types for run_app -method (constructor of TopLevelApp) and types
#    App, MouseEvent and KeyEvent that may be helpful for users who want to
#    use type hints in their own code

# Version 0.1.0
#  * Changed to snake_case style


# A fork of cmu_112_graphics.py version 0.9.2
# Used with permission from the CMU 112 graphics package developers
# Adapted for INF100 at the University of Bergen for fall 2022


# Version history for cmu_112_graphics.py


# Pending changes:
#   * Fix Windows-only bug: Position popup dialog box over app window (already works fine on Macs)
#   * Add documentation
#   * integrate sounds (probably from pyGame)
#   * Improved methodIsOverridden to TopLevelApp and ModalApp
#   * Save to animated gif and/or mp4 (with audio capture?)

# Deferred changes:
#   * replace/augment tkinter canvas with PIL/Pillow imageDraw (perhaps with our own fn names)


# Changes in v0.9.2
#  * added event.ctrl, event.alt, event.shift

# Changes in v0.9.1
#  * If we are in a mode when we call app_stopped, then also call the non-modal app_stopped

# Changes in v0.9.0
#  * added simpler top-level modes implementation that does not include mode objects
#  * added ImageDraw and ImageFont to PIL imports

# Changes in v0.8.8
#   * added __repr__ methods so:
#     * print(event) works and prints event.key or event.x + event.y
#     * print(app) works and prints just the user defined app fields

# Changes in v0.8.7
#   * removed modes (for now)

# Changes in v0.8.6
#   * f21

# Changes in v0.8.5
#   * Support load_image from Modes

# Changes in v0.8.3 + v0.8.4
#   * Use default empty Mode if none is provided
#   * Add KeyRelease event binding
#   * Drop user32.SetProcessDPIAware (caused window to be really tiny on some Windows machines)

# Changes in v0.8.1 + v0.8.2
#   * print version number and last-updated date on load
#   * restrict modifiers to just control key (was confusing with NumLock, etc)
#   * replace hasModifiers with 'control-' prefix, as in 'control-A'
#   * replace app._paused with app.paused, etc (use app._ for private variables)
#   * use improved ImageGrabber import for linux

# Changes in v0.8.0
#   * suppress more modifier keys (Super_L, Super_R, ...)
#   * raise exception on event.keysym or event.char + works with key = 'Enter'
#   * remove tryToInstall

# Changes in v0.7.4
#   * renamed drawAll back to redraw_all :-)

# Changes in v0.7.3
#   * Ignore mousepress-drag-release and defer configure events for drags in titlebar
#   * Extend deferred_redraw_all to 100ms with replace=True and do not draw while deferred
#     (together these hopefully fix Windows-only bug: file dialog makes window not moveable)
#   * changed size_changed to not take event (use app.width and app.height)

# Changes in v0.7.2
#   * Singleton App._theRoot instance (hopefully fixes all those pesky Tkinter errors-on-exit)
#   * Use user32.SetProcessDPIAware to get resolution of screen grabs right on Windows-only (fine on Macs)
#   * Replaces show_graphics() with run_app(...), which is a veneer for App(...) [more intuitive for pre-OOP part of course]
#   * Fixes/updates images:
#       * disallows loading images in redraw_all (raises exception)
#       * eliminates cache from load_image
#       * eliminates app.getTkinterImage, so user now directly calls ImageTk.PhotoImage(image))
#       * also create_image allows magic pil_image=image instead of image=ImageTk.PhotoImage(app.image)

# Changes in v0.7.1
#   * Added keyboard shortcut:
#       * cmd/ctrl/alt-x: hard exit (uses os._exit() to exit shell without tkinter error messages)
#   * Fixed bug: shortcut keys stopped working after an MVC violation (or other exception)
#   * In app.save_snapshot(), add .png to path if missing
#   * Added: Print scripts to copy-paste into shell to install missing modules (more automated approaches proved too brittle)

# Changes in v0.7
#   * Added some image handling (requires PIL (retained) and pyscreenshot (later removed):
#       * app.load_image()       # loads PIL/Pillow image from file, with file dialog, or from URL (http or https)
#       * app.scale_image()      # scales a PIL/Pillow image
#       * app.getTkinterImage() # converts PIL/Pillow image to Tkinter PhotoImage for use in create_image(...)
#       * app.get_snapshot()     # get a snapshot of the canvas as a PIL/Pillow image
#       * app.save_snapshot()    # get and save a snapshot
#   * Added app._paused, app.togglePaused(), and paused highlighting (red outline around canvas when paused)
#   * Added keyboard shortcuts:
#       * cmd/ctrl/alt-s: save a snapshot
#       * cmd/ctrl/alt-p: pause/unpause
#       * cmd/ctrl/alt-q: quit

# Changes in v0.6:
#   * Added fnPrefix option to TopLevelApp (so multiple TopLevelApp's can be in one file)
#   * Added show_graphics(drawFn) (for graphics-only drawings before we introduce animations)

# Changes in v0.5:
#   * Added:
#       * app.winx and app.winy (and add winx,winy parameters to app.__init__, and sets these on configure events)
#       * app.set_size(width, height)
#       * app.set_position(x, y)
#       * app.quit()
#       * app.show_message(message)
#       * app.get_user_input(prompt)
#       * App.last_updated (instance of datetime.date)
#   * Show popup dialog box on all exceptions (not just for MVC violations)
#   * Draw (in canvas) "Exception!  App Stopped! (See console for details)" for any exception
#   * Replace callUserMethod() with more-general @_safe_method decorator (also handles exceptions outside user methods)
#   * Only include lines from user's code (and not our framework nor tkinter) in stack traces
#   * Require Python version (3.6 or greater)

# Changes in v0.4:
#   * Added __setattr__ to enforce Type 1A MVC Violations (setting app.x in redraw_all) with better stack trace
#   * Added app._deferred_redraw_all() (avoids resizing drawing/crashing bug on some platforms)
#   * Added deferred_method_call() and app._afterIdMap to generalize afterId handling
#   * Use (_ is None) instead of (_ == None)

# Changes in v0.3:
#   * Fixed "event not defined" bug in size_changed handlers.
#   * draw "MVC Violation" on Type 2 violation (calling draw methods outside redraw_all)

# Changes in v0.2:
#   * Handles another MVC violation (now detects drawing on canvas outside of redraw_all)
#   * App stops running when an exception occurs (in user code) (stops cascading errors)

# Changes in v0.1:
#   * OOPy + supports inheritance + supports multiple apps in one file + etc
#        * uses import instead of copy-paste-edit starter code + no "do not edit code below here!"
#        * no longer uses Struct (which was non-Pythonic and a confusing way to sort-of use OOP)
#   * Includes an early version of MVC violation handling (detects model changes in redraw_all)
#   * added events:
#       * app_started (no init-vs-__init__ confusion)
#       * app_stopped (for cleanup)
#       * key_released (well, sort of works) + mouse_released
#       * mouse_moved + mouse_dragged
#       * size_changed (when resizing window)
#   * improved key names (just use event.key instead of event.char and/or event.keysym + use names for 'Enter', 'Escape', ...)
#   * improved function names (renamed redraw_all to drawAll)
#   * improved (if not perfect) exiting without that irksome Tkinter error/bug
#   * app has a title in the titlebar (also shows window's dimensions)
#   * supports Modes and ModalApp (see ModalApp and Mode, and also see TestModalApp example)
#   * supports TopLevelApp (using top-level functions instead of subclasses and methods)
#   * supports version checking with App.major_version, App.minor_version, and App.version
#   * logs drawing calls to support autograding views (still must write that autograder, but this is a very helpful first step)

