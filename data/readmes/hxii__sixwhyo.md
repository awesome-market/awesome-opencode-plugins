![sixwhyo](./assets/sixwhyo.svg)

# sixwhyo (6 y.o.)

<center><i>Dad, is this function so long because it is Python?</i></center>

![MIT License](https://img.shields.io/badge/License-MIT-000?style=flat-square)

`sixwhyo` asks "Why?" for you, the adult who is stuck in their fixed mindset,
expected conventions and beliefs about how code should look and work.

`sixwhyo` tears down the over-engineered castles you've built for yourself for absolutely no
reason just because that's either what you're used to, or someone told you to
do it that way.

The inspiration for this was:

- My own 6-year-old, Andy! ❤️
- [Ponytail](https://github.com/DietrichGebert/ponytail/)

## Skills

| Skill               | Description                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `sixwhyo`           | A six-year-old code reviewer who asks "why?" about everything. Catches over-engineering, confusing names, and unnecessary complexity. |
| `sixwhyo-summarize` | Output is a 1-2 line summary of the request as a whole: how is the file? Is the class nice? Is the function correct?                  |
| `sixwhyo-simplify`  | Corrects the code through the lens of a 6-year-old, maintaining simplicity and readability.                                           |

## Usage

| Trigger             | What happens                                                                                        |
| ------------------- | --------------------------------------------------------------------------------------------------- |
| Say `6yo`           | The kid turns on and stays on. Persists across responses until you say `stop` or `go to your room`. |
| `sixwhyo-simplify`  | One-shot: reviews and rewrites the code, then exits.                                                |
| `sixwhyo-summarize` | One-shot: produces a 1-2 line summary of the file, then exits.                                      |

## Install

### OpenCode

To install globally

```shell
mkdir -p ~/.config/opencode/skills/ && git clone https://github.com/hxii/sixwhyo.git ~/.config/opencode/skills/sixwhyo
```

To install in your project

```shell
mkdir -p .opencode/skills/ && git clone https://github.com/hxii/sixwhyo.git .opencode/skills/sixwhyo
```

### Oh My Pi (omp)

Via `omp`

```shell
omp plugin install github:hxii/sixwhyo
```

### Pi

Via `pi`

```shell
pi install git:github.com/hxii/sixwhyo
```

To install globally

```shell
mkdir -p ~/.agents/skills/sixwhyo && git clone https://github.com/hxii/sixwhyo.git ~/.agents/skills/sixwhyo
```

To install in your project

```shell
mkdir -p .agents/skills/sixwhyo && git clone https://github.com/hxii/sixwhyo.git .agents/skills/sixwhyo
```

### Codex

Run

```shell
codex plugin marketplace add hxii/sixwhyo
```

## Example

```python
# calculator.py
from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

class AdditionOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b

class SubtractionOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b

class MultiplicationOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b

class DivisionOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

class OperationFactory:
    @staticmethod
    def create_operation(op_type: str) -> Operation:
        if op_type == "add":
            return AdditionOperation()
        elif op_type == "subtract":
            return SubtractionOperation()
        elif op_type == "multiply":
            return MultiplicationOperation()
        elif op_type == "divide":
            return DivisionOperation()
        else:
            raise ValueError(f"Unknown operation: {op_type}")

class Calculator:
    def __init__(self):
        self.factory = OperationFactory()

    def calculate(self, op_type: str, a: float, b: float) -> float:
        operation = self.factory.create_operation(op_type)
        return operation.execute(a, b)

def main():
    calc = Calculator()
    result = calc.calculate("add", 5, 3)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

**becomes**

````
This file is too big and I'm confused.

**Why is it called test.py when it says calculator.py inside?**
The comment on line 1 says "calculator.py" but the file is test.py. That's like putting a "cat" label on a dog.

**Why so many classes for adding numbers?**
You have:
- One class to say "what an operation is" (Operation)
- Four classes for adding, subtracting, multiplying, dividing
- One class to make the operations (OperationFactory)
- One class to use the operations (Calculator)

That's 7 classes to do `a + b`. I can do that with just `a + b`.

**Why does the factory need to exist?**
The factory takes a string like "add" and returns an AdditionOperation. But why not just do the math right there? When I want to add 5 and 3, I don't need to build a machine first.

**Why does Calculator need its own class?**
It just has one method that asks the factory for an operation and runs it. That's two lines of code, not a whole class.

**What's good:**
You did check for dividing by zero. That's smart because dividing by zero makes numbers explode.

**My question:**
Why can't this whole file just be:

```python
def calculate(op, a, b):
    if op == "add": return a + b
    if op == "subtract": return a - b
    if op == "multiply": return a * b
    if op == "divide":
        if b == 0: raise ValueError("Cannot divide by zero")
        return a / b
    raise ValueError(f"Unknown operation: {op}")
```

That's 8 lines instead of 56. Do we really need all those classes?
````
