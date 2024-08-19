# Library Manager 📚

## Index

- [Overview](#description)
- [Features](Features)
- [Requirements](#Requirements)
- [Installation and Configuration](#installation-and-configuration)
- [Project Developers](#project-developers)


## Overview

We develop a system for managing a library through a CRUD so that your database can be kept up to date. The objective of the project is to be able to add, consult, filter, and delete records (users, books, loans and book categories); as well as add information and create a loan delay alert service.

## Features

- Connects to a PostgreSQL database using psycopg2.
- Implements logging to track application events and errors.
- Uses abstract base classes to define and enforce methods.
- Includes unit tests with pytest and mock to ensure code quality.

## Requirements

- psycopg2 2.9.9 for PostgreSQL database interaction
- pytest 8.3.1 for running tests
- python-mock 3.14.0 for mocking objects in tests

## Installation and Configuration

To install the required packages, you can use pip. It's recommended to create a virtual environment for your project.

- Clone the repository:

        git clone https://github.com/helopgom/LibraryManager.git

- Navigate into the project directory:

        cd your-repository

- Create a virtual environment: 

            python -m venv venv

- Activate the virtual environment:

       On Windows:

       venv\Scripts\activate

- On macOS/Linux:

      source venv/bin/activate

- Install the dependencies:

      pip install psycopg2-binary pytest mock


## Project Developers

- [Belen](https://github.com/Belensanchez1989): Scrum Master
- [Lara](https://github.com/laradrb): Product Owner
- [Esther](https://github.com/Fire-Fairy84): Developer
- [Helena](https://github.com/helopgom): Developer 
- [Paola F.](https://github.com/0795PAO): Developer 

