[![GitHub release](https://img.shields.io/github/release/OpenWayside/pyDictStore.svg?label=GitHub%20release)](https://github.com/OpenWayside/pyDictStore/releases)
![PyPI](https://img.shields.io/pypi/v/pyDictStore)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyDictStore)
![GitHub](https://img.shields.io/github/license/OpenWayside/pyDictStore)

# What is pyDictStore

pyDictStore adds automated dictionary storage to properties eliminating the need for code bodies, property getters and setters. It also provides a property change event.


# Minimum usage
The minimum usage of this library requires you to add the @storage decorator to your class. This will automatically wrap your properties with the auto storage capabilities. The default value applied to any property is None. To override this, you will need to apply the @default decorator to your propperty's getter. 
```python
@storage
class ExampleClass(): 
    @property
    def exampleProperty(self): ...
    @exampleProperty.setter
    def exampleProperty(self,value): ...
```

## ...with default value
```python
@storage
class ExampleClass(): 
    @property
    @default(10)
    def exampleProperty(self) -> int: ...
    @exampleProperty.setter
    def exampleProperty(self,value) -> None: ...
```
# Overriding the getter and setter

## getter

If the getter returns a value other than None it will override the value pulled by pyDictStore. The example below will result in the property always returning 12.

```python
@storage
class ExampleClass(): 
    @property
    @default(10)
    def exampleProperty(self) -> int: 
        return 12
```

## setter

Overriding the setter allows you to modify the value that is saved into storage. This is helpful if you need to perform logic against the value being passed in or if you want to force the storage type; such as parsing an integer from a string or storing a Boolean value as an integer. To do this requires ignoring normal setter conventions by using a return statement.

> :warning: **Warning:** Overriding the output does not work if you return a value of None.

```python
@storage
class ExampleClass():
    @property 
    @default(10)
    def exampleProperty(self) -> int: ...
    @exampleProperty.setter
    def exampleProperty(self,value) -> None: 
        return value * 3
```

# Event Handling
When the setter of a property is called it will raise a PropertyChanged Event within your class. This provides you the instance of the class that raised the event, the name of the property, the previous value, and the new value.

> :bulb: **Note:** When the default value is instantiated the PropertyChanged event does not fire.

## ...event handler within class

```python
@storage
class ExampleClass(): 
    def __init__(self) -> None:
        self.PropertyChanged += self.onPropertyChanged
        
    @staticmethod
    def onPropertyChanged(sender, name:str, oldValue, newValue):
        ... #Your Custom Action here
        
    @property
    @default(10)
    def exampleProperty(self) -> int: ...
    @exampleProperty.setter
    def exampleProperty(self,value) -> None: ...
```

## ...event handler external from class

```python
def onPropertyChanged(sender, name:str, oldValue, newValue):
    ... #Your Custom Action here

@storage
class ExampleClass(): 
    def __init__(self) -> None:
        self.PropertyChanged += onPropertyChanged
              
    @property
    @default(10)
    def exampleProperty(self) -> int: ...
    @exampleProperty.setter
    def exampleProperty(self,value) -> None: ...
```
