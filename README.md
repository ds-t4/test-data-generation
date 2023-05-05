# Automated Test Data Generation Using Search-based Algorithm

DataScience-T4

## Folders and Code Structure

- `nsga/`: customized implementation of the NSGA-II helper functions including the customized definition of Sampling, Crossover, Mutation, and Selection function. 

- `sample/`: sample test problems including `BucketList` and `Quadratic`

- `NSGA.py`: implementation and initialization of the NSGA-II algorithm

- `Random.py`: implementation of the random testing algorithm(the traditional approach)  

- `Application.py`: code to initialize the NSGA-II and render it in the frontend


## Installation
Create a virtual environment and activate it:

```bash
$ python3 -m venv env
$ source env/bin/activate
```

Install the modules necessary to run this application:
```bash
$ pip install -r requirements.txt
```

## Run the Application

1. To run the frontend of the application:
```bash
$ streamlit run ./Application.py: 
```

2. To run the NSGA-II algorithm script in the terminal:
```bash
$ python3 NSGA.py
```

3. To run the random algorithm script (traditional approach) in the terminal:
```bash
$ python3 Random.py
```