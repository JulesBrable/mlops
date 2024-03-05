# mlops [![Construction image Docker](https://github.com/JulesBrable/mlops/actions/workflows/prod.yaml/badge.svg)](https://github.com/JulesBrable/mlops/actions/workflows/prod.yaml)

Repository for the final project of the MLOps course (taught by R. Avouac &amp; L. Galiana during 2nd Semester of the final year at ENSAE Paris).

<br>

To access our [`Streamlit`](https://streamlit.io/) app, that is, the main output of this project, one can access the latest deployed version just by clicking [here](https://mlops.kub.sspcloud.fr/). Indeed, the app is deployed on a `Kubernetes` cluster hosted by [SSP Cloud](https://datalab.sspcloud.fr/).

<br>

On the other hand, you might want to run this app locally. This is why we are giving you the following steps to set the project up.

## Setup Instructions

### General instructions

Firstly, from the command line, you will have to run the following commands:

1. Clone this repository:

```bash
git clone https://github.com/JulesBrable/mlops.git
```

2. Go to the project folder:
```bash
cd mlops
```

Then, choose between [option **A**](#A.-If-you-have-[`Docker`](https://www.docker.com/)-installed:) and option [option **A**](#A.-If-you-have-[`conda`](https://docs.conda.io/)):

### A. If you have [`Docker`](https://www.docker.com/) installed:

3. Build the Docker image:
```bash
docker build -t mlops .
```

4. Run the Docker container:
```bash
docker run -p 5000:5000 mlops
```

### B. If you have [`conda`](https://docs.conda.io/) installed:

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

### Run the app locally:

By default, we are using port 5000, so once you have run the following command, you will be able to access the app with the following link: [http://localhost:5010/](http://localhost:5000/).

```bash
streamlit run Homepage.py --server.port=5000
```

## Contact

* [Jules Brablé](https://github.com/JulesBrable) - jules.brable@ensae.fr
* [Martin Boutier]() - martin.boutier@ensae.fr
* [Louis Latournerie]() - louis.latournerie@ensae.fr

