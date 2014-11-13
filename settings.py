import os
'''This class Parses a settings file with extra customization needed for the system or in the future from the 
   extensions that might be developed. 
   We do not use compile(exec(file.py)) because this could have unwilling consequences'''


class SettingsObj(object):
    '''The class from which the Settings values are retrieved as a dictionary Key'''
    
    # def __init__(self, app=None):
        # self.app = app
        # if app is not None:
            # self.init_app(app)
            
    def __init__(self,name):
        self.__name__ = name
        self.settings = Settings()
        
    def __get__(self, obj):
        if obj is None:
            return self
        rv = obj.settings[self.__name__]
        return rv
    
    def __set__(self, obj, value):
        obj.settings[self.__name__] = value
      


class Settings(dict):
    #file = "conf%ssettings.py" % (os.sep)
    def __init__(self):
        self.file = "conf%ssettings.set" % (os.sep,)
        self.init_timestamp = self.get_time()
        self.count = 0


    def parse(self):
        if self.init_timestamp != self.get_time():
            print ("Timestamp is different updating time....")
            self.init_timestamp = self.get_time()
        self.load_settings()
        


    def get_time(self):
        return os.path.getctime(self.file)
        
    def load_settings(self):
        #f = open(self.file,'r')
        #f.seek(0)
        with open(self.file,'r') as fil:
                for f in fil:
                    key, value = f.split("=",1)
                    key = key.strip()
                    self.__setitem__(key, self.load_value(value))
        print("Total recursives = %d" % self.count)
        
    def update_settings(self):
        d = {'1':True,'0':False,'t':True}
        with open(self.file,'w') as fi:
            for k,v in self.items():
                vl = "{0} = {1}{2}{1}\n"
                if self.is_numeric(v):
                    try:
                       v = (d[self.is_numeric(v,'n')])
                    except KeyError:
                        pass
                        
                    vl = vl.format(k,"",v)
                else:
                    vl = vl.format(k,"'",v)
                fi.write(vl)
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
                        escaped = not escaped
                    elif escaped == False:
                        ec = c
                        escaped = not escaped        
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
        else:
            rvalue = value
        return rvalue
        
            
    def is_numeric(self,num,type='bool'):
        '''If type is something different than bool then it returns the
            value converted otherwise it returns true false'''
        rv = False
        y = False
        try:
            rv = round(float(num),3)
            y = True
        except (ValueError, TypeError):
                rv = y = False
        if type == 'bool':
            rv = y
        return rv
        
    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))
            
        
        
