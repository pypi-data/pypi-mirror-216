MVF stands for model validation framework. MVF is a pluggable ML/statistical modelling framework that allows for the easy comparison of models implemented in Python and R. Write simple wrapper classes for your models and compare their performance on a particular dataset.

Test change on dev branch

Test change on dev-tk branch

## Getting started

For full documentation of the project and instructions on how to get started, visit the [documentation site](https://tomkimcta.gitlab.io/model-validation-framework).

## Main features

* Automates the supervised ML workflow with simple configuration.
* R and Python models can be plugged in easily.

## For developers

### Dependencies

You need Python>=3.9 and R>=4.0. 

Additionally, you must have a working installation of the `R6`, [`IRkernel`](https://github.com/IRkernel/IRkernel) and `arrow` R packages to leverage the R/Python interoperability.

### Git

This project operates using two Git branches

- dev
- main

All development work should be undertaken on the development branch. The dev branch should then be merged into the master branch to deploy a new version of the package. 

### CI/CD

This project uses GitLab CI/CD. There are currently three stages in the CI/CD pipeline

* **test** - Runs any CI/CD tests using [pytest](https://docs.pytest.org).
* **build_deploy_package** - Builds the Python package and deploys to [PyPI](https://pypi.org/).
* **build_deploy_docs** - Builds the documentation site and deploys to [GitLab Pages](https://docs.gitlab.com/ee/user/project/pages/).

The **test** stage runs on every commit. The **build_deploy_package** and **build_deploy_docs** stages only run on commits to the `main` branch. All CI/CD stages run in a Docker container. This project uses `node:latest` for the **build_deploy_docs** stage and a custom R/Python container for the remaining stages.

#### Docker

To update the container in the registry, navigate to the project root and run

```
sudo docker login registry.gitlab.com
```

Enter your GitLab username and password (only for members of the project). Then run

```
sudo docker build -t registry.gitlab.com/tomkimcta/model-validation-framework .
sudo docker push registry.gitlab.com/tomkimcta/model-validation-framework
```

#### PyPI

The version stored in the `version` file must be incremented for a deployment of the package to be successful.

### Documentation

This project uses a static site generator called [Docusaurus](https://docusaurus.io) to create its documentation. The content for the documentation site is contained in `documentation/docs/`. Any updates to documentation can be verified in a development server by running `npm i && npm start` from the `documentation/` directory.

