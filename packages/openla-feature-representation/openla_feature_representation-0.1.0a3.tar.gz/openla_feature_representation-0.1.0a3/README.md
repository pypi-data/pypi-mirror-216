# openla-feature-representation: generate features EventStream data

## Introduction

openla-feature-representation is an open-source Python module that generates features from [OpenLA](https://limu.ait.kyushu-u.ac.jp/~openLA/) EventStream data to make the data easier to use for ML.

## Installation

Until this module is available on PyPI or as a release on the GitHub repository, we recommend building a wheel using [poetry](https://python-poetry.org/) and installing that file using `pip`:

```sh
poetry build
pip install dist/openla_feature_representation-0.1.0-py3-none-any.whl
```

## Usage

This is how to call the constructor:

```py
E2Vec(fT_model_path, EduData, course_id)
```

- `fT_model_path` is the path to a fastText language model trained for this task
- `EduData` is the path to a directory with the dataset (see below)
- `course_id` is a string to identify files for the course to analyze within the `EduData` directory

After that, all methods the class provides can be used.

## Datasets for OpenLA

This module uses data in the same format as OpenLA. Please refer to the [OpenLA documentation](https://limu.ait.kyushu-u.ac.jp/~openLA/) for further information.
