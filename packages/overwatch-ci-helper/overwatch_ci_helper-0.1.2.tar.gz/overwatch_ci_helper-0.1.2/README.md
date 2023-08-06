# overwatch-ci-helper

This python package is built to help overwatch during ci builds/tests. It utilizes the docker-py package to manage deploying any number of overwatch microservices during CI testing. It requires you to have a config defined which has information about the image to use, the config for the overwatch microservices and the such.

## Installation

To install the package, install it in the same way anyone install python packages:
```
python3 -m pip install overwatch-ci-helper
```

## Usage

To use the package, simply use it in the following manner:
```
needs model-registry overwatch-server input-server -c PATH/TO/config.yaml --keystores PATH/TO/.dcp
...
...
...

needs model-registry overwatch-server input-server -c PATH/TO/config.yaml --keystores PATH/TO/.dcp --cleanup
```

The first command spins up a model-registry, overwatch-server and an input-server using the config specified and with the keystores given. The second cleans up the spun up docker containers, kills them and removes them from docker. 



