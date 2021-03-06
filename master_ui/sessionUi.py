"""
This class holds the basic ui class for a session ui
"""
import os
import imp
from os.path import expanduser


from PySide import QtCore, QtGui

import workFile.masterReload_rc
import session
from master_ui.workFile import session_form
from master_ui import actionUi
import env_config

class SessionUi(QtGui.QMainWindow, session_form.Ui_session_form):
    """
    @brief Ui class for displaying/editing Sessions
    This is the class in charge to display a Session class and 
    to inject the input data dirctly in the class itself
    """

    ##private constant of the folders to exclude in the parse
    __FOLDERS_TO_EXCLUDE = ["workFile"]
    ##private constant of the files to exclude
    __FILES_TO_EXCLUDE = []
    ##The tag used to identify a new session
    NEW_SESSION_TAG = "new session"

    def __init__(self, parent=None):
        """
        This is the constructor 
        @param parent: QWidget, the parent of the UI if provided
        """
        QtGui.QMainWindow.__init__(self,parent)
        #ui build from designer
        self.setupUi(self)
        #my own ui build 
        self.customizeUi()

    def customizeUi(self):
        """
        This function is automatically called at init time,
        it is going to add all the missing bits that are not 
        possible to add in the designer
        """
        ##the stileSheet file
        self.ssh_file= str(__file__).rsplit(os.path.sep,1)[0]+ \
                            "/resources/darkorange.stylesheet"
        with open(self.ssh_file,"r") as fh:
            self.setStyleSheet(fh.read())

        ##this attribute holds the instance of the currently 
        ##displayed session
        self.currentSession = session.ActionSession()
        ##this attribute holds the Actions added to the session
        self.actions = []
        ##this private list holds the list of the available 
        ##action guis to be instanciated
        self.__available_actions_uis = []
        ##this private dict holds a dict that maps the module
        ##name to its full path on disk
        self.__uis_dict = {}
        ##this private list holds all the stored sessions
        self.__available_sessions = []
        ##QSetting used for the tool
        self.__settings = QtCore.QSettings("reloadMaster", "MG_dev")
        
        #forcing the private variables to populate
        self.__get_available_actions_uis()
        self.__get_available_sessions()

        #laoding the data in the session then in the ui
        self.load_actions()
        self.load_ui_sessions()

        ##list holding all the loaded UIs
        self.action_uis = []

        ##Item used to squeze the sessionsUis up
        self.__spacer_item = None

        #now that all is in place we load the current session
        self.load_current_session()

        #adding needed signals
        self.addPB.clicked.connect(self.add_action)
        self.savePB.clicked.connect(self.save_session)
        self.sessionsCB.currentIndexChanged.connect(self.load_current_session)
        self.executePB.clicked.connect(self.execute)
        self.setDefaultPB.clicked.connect(self.set_current_as_default)
        self.actionSession_Path.triggered.connect(self.set_session_path)

    def set_session_path(self):
        """
        This fucntion is used to store the session 
        path in the settings
        """
        path  = QtGui.QFileDialog.getExistingDirectory(None,
        "Pick session folder", get_sessionPath())

        self.__settings.setValue("sessionPath",path)
        print "Path corretly stored:", path

    @property
    def available_action_uis(self):
        """
        This is the getter function for the attribute
        available_actions, this attribute holds all the possible
        actions that the user can instanciate
        """
        self.__available_actions_uis = []
        return self.__get_available_actions_uis()



    def __get_available_actions_uis(self):
        """
        This function returns a list of all availble actions
        """
        self.__check_path(env_config.UI_PATH)
        return self.__available_actions_uis

    @property
    def available_sessions(self):
        """
        This is the getter function for the attribute
        available_actions, this attribute holds all the possible
        actions that the user can instanciate
        """
        self.__available_sessions = []
        self.__get_available_sessions()
        return self.__available_sessions

    def __get_available_sessions(self):
        """
        This function returns a list of all availble actions
        """
        results = os.listdir(get_sessionPath())

        self.__available_sessions = [subRes for subRes in results if subRes.find(".session") != -1]
        self.__available_sessions.insert(0,self.NEW_SESSION_TAG)
    def __check_path(self, path):
        """
        This procedure checks a path for the py files and kicks the recursions
        """

        res = os.listdir(path)
        to_return = []
        for sub_res in res:
            if sub_res not in self.__FOLDERS_TO_EXCLUDE and \
            os.path.isdir(path + sub_res) == 1:
                self.__check_path(path  + sub_res + "/")


            if sub_res.find("ActionUi.py") != -1 and sub_res.find(".pyc") == -1 \
            and sub_res not in self.__FILES_TO_EXCLUDE:
                if sub_res.find("reload") == -1:
                    to_return.append(sub_res)
                    self.__uis_dict[sub_res] = path +"/" + sub_res
        self.__available_actions_uis += to_return


    def load_actions(self):
        """
        This function loads the available actions in the ui
        """
        self.actions = self.currentSession.available_actions
        self.actionsCB.clear()
        self.actionsCB.addItems(self.actions)

    def load_ui_sessions(self):
        """
        This function loads the available sessions in the ui
        """
        
        self.sessionsCB.clear()
        self.sessionsCB.addItems(self.available_sessions)
        self.set_current_session_ui()


    def load_current_session(self):
        """
        This procedure load the available session in the ui
        """

        current = str(self.sessionsCB.currentText())
        if current == "":
            return
        self.currentSession = session.ActionSession()
        if current != self.NEW_SESSION_TAG:
            self.currentSession.load(get_sessionPath() \
                + "/" + current)

        self.update_ui()  
        

    def add_action(self, action_name = None):
        """
        This function adds an action to the current session
        """

        if action_name:
            currAction = action_name
        else:
            currAction = str(self.actionsCB.currentText ())

        self.currentSession.add_action_from_str(currAction)

        self.update_ui()


    def update_ui(self):
        """
        This fucntion refreshes the ui with the 
        latest data
        """
        #removing all the widgets
        for subUi in self.action_uis :
            self.remove_widget(subUi)

        #cleaning old classes and remove spacer
        self.action_uis = []
        self.__remove_spacer()

        for sub_action in self.currentSession.actions :
    
            ui_name = sub_action.__class__.__name__ + "Ui"
            my_ui = self.__get_nstance_from_str(ui_name, sub_action)[0]

            # aui = actionUi.ActionUi(self.currentSession, sub_action, self)
            self.verticalLayout_5.addWidget(my_ui)
            self.action_uis.append(my_ui)
            my_ui.load()

        self.__add_spacer()

    def remove_widget(self, widget):
        """
        This functon is called from the widget itself 
        for removing iteself
        """
        #removing the widget from the layout, i should probably
        #rename that layout to something more meaningful
        self.verticalLayout_5.removeWidget(widget)
        widget.deleteLater()
        widget = None
        self.update()

    def __get_ui_from_string(self, ui_name):
        """
        This procedure makes an istance of a module from its name
        @param moduleName: str ,the name of the module
        @return: module instance
        """
        my_ui = self.__uis_dict[self.__fix_ui_name(ui_name)]
        my_ui = imp.load_source(self.__fix_ui_name(ui_name, 0), \
                    my_ui)
        return my_ui

    def __fix_ui_name(self, ui_name, add_extension=1):
        """
        This procedure converts the given module name in a way that is suitable
        for the instancing
        @param moduleName: str ,the name of the module
        @param addExtension: bool , whether or not to add the ".py" at the end
        @return: str
        """

        val = ui_name[0].lower() + ui_name[1:]
        if add_extension == 1:
            val += ".py"

        return val

    def __get_nstance_from_str(self, ui_name, action):
        """
        This procedure returns a class instance from the given string
        @param moduleName: str ,the name of the module
        """
        my_ui = self.__get_ui_from_string(ui_name)
        my_ui_instance = my_ui.get_ui(self.currentSession, action, self, None)
        return my_ui_instance, my_ui


    def __add_spacer(self):
        """
        This function add a spacer after all the sub_uis
        """
        self.__spacer_item = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(self.__spacer_item)

    def __remove_spacer(self):
        """
        This function removes the spacer from 
        the sessionUi
        """
        if self.__spacer_item:
            self.verticalLayout_5.removeItem(self.__spacer_item)
            del(self.__spacer_item)
            self.__spacer_item = None
            self.update()

    def __transfer_data(self):
        """
        This function copies all the data 
        from the UI to the session
        """
        for sub_ui in self.action_uis:
            sub_ui.save()

    def save_session(self):
        """
        This function saves the current
        session on disk
        """
        self.__transfer_data()
        current = str(self.sessionsCB.currentText())
        if current == self.NEW_SESSION_TAG :
            current = self.currentSession.save(None )
        else:
            self.currentSession.save(get_sessionPath() + "/" +current)

        self.__settings.setValue("current_session", current)
        self.load_ui_sessions()
        self.update()


    def execute(self):
        """
        This function execute the currenct session
        """
        self.currentSession.execute()

    def get_current_session_ui(self):
        """
        This function loads the current session 
        uis
        """
        return self.__settings.value("current_session", self.NEW_SESSION_TAG)
        

    def set_current_session_ui(self):
        """
        This function sets the combobox to the correct
        index pointing to the current session if exists
        """
        toSet = self.get_current_session_ui()
        for i in range(self.sessionsCB.count()):
            if str(self.sessionsCB.itemText(i)) == toSet:
                self.sessionsCB.setCurrentIndex(i)
                self.update()
                return

    def set_current_as_default(self):
        """
        This function sets the current sessions
        as defult
        """
        toSet = str(self.sessionsCB.currentText())
        self.__settings.setValue("current_session", toSet)


    def swap_action(self, action, direction="down"):
        """
        This function is used to move an action up and down
        the list, if reaches the start or end it loops it
        @param action: action instance, the action to move up or down
        @param direction: str, the direction to push the action to,
                        accepted values are up and down
        """
        self.currentSession.swap_action(action, direction)
        self.update_ui()
def run_default():
    """
    This function runs the default action
    """
    settings = QtCore.QSettings("reloadMaster", "MG_dev")
    value = settings.value("current_session", SessionUi.NEW_SESSION_TAG)
    current = session.ActionSession()


    path = get_sessionPath() + "/" + value
    if os.path.isfile(path) == 1 :
        current.load(path)
        current.execute()

def get_sessionPath():
    """
    This function returns the the path to the session folder
    @return str
    """
    settings = QtCore.QSettings("reloadMaster", "MG_dev")
    sessionPath = settings.value("sessionPath",expanduser("~"))
    return sessionPath
