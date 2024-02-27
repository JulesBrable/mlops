# mlops
Repository for the final project of the MLOps course (taught by R. Avouac &amp; L. Galiana during 2nd Semester of the final year at ENSAE Paris).

## Setup Instructions

From the command line, you will have to follow the following steps to set this project up:

1. Clone this repository:

```bash
git clone https://github.com/JulesBrable/mlops.git
```

2. Go to the project folder:
```bash
cd mlops
```

3. Create and activate conda env:

```bash
conda create -n mlops python=3.9.16
```

```bash
conda activate mlops
```

4. Install the listed dependencies:
   
```bash
pip install -r requirements.txt
```

## Web application

1. Go to the app folder:

```bash
cd app
```

2. Run this app locally:

```bash
streamlit run app.py --server.port=8000
```

[![Construction image Docker](https://github.com/JulesBrable/mlops/actions/workflows/prod.yaml/badge.svg)](https://github.com/JulesBrable/mlops/actions/workflows/prod.yaml)

## Contact

* [Jules Brablé](https://github.com/JulesBrable) - jules.brable@ensae.fr
* [Martin Boutier]() - martin.boutier@ensae.fr
* [Louis Latournerie]() - louis.latournerie@ensae.fr

