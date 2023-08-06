# Installation

We recommend using conda to manage the environment.
Other methods may also work well such like using docker or virtual env.

Choose one of the following installation methods.

## PyPI

Simple installation from PyPI

```bash
pip install -U idrlnet
```

Note: To avoid version conflicts, please use some tools to create a virtual environment first.

## Docker

Pull latest docker image from Dockerhub.

```bash
docker pull idrl/idrlnet:latest
docker run -it idrl/idrlnet:latest bash
```

Note: Available tags can be found in [Dockerhub](https://hub.docker.com/repository/docker/idrl/idrlnet).

## Anaconda

```bash
conda create -n idrlnet_dev python=3.8 -y
conda activate idrlnet_dev
pip install idrlnet
```

## From Source

```
git clone https://github.com/idrl-lab/idrlnet
cd idrlnet
pip install -e .
```
