import pandas as pd
def input_method(f): #input decorator used to deal with file and text
    def wrapper(self,source,*args):
        try:
            return f(self,pd.read_csv(source),*args)# try if args can read as 
        except ValueError:
            return f(self,source,*args) # then return as normal string

    wrapper.__isinput__ = True # set a secret isinput attr
    return wrapper

def output_method(f): # output decorator used to deal with overloading and typing
    f.__isoutput__ = True # set a secret isoutput attr
    type_anno = [t.__name__ if not(isinstance(t,str)) else t for t in f.__annotations__.values()] #get type annotations
    if type_anno:# prevent no type annotations function
        f.__signatures__ = type_anno # set another secret signatures attr
        return f
    raise ValueError('Please Provide A Function With Type Annotation(s)')

class Overload():
    def __init__(self,overload_list):
        self.overload_list = overload_list #get the list
        self.signatures = [f.__signatures__ for f in overload_list] # get the type anno for all func

    def __call__(self,*args):
        all_param = []
        for arg in args: # get all params type when function is called
            all_param.append(type(arg).__name__)

        if all_param in self.signatures: # matching
            best_match_func = self.overload_list[self.signatures.index(all_param)](self,*args) 
            return best_match_func
        
        raise TypeError(str('No Output function with ('+' ,'.join(all_param)+') types')) # no matching function

class OverloadList(list):# list for overload dict incase of someone try to store a list as dictionary value
    pass

class OverloadDict(dict): 
    def __setitem__(self, key,value):
        assert isinstance(key,str),'keys must be a str' #check if key is a string
        
        new = self.get(key,True)# check if key is seen in dict
        overloaded = getattr(value,'__isoutput__',False) # check if value is overloaded

        if new is True:
            insert_value = OverloadList([value]) if overloaded else value # setvalues if new and overloaded
            super().__setitem__(key,insert_value)
        elif isinstance(new,OverloadList):#if existed
            new.append(value)
        else:#normal things
            super().__setitem__(key,value)

class NLPMeta(type):
    '''
    This is GODMeta Class and there is something you need to do
        - First create ONLY ONE function with decorator inp
        - Second create ONE OR MORE function using overload decorator
    '''
    def __call__(cls,*args): #check for input and output methods
        __input_method = []
        __output_method = []
        for key,val in vars(cls).items():# get all functions
            if getattr(val,'__isinput__',False):# check isinput attr
                __input_method.append(key)
                
            if getattr(val,'overload_list',False): # check isoutput attr
                __output_method = val.overload_list

        if len(__input_method) != 1:
            raise TypeError("You need to put only one input method")

        if len(__output_method) < 1:
            raise TypeError("You need at least one output method")
        
        return super().__call__(*args)

    @classmethod
    def __prepare__(mcs,name,bases):# class that return dict to set attr
        return OverloadDict()

    def __new__(mcs, name, bases, namespace, **kwargs):#filter and create the class
        overload_namespace = {
            key: Overload(val) if isinstance(val, OverloadList) else val
            for key, val in namespace.items()
        }
        return super().__new__(mcs, name, bases, overload_namespace, **kwargs)
                               
class NLPBase(metaclass = NLPMeta):#for inherit
    pass