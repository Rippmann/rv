import rhinoscriptsyntax as rs

class RVsettings(object):
    
    name        = "RhinoVault"
    version     = "2.0.0.1" 
    f_precision = '3f'

class RVinfo(object):
    
    messages = {
    'e_plugin'  : "Plugin not or incorrectly installed. Check installation instructions.",
    'e_object'  : "No object selected.",
    'e_objects' : "No or not sufficient objects selected.",
    'e_closed'  : "Set of curves must enclose spaces. No single-end curves allowed.",
    'e_discon'  : "Set of curves must define only one connected mesh.",
    'i_init'    : "Internal attempt to re-initiate plugin."    
    }
    @staticmethod
    def message(key=None):
        if not key in RVinfo.messages: return None
        return RVinfo.messages[key]
    
    @staticmethod
    def message_box(key=None,buttons=0):
        
        settings = RVsettings()
        title = settings.name + " " + settings.version
        
        if not key in RVinfo.messages: return None
        return rs.MessageBox(RVinfo.messages[key], buttons, title)
        # |              following flags. If omitted, an OK button and no icon is displayed
        # |              0      Display OK button only.
        # |              1      Display OK and Cancel buttons.
        # |              2      Display Abort, Retry, and Ignore buttons.
        # |              3      Display Yes, No, and Cancel buttons.
        # |              4      Display Yes and No buttons.
        # |              5      Display Retry and Cancel buttons.
        # |              16     Display Critical Message icon.
        # |              32     Display Warning Query icon.
        # |              48     Display Warning Message icon.
        # |              64     Display Information Message icon.
        #-----------------------------------------------------------------------
        # |            A number indicating which button was clicked:
        # |              1      OK button was clicked.
        # |              2      Cancel button was clicked.
        # |              3      Abort button was clicked.
        # |              4      Retry button was clicked.
        # |              5      Ignore button was clicked.
        # |              6      Yes button was clicked.
        # |              7      No button was clicked.


verbose = False
if verbose:
    def verboseprint(*args):
        # Print each argument separately so caller doesn't need to
        # stuff everything to be printed into a single string
        for arg in args:
           print arg,
        print
else:   
    verboseprint = lambda *a: None      # do-nothing function
    
    
def delete_alias():
    names = rs.AliasNames()
    print names
    del_all = True
    for name in names:
        if 'Rv' in name or del_all:
            rs.DeleteAlias(name)

if __name__ == '__main__':
    delete_alias()



