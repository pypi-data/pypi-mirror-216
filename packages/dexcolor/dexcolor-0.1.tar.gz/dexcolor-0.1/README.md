## dexcolor

`dexcolor` is a Python module that provides functionality for printing text with different colors, styles, and backgrounds in the terminal. It offers a convenient way to add visual enhancements to your console output.

### Installation

You can install `dexcolor` using pip:

```
pip install dexcolor
```

### Usage

Here are some examples of how to use `dexcolor`:

#### Example 1: Using color, style, and background

```python
from dexcolor import DEX

print(DEX.purple('Example', style='bold', back='yellow'))
```

Output: The word "Example" will be printed in purple color, bold style, and yellow background.

#### Example 2: Using style only

```python
from dexcolor import style

print(style.bold('Example'))
```

Output: The word "Example" will be printed in the default color with bold style.

#### Example 3: Using background only

```python
from dexcolor import back

print(back.red('Example'))
```

Output: The word "Example" will be printed in the default color with a red background.

#### Example 4: Using reset

```python
from dexcolor import DEX, style, back, RESET

print(DEX.purple('Example', style='bold', back='yellow') + RESET)
print(style.bold('Example') + RESET)
print(back.red('Example') + RESET)
```

Output: The word "Example" in each line will be printed with the specified color, style, and background, followed by a reset to revert to the default settings.

### Additional Information

For more information and additional features provided by `dexcolor`, you can refer to the [dexcolor GitHub repository](https://github.com/Terong33/dexcolor) or the [dexcolor PyPI page](https://pypi.org/project/dexcolor/).

Please note that the provided examples are just a subset of the capabilities of `dexcolor`. You can explore the module further to discover more options and customization possibilities.

### Contribution and Feedback

If you have any suggestions, feature requests, or bug reports related to `dexcolor`, please feel free to contribute to the project on GitHub or provide feedback to the module's maintainers. Your input is valuable in improving the module and making it more versatile for a wider range of use cases.

Happy coding with `dexcolor`!