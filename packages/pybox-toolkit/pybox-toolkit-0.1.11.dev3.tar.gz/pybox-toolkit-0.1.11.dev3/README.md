# Welcome to the pybox-toolkit guide!

This tutorial will guide you through how to define and use the pybox toolkit for building Jupyter notebooks compatible with the pybox website.

Please note that it's not fully meant to be used as a template, instead open up a notebook along side it and copy over code snippets that you find useful and want to modify.

## Step 1: Installing libraries

You only need to install required libraries when you're running the notebooks locally (e.g. on your own computer).

The only _required_ library is the toolkit library, which you'll use to write your formula. You can install it by running the following command in your terminal:

```bash
pip install pybox-toolkit
```

You can also install the library from within the Jupyter notebook, by adding the following line into a code cell:

```
%pip install pybox-toolkit
```

Please only install the libraries on the list below, as they are guaranteed to be present within the website environment as well. Any other python packages, apart from the standard library, may not be available when running in the website.

### List of available libraries

Below are some of the main libraries you might end up using. For a more comprehensive list, visit: https://pyodide.org/en/stable/usage/packages-in-pyodide.html.

- [`sympy`](https://www.sympy.org/en/index.html)
- [`scipy`](https://scipy.org/)
- [`numpy`](https://numpy.org/)

## Step 2: Importing libraries

Import required libraries. At the minimum, you need to import the `toolkit` library, but you can also rely on `sympy` or the python standard library.

The `toolkit` library acts as the interface between your Jupyter notebook and the website. In addition, it also provides you with some convenient features, such as physical bounds checking, SI units, unit composition, etc, but these features will be discussed later as we encounter them.

```python
# Required import for any formula
import toolkit
# Importing the Python math library (https://docs.python.org/3/library/math.html)
# We will use the library to obtain constants, such as `math.pi` and `math.e`
import math
# Inside of pure formulas, we need to use the math functions provided by sympy
# This is explained later on
from sympy import sin
```

## Step 3: Using units

As the library is designed with engineering formulas in mind, it has support for units. You have three different options:

- stick to the SI units provided by the toolkit library
- create your own units
- create new units by composition of existing units

### Using provided SI units

Available units in the library are:

- Meter
- Second
- Kilogram
- Ampere
- Kelvin
- Mole
- Candela

You can import them from the toolkit library using a simple import statement

```python
# Replace "Meter" or "Kilogram" with your SI unit of choice
from toolkit.typing.si import Meter, Kilogram
```

### Creating new units

If you can't find the unit you need in the list of available SI units, you can create your own unit types.

A unit at its core is a Python class with two fields:

- `units`: The unit symbol (e.g. "m" for meters)
- `physical_range` (optional): Physical range in mathematical notation, e.g. `(-inf, 59]`. Default value if not provided is `(-inf, inf)`.

Your unit must extend from the `Unit` base class, meaning that a new unit definition with name "Example" and symbol "x" can be implemented as follows:

```python
from toolkit.typing import Unit

class Example(Unit):
    """ Example unit """
    units = "x"
    physical_range = "(-inf, 59]"
```

### Create units using composition

New units can also be created by composing unit classes using mathematical expressions. For example, let's say that we have unit "Meter" and unit "Second", and we want to create the unit for acceleration, meters over second squared.

Instead of creating a new class for this, we can just use composition as follows:

```python
from toolkit.typing.si import Meter, Second

Acceleration = Meter / (Second ** 2)
Acceleration.units
```

Allowed mathematical operations on unit classes are multiplication, exponentiation and division. Addition, subtraction and other operations are not allowed.

The library will perform simplification on composed units, meaning that fractions will cancel themselves out if possible:

```python
VelocityWithSimplification = (Meter * Meter) / (Second * Meter)
VelocityWithSimplification.units
```

You can also compose custom units, let's look at composing using our example unit:

```python
WeirdUnit = Example**2 * Second / Meter
WeirdUnit.units
```

Physical ranges are also dealt with automatically when doing unit composition:

```python
ExampleSquared = Example**2
ExampleSquared.physical_range
```

### Choice units

In addition to regular units, impure formulas also support "choice" units. The website user will have to select one of the several pre-defined options, which allows you to map an arbitrary string to an arbitrary value.

Each choice unit consists of a list of "entries" and a desciption.

Each entry has a value, optional name (which is used in the user-interface to represent the value) and an optional description.

However, the choice units don't have to be "instantiated" when used (see section about unit instantiation).

```python
from toolkit.typing import Choice, ChoiceEntry

choices = Choice(
    [
        ChoiceEntry("green"),
        ChoiceEntry("red", "a name different to red"),
        ChoiceEntry("yellow", description = "yellow is a weird colour"),
        ChoiceEntry("pink")
    ],
    "Colour we gossip about"
)

choices.choices[2]

```

If you run the cell above, you'll notice that the default name for a choice is equal to its value!

## Step 4: Defining a formula

A formula is a Python function, annotated with the appropriate "function decorator". The decorator tells the toolkit information about the formula, such as the units of the formula output, keywords/categories of the formula (used for catgorization on the website), etc.

There exist two different annotations, `PureFormula` and `ImpureFormula`. They differ in additional functionality they provide and constraints, but we will discuss them later.

Both decorators require you to specify two fields:

- `outputs`: a list of 2 element [tuples](https://www.programiz.com/python-programming/tuple) (_not a list of lists!_), where each tuple contains the name of an output variable and the (instantiated) unit of the variable (see the section about unit instantiation for more details).
- `keywords`: a list of string labels that categorize a specific formula. The keywords are used on the website to display formulas in their corresponding categories. Note that a single formula can have more than one keyword, and the keywords are case-insensitive.

The function itself can accept any number of arguments, as long as they are type-annotated (specify the unit type for the specific argument). Check out the full formula examples to see how this should look in practice.

A function can return multiple values by returning a tuple instead of a single value - works for both pure and impure formulas.

Finally, the function should contain a short "docstring". This is a string that comes immediately after the function signature (`def` statement), and starts & ends with three quote symbols. It should contain a short description of the formula.

That's a lot to take in at once, so here is a simple example!

```python
@toolkit.PureFormula(
    outputs = [("example_output", (Example**2)("This is covered later ;)"))],
    keywords = ["label 1", "label 2", "3 labels, are you crazy!?"]
)
def example_formula(example_input: Example("I Wonder why this is here")):
    """ This is the docstring """
    i = example_input ** 2
    i += 5 # Magic constant
    return i
```

Note that when we run a formula, it doesn't return the same output as a regular python function. Here is what it looks like:

```python
example_formula(5)
```

Notice that the output is a list of dictionaries. This is because a function could return multiple sets of outputs, for example:

```python
example_formula(example_output = 30)
```

### Unit instantiation

Both the output unit types and the function argument annotations require you to "instantiate" the unit. While it sounds scary, it simply means that you need to provide a short description for the argument which uses that particular unit.

Example unit instantiations:

```python
MeterInstance = Meter("This is the length of an imaginary thing")
MeterInstance.description

ChoiceInstance = Choice(
    [
        ChoiceEntry(1, "choice 1", "not a good choice"),
        ChoiceEntry(2, "choice 2", "a better choice")
    ],
    "Description of choices as a whole"
)
```

There is no actual need to instantiate your units like that outside a formula, it's just for example.

### Pure formulas

"Pure" formulas are formulas which can be expressed as a single mathematical expression. They operate under stricter conditions than impure formulas, as they don't allow you to perform any form of flow control (no loops, `if` statements, etc.).

The expression within the function should return a [sympy](https://docs.sympy.org/latest/reference/index.html#reference) expression composed of input arguments (which act as sympy variables), constants, and sympy functions (e.g. `sympy.sin` or `sympy.sqrt`).

While the constraints on the pure formulas may seem arbitrary and discouraging, they provide the website users with one major benefit: pure formulas can be "inverted", meaning that if inputs `a` and `b` result in output `c`, the expression can be **automatically** changed to express `b` from `a` and `c`.

In the example below, we create a pure formula which can be used to calculate the area of the sphere. The formula has one output, the computed area, which is expressed in meters squared. The description of the output is "Area of sphere".

The formula also has one input, namely the radius. It is expressed in meters, and the description of the parameter is "Radius of sphere".

The formula also contains a docstring, which is "Compute the area of a sphere".

```python
@toolkit.PureFormula(
    outputs = [("area", (Meter**2)("Area of sphere"))],
    keywords = ["Sphere"]
)
def area_of_sphere(radius: Meter("Radius of sphere")):
    """Compute the area of a sphere"""
    area = math.pi * 4 * radius**2
    return area
```

```python
area_of_sphere(radius = 2)
```

```python
area_of_sphere(area = 4)
```

If you want to use mathematical functions, you'll have to use those provided by sympy: https://docs.sympy.org/latest/modules/functions/elementary.html.

```python
from sympy import log

@toolkit.PureFormula(
    outputs = [("logarithm", Unit("Calculated log"))],
    keywords = ["Log"]
)
def my_log(x: Unit("Number to take the log of")):
    """Compute Gumbel distribution parameters from two points of the CDF."""
    return log(x)
```

Sympy is not bullet proof however, sometimes it won't be able to figure out how to reverse a formula, or it won't support a feature you need, so definitely try to test it thoroughly. This manifests in the form of nothing happening when you try to run the formula with certain inputs, leading to the program "hanging". You may also get an error after defining a formula, such as "could not determine the value of a relational", in which case your formula may not be suited to be pure. In any of those scenarios, it's recommended you stick to an impure formula, or make a note of which input sets will cause sympy to hang.

### Impure formulas

"Impure" formulas are declared in the same way as pure formulas, with the only difference being that you are allowed to use any Python code in the method body, including if statements, loops, etc. However, the expression cannot be inverted automatically, resulting in a worse user experience when compared to pure formulas.

Below is an example of an impure formula. The formula has one input argument, namely a choice between 4 different colours. The description of the `Choice` is "Color we gossip about". It has one output, which has the description "Score for the chosen colour".

```python
@toolkit.ImpureFormula(
    outputs = [("score", (Unit)("Score for the chosen colour"))],
    keywords = ["Colours"]
)
def we_like_green(colour: Choice([ChoiceEntry("green"), ChoiceEntry("red"), ChoiceEntry("yellow"), ChoiceEntry("pink")], "Colour we gossip about")):
    """ We really like green, who knows why. """
    scores = {"green": 10000, "red": 5, "yellow": 2}

    if len(scores) < 2:
        return -3

    if colour not in scores: return -1
    return scores[colour]
```

## Step 5: Writing documentation

Formulas must have documentation provided. It uses a specific markdown format, that should start with the following sequence:

```markdown
# Documentation: we_like_green
```

`we_like_green` should be replaced by the name of your function.

Then, you can follow it up with an arbitrary number of key-value pairs. They are currently unused, but there may be a use-case for them in the future.

```markdown
**Key1**: value1

**Key2**: value2
```

After that, write documentation as you would normal markdown document. LaTeX **is supported**. Note that subsequent markdown cells in the notebook will also be consumed as documentation. To clearly define where your documentation end, finish it with:

# End documentation

## Step 6: Writing tests (recommended)

Tests for a function are a collection of functions within a test class. The class itself should be decorated with the `test.set_function` decorator, with the name of the function under test provided as the argument. Furthermore, the test class should extend the `toolkit.test.ToolkitTests` class.

Each individual test is a function in the test class, which takes only one argument, `self`. It should be decorated with `@toolkit.test.test`.

Within the function, you can call `self.documented_test` and provide two arguments:

- `arguments`: Input arguments for the formula, expressed as a dictionary
- `expected`: A dictionary of expected output values.

self.documented_test allows the test cases to be automatically validated & extracted and then uploaded to the website (next to the formula documentation) when you upload your notebook. Toolkit tests work with [unittest](https://docs.python.org/3/library/unittest.html) behind the scenes. That means you can use methods from unittest, but those tests won't be documented on the website.

```python
@toolkit.test.set_function(
    area_of_sphere
)
class AreaOfSphereTests(toolkit.test.ToolkitTests):
    @toolkit.test.test
    def radius1(self):
        self.documented_test(                   # This test case will be documented and appears on the website!
            arguments = {"radius": 1},
            expected = {"area": 4 * math.pi}
        )

    @toolkit.test.test
    def radius2(self):
        calculated_radius = self.function(area = 4)[0]["radius"] # Outputs follow the form: [{"radius": ...}, {"radius": ...}, ...]
        self.assertTrue(calculated_radius < 2) # This won't be documented, but will run
```

In documented tests, numbers will be checked to be within either 5% or 0.00001 of each other (whichever is greatest). This means the numbers don't have to match up exactly, but that's a result of how computers handle decimals.

### Running tests locally

You can run tests locally by calling `function_name.run_tests()`:

```python
area_of_sphere.run_tests()
```

You probably don't want your tests to be run like this on PyBox, so before running tests, you can tell us that all the useful content of the notebook has already been written by writing:

# End notebook

Now any code or documentation you write after will be ignored!

```python
print("Nobody will see this message!")
```

Please note that although you can have multiple formulas per notebook, it is highly recommended to only include one. That just makes it easier for maintainers and other contributors to keep track of where formulas are coming from!

For now that's all you need to worry about! Before you know it, your notebooks too can be on the website :)
