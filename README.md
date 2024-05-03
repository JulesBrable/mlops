# mlops [![Construction image Docker](https://github.com/JulesBrable/mlops/actions/workflows/prod.yaml/badge.svg)](https://github.com/JulesBrable/mlops/actions/workflows/prod.yaml)

Repository for the final project of the MLOps course (taught by R. Avouac &amp; L. Galiana during 2nd Semester of the final year at ENSAE Paris).

<br>

## Content

This project basically implement a NLP based recommender system and deploy it though a [`Streamlit`](https://streamlit.io/) app. The model built follows a very simple approach that combines an embeddings model ([`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)) with cosine similarity to make event recommendations, based on a query. We have tried to make this engine multilingual by adding a translator in the backend.

<br>

* The `app` folder contains the code and assets that are needed for the app. The code used to build the model can be found in the `app/src/models/` folder. In addition, the `app/src/utils` folder contains a lot of functions that we used to build the app.
* Finally, in order to deploy the app, we built a Docker image (with entrypoint being the run.shscript). We automated the image delivery thanks to some configuration stuff (`k8s/deployment`and `argocd` folders), hence a new image is being pushed to the DockerHub at every new version of the app.

**NB:** _The data comes from a [public website](https://opendata.paris.fr/explore/dataset/que-faire-a-paris-/export/), and can also be directly downloaded from this site. However, we added the data to a S3 bucket, accessible to the [SSP Cloud](https://datalab.sspcloud.fr/)'s solution ([`MinIO`](https://min.io/)). Hence, in our code, we directly use the data that is stored in our bucket._

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

2. Go to the app folder:
```bash
cd mlops/app
```

Then choose one of the following options, depending on whether you prefer to use [`Docker`](https://www.docker.com/) or [`conda`](https://docs.conda.io/).

### Option A: you have [`Docker`](https://www.docker.com/) installed:

3. Build the Docker image:
```bash
docker build -t mlops .
```

4. Run the Docker container:
```bash
docker run -p 5000:5000 mlops
```

### Option B: you have [`conda`](https://docs.conda.io/) installed:

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

By default, we are using port 5000, so once you have run the following command, you will be able to access the app with the following link: [http://localhost:5000/](http://localhost:5000/).

```bash
streamlit run Homepage.py --server.port=5000
```

## Further work

To make our work more robust, we could have added a feature that automatically updates events on a weekly or monthly basis. This can be done in `Kubernetes` using the `cronjob`functionality. We've tried to develop this solution, but we haven't managed to implement it.

## Contact

* [Jules Brablé](https://github.com/JulesBrable) - jules.brable@ensae.fr
* [Martin Boutier]() - martin.boutier@ensae.fr
* [Louis Latournerie]() - louis.latournerie@ensae.fr

