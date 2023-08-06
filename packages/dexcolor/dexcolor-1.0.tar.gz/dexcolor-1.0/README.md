## dexcolor

dexcolor is a Python module that provides various functions for working with colors, styles, and backgrounds in the terminal.

### Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Color Examples](#color-examples)
- [Style Examples](#style-examples)
- [Background Examples](#background-examples)
- [Rainbow Text Example](#rainbow-text-example)
- [Additional information](#Additional-Information)
- [Contribution and Feedback](#Contribution-and-Feedback)

### Installation

To install dexcolor, you can use pip:

```shell
pip install dexcolor
```

### Usage

Here is an example of how to use dexcolor:

```python
from dexcolor import DEX, style, back, RESET

# Color, Style, and Background Example
print(DEX.purple('Example', style='bold', back='yellow'))
# Output: The word "Example" will be printed in purple color, bold style, and yellow background.

# Style Example
print(style.bold('Example'))
# Output: The word "Example" will be printed in the default color with bold style.

# Background Example
print(back.red('Example'))
# Output: The word "Example" will be printed in the default color with a red background.

# Reset Example
print(DEX.purple('Example', style='bold', back='yellow') + RESET)
print(style.bold('Example') + RESET)
print(back.red('Example') + RESET)
# Output: The word "Example" in each line will be printed with the specified color, style, and background, followed by a reset to revert to the default settings.
```

### Color Examples

Here are some examples of using colors with dexcolor:

```python
from dexcolor import DEX

print(DEX.red('This text is in red color'))
print(DEX.green('This text is in green color'))
print(DEX.blue('This text is in blue color'))
```

### Style Examples

Here are some examples of using styles with dexcolor:

```python
from dexcolor import style

print(style.bold('This text is bold'))
print(style.underline('This text is underlined'))
print(style.inverse('This text is inversed'))
```

### Background Examples

Here are some examples of using backgrounds with dexcolor:

```python
from dexcolor import back

print(back.red('This text has a red background'))
print(back.green('This text has a green background'))
print(back.blue('This text has a blue background'))
```

### Rainbow Text Example

Here is an example of using the RainbowText function from dexcolor to print text in rainbow colors:

```python
from dexcolor import RainbowText

print(RainbowText.dex('text here', 'red', 'dark_gray', 'blue'))
```

The `RainbowText` function takes a string as input and generates a string with each character having a different rainbow color.

### Additional Information

For more information and additional features provided by `dexcolor`, you can refer to the [dexcolor GitHub repository](https://github.com/Terong33/dexcolor/) or the [dexcolor PyPI page](https://pypi.org/project/dexcolor/).

Please note that the provided examples are just a subset of the capabilities of `dexcolor`. You can explore the module further to discover more options and customization possibilities.

### Contribution and Feedback

If you have any suggestions, feature requests, or bug reports related to `dexcolor`, please feel free to contribute to the project on GitHub or provide feedback to the module's maintainers. Your input is valuable in improving the module and making it more versatile for a wider range of use cases.

Happy coding with `dexcolor`!
