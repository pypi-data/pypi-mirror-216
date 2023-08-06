# RaiseTool

The project contains small class for formatting thrown exception messages.

The message can be formatted with information about the class, method, and line number where the exception was thrown.

## Public methods
```
Raise.message(message:str, class_name:Optional[str],currentframe:Optional[FrameType])-> str
Raise.attribute_error(message:str, class_name:Optional[str],currentframe:Optional[FrameType])-> AttributeError
Raise.connection_error(message:str, class_name:Optional[str],currentframe:Optional[FrameType])-> ConnectionError
Raise.key_error(message:str, class_name:Optional[str],currentframe:Optional[FrameType])-> KeyError
Raise.os_error(message:str, class_name:Optional[str],currentframe:Optional[FrameType])-> OSError
Raise.syntax_error(message:str, class_name:Optional[str],currentframe:Optional[FrameType])-> SyntaxError
Raise.type_error(message:str, class_name:Optional[str],currentframe:Optional[FrameType])-> TypeError
Raise.value_error(message:str, class_name:Optional[str],currentframe:Optional[FrameType])-> ValueError
```

## Usage examples

```
import inspect
from raisetool.formatter import Raise


class Example:
    def __init__(self):
        print(f"1: {Raise.message('example message 1')}")
        print(
            f"2: {Raise.message('example message 2', self.__class__.__name__)}"
        )
        print(
            f"3: {Raise.message('example message 3', self.__class__.__name__, inspect.currentframe(), )}"
        )
        try:
            raise Raise.value_error(
                "example message 4",
                self.__class__.__name__,
                inspect.currentframe(),
            )
        except ValueError as ex:
            print(f"4: {ex.__class__.__name__}: {ex}")


if __name__ == "__main__":
    obj = Example()
```
Output:
```
1: example message 1
2: Example: example message 2
3: Example.__init__ [line:21]: example message 3
4: ValueError: Example.__init__ [line:24]: example message 4
```
