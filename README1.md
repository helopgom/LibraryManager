# Library Manager 📚

## Index

- [Overview](#description)
- [Features](Features)
- [Requirements](#Requirements)
- [Installation and Configuration](#installation-and-configuration)
- [Routes](#routes)
- [Functional Features](#functional-features)
- [Technical Features](#technical-features)
- [Project Developers](#project-developers)


## Overview

We develop a system for managing a library through a CRUD so that your database can be kept up to date. The objective of the project is to be able to add, consult, filter, and delete records (users, books, loans and book categories); as well as add information and create a loan delay alert service.

## Features

To see the complete design of the application, you can visit our [Mockup on Figma](https://www.figma.com/design/Syc6WSsElojyub37hdt74n/InfoCatEmbalses?node-id=0-1&t=vcxeJOXpPUZyGfoA-0).

- Connects to a PostgreSQL database using psycopg2.
- Implements logging to track application events and errors.
- Uses abstract base classes to define and enforce methods.
- Includes unit tests with pytest and mock to ensure code quality.

## Requirements

- Python 3.7 or higher.
- psycopg2 for PostgreSQL database interaction
- pytest for running tests
-  mock for mocking objects in tests

## Installation and Configuration

To install the required packages, you can use pip. It's recommended to create a virtual environment for your project.

- Create a virtual environment:

bash

python -m venv venv

Activate the virtual environment:

    On Windows:

    bash

venv\Scripts\activate

On macOS/Linux:

bash

    source venv/bin/activate

Install the dependencies:

bash

pip install psycopg2-binary pytest mock


## Project Developers

### Frontend
- [Belen](https://github.com/Belensanchez1989): Scrum Master
- Esther P. Sarasua: Developer
- Conchy Pereira: Developer
- Belén Sanchez: Developer

### Backend
- Isamar Romero: Developer
- [Lara](https://github.com/laradrb): Product Owner