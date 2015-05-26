import sys
from os import path

class Settings(dict):
    "Reads a simple configuration file and stores the values in a dict like style."

    ##
    # objects initialize method
    #
    # @param cpath: path to configuration file (default "conf")
    # @param config: configuration file name (default "settings.cfg")
    # @param debug: toggles debugging on or  off (default False)
    # @param max_filesize: max configs file size (defualt 1mb)
    def __init__(self, cpath = u"conf", config = u"settings.cfg", debug = False, max_filesize = 1048576):
        self.file = path.abspath(path.join(cpath, config))
        self.init_timestamp = self.get_time()
        self.count = 0
        self.max_filesize = max_filesize

    ##
    # Parses the config in case it changed
    def parse(self):
        if self.init_timestamp != self.get_time():
            if debug:
                print ("Timestamp is different updating time....")
            self.init_timestamp = self.get_time()
            self.load_settings()

    ##
    # Returns the configs modification time
    #
    # @returns time in epoch format
    def get_time(self):
        # returns the files modification time
        return path.getmtime(self.file)
        
    def load_settings(self):
        conf_file = open(self.file,'r')
        # aborts reading in case the config file is larger than the maximum file size
        if self.max_filesize < path.getsize(self.file):
            raise IOError("Configuration file is too big!")
        content = conf_file.read(self.max_filesize) # just in case
        self.loads(content)

    ##
    # Loads settings from a string instead of the file directly. This helps
    # with the unit testing
    #
    # @param content: configuration file contents
    def loads(self, content):
        pass

    def update_settings(self):
        with open(self.file,'w') as fi:
            output = u""
            for k,v in self.items():
                output += u"{0} = {1}\n".format(k, repr(v).replace('\\\\', '\\'))
            fi.write(output)
            fi.flush()
        print("Settings file updated")
        

    def load_value(self,value):
        self.count+=1
        value = value.strip()
        rvalue = None
        if value[0]=='"' or value[0] == "'":
            rvalue = value.strip("'\"")
        elif self.is_numeric(value):
            print (value)
            rvalue = self.is_numeric(value,'num')
        elif value[0] =='[' or value[0] == '(':
            #value = value.strip("([])")
            value = value[1:-1]
            #value = value.split(',')
            escaped = False
            ec = ""
            l = []
            temp = ""
            i=0
            e_chars = {"'":"'", '"':'"', '[':']', "(":")", '{':'}'}
            while i<len(value):
                c = value[i]
                if c in e_chars or c in e_chars.values():
                    #escaped = not escaped
                    if escaped == True and e_chars[ec] == c:
                        ec = ""
                        escaped = False
                    elif escaped == False:
                        ec = c
                        escaped = True        
                if escaped == False:
                    if c == "," or i+1>=len(value):
                        if c == ",":
                            c = ""
                        temp += c
                        l.append(temp)
                        temp = ""
                else:
                    temp += c
                i+=1
            rvalue  = []
            for v in l:
                rvalue.append(self.load_value(v))
        elif value=="True" or value=="False":
            if value=="True":
                value = True
            else:
                value = False
            rvalue = value
        else:
            sys.stderr.write("Unrecognized value type: {0}\n".format(value));
        return rvalue
        
            
    def load_numeric(self,num):
        '''Converts the string value to int or float depending on the type.
        If the value is not a valid number then returns None and prints an error message.'''
        number = None
        try:
            number = int(num)
        except ValueError:
            try:
                number = float(num)
            except ValueError:
                sys.stderr.write("The {0} is not a valid number.\n".format(num))  
        return number
        
       
    def matcher(value,pattern='key_value'):
        import re
        patterns = {
            'key_value':'((?:[a-z][a-z0-9_]*)\s*?(=)\s*?.*)$','advance_key':'',
            'custom':''}
        if type(value) is list or type(value) is dict:
            pass
        return re.match('<.*?>', value).group()
        
    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))
            
        
        
