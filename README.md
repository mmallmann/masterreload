masterreload
============

dev tool for speed up dev cycle in Maya

Hi everyone. this is a tool I wrote out of frustration for the repetitive actions needed
in order to develop in Maya.
For example when you develop a C++ plug-in, you need to kill and re-open Maya 
when you recompile a new version, load the plugin/plugins and setup the scene 
over and over.
That's why I decided to write this tool to speed up the process.

![Alt UI](/doc/resources/ui_screen.png)

Here you can see how you can open the ui (PYTHON):

```python
import reload_master
from master_ui import sessionUi
reload(reload_master)
reload_master.reload_it()
s = sessionUi.SessionUi()
s.show()
```

Here instead you can kick the default session (PYTHON):

```python
import reload_master
from master_ui import sessionUi
reload(reload_master)
reload_master.reload_it()
sessionUi.run_default()
```

This two are actually the two script I use all the time, I attached them to two hotkeys:

ctrl + alt + w  = show window
ctrl + alt + q  = kick default session

if you want to know more about the tool here is a demo (right click on the image -> open in new tab:

[![IMAGE DEMO](/doc/resources/reloadMasterThumb.png)](https://vimeo.com/107648350)