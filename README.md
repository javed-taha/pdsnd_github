# Bike Share Data Analysis Project

Date: August 28th, 2024

## Description

This Python script analyzes bike share data for three major cities in the United States. It provides an interactive command-line interface for users to explore various statistics about bike usage patterns.

## Features

- Data loading and filtering by city, month, and day
- Time statistics (most frequent times of travel)
- Station statistics (most popular stations and trips)
- Trip duration statistics
- User statistics
- Option to view raw data

## Project Structure

- Main script: `bikeshare.py`
- Data directory: Store `chicago.csv`, `new_york_city.csv` and `washington.csv` data files.
   - Refer to [detailed instructions](data/README.md) in the data directory.
- Project setup files:
   - `environment.yml`: Use with conda
   - `requirements.txt`: Use with pip
- Other files:
   - `.gitignore`: Exclude files not required by project

## Requirements

- Python 3.12.4
- pandas 2.2.2
- numpy 1.26.4

For detailed requirements, see `environment.yml` or `requirements.txt`.

### Note on Dependencies

The specific versions listed above were used to develop and test this project. While these exact versions are recommended for the most consistent experience, the project may work with newer versions of these packages. If you encounter any issues with newer versions, please revert to the specified versions.

## Installation

This project requires Python and the following Python libraries: pandas and numpy. You can set up the environment using either Conda or pip.

### Common Steps

1. Fork the [repository](https://github.com/javed-taha/pdsnd_github.git) in GitHub.
2. Clone the repository:

```shell
git clone https://github.com/your-username/pdsnd_github.git
cd pdsnd_github
```

### Option 1: Using Conda

1. If you don't have Conda installed, follow instructions on [installing conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
2. Follow instructions in [common steps](#common-steps).
3. Create a new Conda environment using the provided `environment.yml` file
   ```shell
   conda env create -f environment.yml
   ```
4. Activate the new conda environment:
   ```shell
   conda activate project_bikeshare
   ```
   Alternatively, you can create the Conda environment manually:

```shell
conda create --name project_bikeshare python=3.12.4 pandas=2.2.2 numpy=1.26.4
conda activate project_bikeshare
```

### Option 2: Using pip

1. Ensure you have [Python](https://www.python.org/downloads/) installed on your system.
   - [Python - Version 3.12.4](https://www.python.org/downloads/release/python-3124/)
2. Follow instructions in [common steps](#common-steps).
3. Create virtual environment (preferably in project folder):
   ```shell
   python -m venv .venv
   ```
4. Activate the virtual environment

   ```shell
   # Bash
   $ source .venv/bin/activate

   # Windows Command Line
   .venv\Scripts\activate.bat

   # Windows Power Shell
   .venv\Scripts\Activate.ps1
   ```

5. Install the required packages
   ```shell
   pip install -r requirements.txt
   ```
   Alternatively, you can install the packages manually:

```shell
pip install pandas==2.2.2 numpy==1.26.4
```

## Running the Project

After setting up your environment, you can run the project using:

```
python bikeshare.py
```

This will start the interactive program that allows you to explore US bikeshare data. Follow the on-screen prompts to analyze the data.

## Resources Used

In the development of this project, the following resources were consulted:

1. Udacity - Programming for Data Science with Python
2. DataCamp - Various Python and Data Analysis courses
3. NumPy Documentation: https://numpy.org/doc/
4. Pandas Documentation: https://pandas.pydata.org/docs/
5. Python Type Hinting Documentation: https://docs.python.org/3/library/typing.html
6. Learn Python Programming (Programiz): https://www.programiz.com/python-programming
7. W3Schools Python Tutorial: https://www.w3schools.com/python/
8. Python Crash Course (Book) by Eric Matthes
9. Real Python - Python Statistics Fundamentals: https://realpython.com/python-statistics/
10. GitHub's Python .gitignore template: https://github.com/github/gitignore/blob/main/Python.gitignore
11. Python Standard Library Documentation: https://docs.python.org/3/library/
12. Stack Overflow - Various threads on Python, Pandas, and data analysis
13. Google Python Style Guide: https://google.github.io/styleguide/pyguide.html

These resources provided valuable insights into Python programming, data analysis techniques, and best practices in code organization and documentation.
