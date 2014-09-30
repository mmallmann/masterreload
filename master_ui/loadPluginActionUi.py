"""
This module holds a load plugin action ui
"""

from master_ui import fileActionUi

class LoadPluginActionUi(fileActionUi.FileActionUi):
    """
    @brief Ui for the load plugin action
    """
    def __init__(self, session_instance, internal_action, session_ui, parent=None ):
        """
        This is the constructor
        @param session_instance: this is the session we want to display the data of
        @param internal_action: this is the acton class we want to work on with this
                                UI
        @param session_ui: this is is the instance of the sessionUi class
        @param parent: this is the parent widget holding the sub_ui
        """
        fileActionUi.FileActionUi.__init__(self, session_instance, internal_action, session_ui, parent)

        #Setupping the pathWidget
        self.pathWidget.set_label_text("plugin path:")
        self.pathWidget.file_extension = "*.mll *.so"

def get_ui(session_instance, internal_action, session_ui, parent):
    """
    This is a generic method that returns an istance 
    of the Ui in this module

    @param session_instance: this is the session we want to display the data of
    @param internal_action: this is the acton class we want to work on with this
                            UI
    @param session_ui: this is is the instance of the sessionUi class
    @param parent: this is the parent widget holding the sub_ui
    @return instance
    """
    return LoadPluginActionUi(session_instance, internal_action, session_ui, parent)