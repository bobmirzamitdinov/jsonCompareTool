# jsonCompareTool (Python)

**jsonCompareTool** is a Python command-line utility designed for comparing large JSON datasets contained in two separate files, `old.json` and `new.json`.It effectively highlights differences and optionally ignores specified discrepancies, presenting results in clear, tabular format

## Table of Contents
- [Features](#features)
- [Installation](#installation)

## Features

- **Mass Comparison**: Capable of handling hundreds of messages, allowing for mass comparison of two JSON blocks in separate files
- **User Input for Ignoring Differences**: Before running the comparison, the tool prompts users to specify any keys for which differences should be ignored, ensuring flexibility in handling expected discrepancies
- **Dual Results Presentation**: Outputs two distinct results tables—one for differences that are considered significant and another for those that have been ignored based on user input

## Installation

To use **jsonCompareTool**, follow these simple steps:

1. Make sure you have Python 3.x installed on your system.
2. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/bobmirzamitdinov/jsonCompareTool.git

3. Navigate to the cloned directory:
      ```bash
   cd jsonCompareTool
4. Optionally, you can create a virtual environment:
      ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
5. Install the required dependencies (if any):
      ```bash
   pip install -r requirements.txt

Usage
To run jsonCompareTool, use the following command:
   ```bash
   python jsonCompareTool.py