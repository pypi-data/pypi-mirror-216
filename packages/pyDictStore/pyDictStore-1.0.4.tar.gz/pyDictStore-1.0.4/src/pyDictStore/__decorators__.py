from .__events__ import PropertyChangedEvent
#from functools import wraps
import functools


def storage(cls):
    @functools.wraps(cls, updated=())
    class storage_wrap(cls):
        def __init__(self, *args, **kwargs) -> None:
            self.__wrapper__ = cls
            self.__storage__ = {}
            #oCls = super(type(self.__wrapper__),self.__wrapper__).__new__(self.__wrapper__)
            #oCls.__storage__ = {}
            self.PropertyChanged = PropertyChangedEvent()
            #Add storageSet and default(none) to properties if not already present
            for name in [p for p in dir(self.__wrapper__) if isinstance(getattr(self.__wrapper__,p),property)]:
                prop = getattr(self.__wrapper__,name)
                fget = (prop.fget 
                        if prop.fget.__qualname__ == 'default.__call__.<locals>.__wrapper__'
                        else default(None)(prop.fget)
                        )
                fset = (prop.fset 
                        if isinstance(prop.fset,storageSetter)
                        else storageSetter(prop.fset)
                        )
                setattr(self.__wrapper__, name, property(fget, fset, prop.fdel))
            #Call Wrapped Class' initilizer
            super().__init__(*args,**kwargs)
    return storage_wrap

class default:
    def __init__(self, value=None) -> None:
        self.value = value

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            obj = args[0]
            v = self.value
            if hasattr(obj,'__storage__'): 
                strg = getattr(obj, '__storage__')
                if not function.__name__ in strg:
                    strg[function.__name__] = self.value
                v = strg[function.__name__]
            vOverride = function(*args, **kwargs)
            return v if vOverride is None else vOverride
        return wrapper

class storageSetter:
    def __init__(self, function) -> None:
        self.function = function

    def __call__(self, *args, **kwargs):
        obj = args[0]
        value = args[1]
        oValue = self.function(*args, **kwargs)
        if hasattr(obj,'__storage__'): 
            strg = getattr(obj, '__storage__')
            oldValue=getattr(obj, self.function.__name__)
            strg[self.function.__name__] = value if oValue is None else oValue
            if hasattr(obj,'PropertyChanged'):
                obj.PropertyChanged(
                            obj
                            ,self.function.__name__
                            , oldValue
                            , getattr(obj, self.function.__name__) #newValue
                            )