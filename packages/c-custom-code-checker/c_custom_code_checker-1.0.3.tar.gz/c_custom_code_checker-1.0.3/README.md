# c-custom-code-checker

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

A custom syntax validator for the C language, which allows you to create custom rules to validate code.
It is a useful tool to verify that the developed code is in accordance with the team's standards.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Contributing](#contributing)

## Installation

### Requirements

#### Clang

This project use [libclang](https://github.com/llvm/llvm-project/releases/) tools to handle with C files and to create the AST. You need to install it, and set libclang installation path on PATH environment variable 


### Installing required python modules

```bash
pip install -r requirements.txt

```

### Installing by pip

This project is available on pip repository, you just have to write the follow command

```
    pip install c-custom-code-checker

```


## Usage

A typical use of this tool is shown below.

```
     c-validator --input {files or directory to check} -r {folder where rules are declared}
```


## How it works?

### Understanding rules files

Rules are abstractions of your team's commitments or agreements. In practice, it is a JSON file with reserved keys to indicate what do you want to check.


#### Rule format

Rule file can be understood easily splitting the file on two parts. The first one describe the [target](#accepted-target-values) of this rule, what do you want to verify, to be precise what kind of token do you want to check (e.g: Variables, macros, functions, etc.).


The second part, is about the **criterion** that you want to use to validade the target token. An object is used to agrupate criterion data.

```
{
    "target":["variables","globals","macros"],
    "description": "Variable declaration name must have length lower than 31 bytes",
    "criterion":{
        "target":"length_less_than",
        "value": 31
    }

}
```


##### Criterion object

It's a simple JSON object with two reserved keys, **target** to indicate what kind of criterion is wanted to use, and **value** to indicate what is the expected value to this taget. The snippet bellow show how a criterion object is created.

```
{
    "criterion":{
        "target":"length_less_than",
        "value": 31
    }
}
```

###### Accepted Criterion target values

|   Target Value    |   Description |
|-------------------|---------------|
|"length_less_than" | Verify if target has length name lower than target informed              |
| "length_bigger_than" | Verify if target has length name bigger than target informed           |
| "prefix" |    Verify if target name has the informed prefix |
| "suffix"  |  Verify if target name has the informed suffix |
| "regex" | Verify if a node name is accept by informed regular expression|



###### Accepted target values

|   Target Value    |   Description |
|-------------------|---------------|
|  "functions"        |   This rule target are the functions declaration            |
|   "globals"        |   This rule target are the global variables                |
|   "variables"      |   This rule target are the local variables                 |
|   "macros"          |  This rule target are Macros declarations                     |


## Contributing

Thank you for your interest in contributing to this project! We welcome contributions from the community, as they help make this project better.

To contribute, please follow these guidelines:

1. Fork the repository and create your own branch for your contributions.
2. Make your changes or additions in the branch.
3. Ensure that your code adheres to the project's coding standards and conventions.
4. Test your changes thoroughly.
5. Document any new features or changes in the appropriate sections of the project's documentation.
6. Submit a pull request with your changes, providing a clear and descriptive explanation of the purpose and scope of the pull request.
7. Once submitted, the project maintainers will review your pull request and provide feedback or merge it if appropriate.

Please note that by contributing to this project, you agree to abide by the project's code of conduct (if applicable).

If you're unsure about anything or have any questions, feel free to open an issue or contact the project maintainers. We appreciate your contributions and look forward to working with you!
