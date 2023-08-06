# [fortext](https://4mbl.link/gh/fortext)
Text stylizer for Python. Mainly useful for CLI output.

## Table of Contents

* [Table of Contents](#table-of-contents)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Text styling](#text-styling)
  * [Syntax highlighting](#syntax-highlighting)
  * [Permutations](#permutations)



## Getting Started

### Prerequisites
* Install or update the [pip](https://pip.pypa.io/en/stable/) package manager.
  ```sh
  python3 -m pip install --upgrade pip
  ```

* It's also recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html).
  * Linux / MacOS
    ```bash
    python3 -m venv <venv-name>
    source venv/bin/activate
    ```
  * Windows
    ```bash
    python3 -m venv <venv-name>
    <venv-name>/Scripts/activate
    ```

### Installation

Use pip to install `fortext`.

```bash
python3 -m pip install --upgrade fortext
```

Install the required dependencies as listed on [requirements.txt](./requirements.txt).
```shell
python3 -m pip install -r requirements.txt
```

## Usage

### Text styling

```python
from fortext import style, Bg, Frmt
print(style('Hi, human.', fg='#ff0000'))
print(style('RGB tuple or list also works.', fg=(0, 255, 0)))
print(style('You can also use predefined colors.', bg=Bg.BLACK))
print(style('Want to be bold?.', frmt=[Frmt.BOLD]))

print(
    style('Want to go all in?',
          fg='#ff0000', bg=Bg.BLACK,
          frmt=[Frmt.BOLD, Frmt.UNDERLINE, Frmt.ITALIC]))
```

### Syntax highlighting

```python
from fortext import highlight
print(highlight({'somekey': 'somevalue', 'anotherkey': [12.4, True, 23]}))
```
Output:

![syntax highlighting example output](./img/syntax_highlighting.png)

### Permutations
```python
from fortext import permutations
for perm in permutations('abc'):
    print(perm)
```
Output:
```
a
b
c
ab
ac
ba
bc
ca
cb
abc
acb
bac
bca
cab
cba
```
