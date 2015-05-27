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
    def __init__(self, cpath = u"conf", config = u"settings.conf", debug = False, max_filesize = 1048576):
        self.file = path.abspath(path.join(cpath, config))
        self.count = 0
        self.max_filesize = max_filesize
        self.debug = debug

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
            raise IOError(u"Configuration file is too big!")
        content = conf_file.read(self.max_filesize) # just in case
        self.loads(content)

    ##
    # Loads settings from a string instead of the file directly. This helps
    # with the unit testing
    #
    # @param content: configuration file contents
    def loads(self, content):
        for line in content.split('\n'):
            # finds the first occurance of "=" and splits the line to key, value
            if line.find("=")>0:
                key, value = line.split("=", 1) 
            else:
                key = line
            key = key.strip(" \t")
            # ignores blank lines
            if len(key)>0:
                if key.isalnum():
                    value = value.strip("\t ")
                    # inserts the key value pair into the dictionary if value exists
                    if len(value)>0:
                        self.__setitem__(key, self.load_value(value))
                    else:
                        self.__setitem__(key, None)
                elif key[0]!='#':
                    # this means the key is not valid and not a comment either
                    raise KeyError(u"Invaild key in {0} at line {1}".format(self.file, self.count))

    def update_settings(self):
        with open(self.file,'w') as fi:
            output = u""
            for k,v in self.items():
                output += u"{0} = {1}\n".format(k, repr(v).replace('\\\\', '\\'))
            fi.write(output)
            fi.flush()
        print("Settings file updated")
        
    ##
    # Try to load a value, in case there is an error in the format
    # it raises ValueError
    def load_value(self,val):
        value = None
        self.count += 1 
        #checks if the value is a number
        if val[0].isdigit() or val[0]=='-':
            value = self.load_numeric(val)
        elif val[0]=='"' or val[0]=="'": # is string value
            value = self.load_string(val)
        return value
    
    ##
    # Validates an loads a string
    #
    # @param string: the potencial string
    # @param i: index in the string, if i is 0 or positive the function
    #   checks partialy the line and extracts the first valid string otherwise
    #   it checks the whole line and raises an ValueError in case of malformed string
    # @returns if i>=0 then returns the first valid string and the end index
    #   otherwise it returns just a string
    def load_string(self, string, i=-1):
        is_valid = False
        escaped = False
        value = u""
        # checks the whole line
        if(i<0):
            start = string[0]
            i = 1
            while(i<len(string)):
                if string[i]==start and not escaped:
                    break
                elif string[i]=='\'':
                    escaped = True
                elif escaped ==True:
                    escaped = False
                    value += string[i]
                else:
                    value += string[i]
                i += 1
        return value

    ##
    # Loads an numberic value (int | float) or raises ValueError
    #
    # @param num: a string with the numeric value
    # @returns an int or a float value
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
                if self.debug:
                    sys.stderr.write(u"Cannot parse number in {0} at line {1}".format(self.file, self.count))
                raise ValueError(u'ValueError in {0} at line {1}'.format(self.file, self.count))
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
            
        
        
