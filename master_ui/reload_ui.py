from master_ui.helperWidgets import reload_helper_widgets
from master_ui.workFile import reload_work_file
from master_ui import actionUi
from master_ui import sessionUi
from master_ui import fileActionUi
from master_ui import loadPluginActionUi
from master_ui import openFileActionUi
from master_ui import runSystemActionUi
from master_ui import runPyActionUi
from master_ui import runPyFileActionUi



modules = [reload_helper_widgets, reload_work_file, actionUi,
            sessionUi, fileActionUi, loadPluginActionUi,
            openFileActionUi]

reload_it_modules = [reload_helper_widgets, reload_work_file]
def reload_it():
    print "------> Sarted reload of ui"
    for sub_module in modules:
        reload(sub_module)
        print "---> Reloading : " +str(sub_module.__name__)

    for sub_module in reload_it_modules:
        sub_module.reload_it()

    print "------> Ended reload of ui"
