# esoteric-sigdigs
**🐍 A Python package that detects and rounds numbers to significant digits.**

This package aims to provide easy-to-use functions to work with significant digits (also known as significant figures).

⚠ Please note that this package is almost certainly laced with bugs, so use it at your own risk! Additionally, the significant digit rules used may not be exactly what you are looking for; I have designed this package to fit the likely-esoteric way I have been taught to use significant digits. Sorry! If you encounter any issues, please create an issue on GitHub (*https://github.com/ericli3690/esoteric-sigdigs*) or email me at *ericli3690@gmail.com*.

## 🛠 Installation and Use

`>> pip install esoteric-sigdigs`

```python
from sigdigs import function_name_here
function_name_here(arguments_here)
```

## 🧪 What is Scientific Notation?

Scientific notation is often used by this package, a string formatting of numbers which takes the following form:

`a.bcdEf`

And which can be written in standard formatting as

`a.bcd * 10^f`

It can be seen that f represents the exponent.

Here are some more examples, shown in scientific notation while pretending that trailing zeros are NOT significant (this is not how functions like *standard_to_scientific* in this package actually behave!):

| Standard Formatting         | Scientific Notation         |
|-----------------------------|-----------------------------|
| `123456`                    | `1.23456E5`                 |
| `120000`                    | `1.2E5`                     |
| `-0.0000056`                | `-5.6E-6`                   |
| `10`                        | `1E1`                       |
| `8`                         | `8E0`                       |
| `100000000000`              | `1E11`                      |

## ⚙ Functionality

### 🟥 sigdigs(*vals:float) -> int

Returns the number of significant digits of a provided float.

Given a list of numbers, it returns the lowest significant digits number provided by any of the floats in the list.

Trailing zeros are considered significant.

Zeros are considered to have one significant digit.

**Examples:**

| Input                                            | Output          |
|--------------------------------------------------|-----------------|
| `123.456`                                        | `6`             |
| `100.0`                                          | `4`             |
| `0.00056`                                        | `2`             |
| `-34`                                            | `2`             |
| `4000`                                           | `4`             |
| `1`                                              | `1`             |
| `0`                                              | `1`             |
| `0.000`                                          | `1`             |
| `123.456, 100.0, 0.00056, -34, 4000`             | `2`             |

### 🟨 round_to_sigdigs(val:float, sig:int) -> str

Rounds a float to an integer number of significant digits.

Always returns answers in scientific notation.

**Examples:**

| Value               | Sigdigs              | Output                |
|---------------------|----------------------|-----------------------|
| `3.255`             | `5`                  | `3.2550E0`            |
| `-8.33`             | `1`                  | `-8E0`                |
| `0.0056`            | `1`                  | `6E-3`                |
| `1234.5678`         | `2`                  | `1.2E3`               |
| `0`                 | `4`                  | `0E0`                 |
| `0.000`             | `9`                  | `0E0`                 |

### 🟩 scientific_to_standard(val:str) -> str:

Converts a number in scientific notation to normal formatting, IF POSSIBLE.

Sometimes, converting to normal formatting would involve adding extra significant digits (ex. 1.2E3 cannot be rewritten as 1200, as this would involve adding two new significant digits).

In these cases, this function will simply return the input.

**Examples:**

| Scientific Notation         | Standard Formatting         |
|-----------------------------|-----------------------------|
| `1.23456E5`                 | `123456`                    |
| `1.2E5`                     | `1.2E5`                     |
| `-5.6E-6`                   | `-0.0000056`                |
| `1.0E1`                     | `10`                        |
| `8E0`                       | `8`                         |
| `1E11`                      | `1E11`                      |
| `0E0`                       | `0`                         |

### 🟩 standard_to_scientific(val:float) -> str:

The inverse of the above operation!

Converts a float into scientific form.

**Examples:**

| Standard Formatting         | Scientific Notation         |
|-----------------------------|-----------------------------|
| `123456`                    | `1.23456E5`                 |
| `120000`                    | `1.20000E5`                 |
| `-0.0000056`                | `-5.6E-6`                   |
| `10`                        | `1.0E1`                     |
| `8`                         | `8E0`                       |
| `100000000000`              | `1.00000000000E11`          |
| `0`                         | `0E0`                       |

### 🟦 round_to_sigdigs_and_standard_form_given_source(val:float, sigsource:list) -> str:

This is a common routine that I personally find useful.

Imagine a calculation being performed...

```
V = lwh

l = 50.0
w = 0.02345
h = 10

V = 11.725... but to how many significant digits?
```

This routine uses *scientific_to_standard*, *round_to_sigdigs*, and *sigdigs* to solve this efficiently.

For example, for this question, to obtain V with proper significant digits:

`round_to_sigdigs_and_standard_form_given_source(50.0 * 0.02345 * 10, [50.0, 0.02345, 10])`

Which outputs `12`, as expected.