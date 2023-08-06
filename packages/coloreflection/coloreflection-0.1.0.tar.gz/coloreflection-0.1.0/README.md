![Coloreflection icon](https://github.com/Addefan/coloreflection/blob/main/images/logo.png?raw=true)

# Coloreflection

A tool with which you can use colors in your Python code to decorate terminal output.

## Install

```shell
pip install coloreflection
```

or,

```shell
poetry add coloreflection
```

## Capabilities

### Dark PyCharm theme

![Styles with dark PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/styles_dark.png?raw=true)
![Foreground colors with dark PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/foreground_dark.png?raw=true)
![Background colors with dark PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/background_dark.png?raw=true)

### Light PyCharm theme

![Styles with light PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/styles_light.png?raw=true)
![Foreground colors with light PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/foreground_light.png?raw=true)
![Background colors with light PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/background_light.png?raw=true)

## Usage

```python
from coloreflection import Color

C = Color()

print(C.border(" Using style for text "))
print(C.FG.red("Changing text color"))
print(C.BG.green("Changing text background"))

print(C.border(C.bold(C.FG.pink("You can"))), "combine", 
      C.BG.blue(C.FG.yellow(f"different colors{C.reverse(' and styles.')}")))
```
![Usage examples](https://github.com/Addefan/coloreflection/blob/main/images/usage.png?raw=true)
