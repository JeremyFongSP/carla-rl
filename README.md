# Improving Carla-RL Training with Curriculum Learning
This project is forked from [carla-rl-gym/carla-rl](https://github.com/carla-rl-gym/carla-rl). This repo is currently being worked on as an Insight Data Science project (20A.AI). The goal is to reproduce results by seansegal, to analyze the difference between the implemented algorithms and to implement curriculum learning (CL) for faster training. 

### Additions to the original repo
* The Vanilla Policy Gradient algorithm (VPG) was added for benchmarking
* Curriculum learning implemented to original code (run with `--follow-curriculum` flag)

### Future work
* Implement SAC to see improvement and then train with CL
* Implement Imitation Learning

## Ubuntu Installation and Setup for CARLA
The Carla simulator requires 2 running processes: __Server__ and __Client__. 
The server generates the specifics of the map. The client runs the algorithms and training process.

### Update Nvidia Drivers
The setup required nvidia-docker to run both server and client.
To use the nvidia-docker, a GPU is required with updated graphics driver.
To update Nvidia drivers use,
```
sudo apt update
sudo apt upgrade
ubuntu-drivers list
```
Take note of the available drivers then run,
```
sudo apt install nvidia-driver-DRIVER_NUMBER
```

### SERVER

#### Build Server (one time)
Install CARLA using the Docker container by running,
```
docker pull carlasim/carla:0.8.2
```

Build modified CARLA server using Docker by running,
```
docker build server -t carla-server
```

#### Running CARLA server
Next, run Docker container with,
```
nvidia-docker run --rm -it -p 2000-2002:2000-2002 carlasim/carla:0.8.2 /bin/bash
```

Inside the Docker container, run server with,
```
./CarlaUE4.sh /Game/Maps/Town01 -carla-server -benchmark -fps=15 -windowed -ResX=800 -ResY=600
```

The logs for stdout and stderr will be under `server_output` folder

Servers output `docker logs -ft CONTAINER_ID` follows and tails it.

### CLIENT

#### Build Client (one time)
Code requires:
* Python 3
* PyTorch
* OpenAI Gym (v 0.10.8)
* OpenAI Baselines

Build modified CARLA client using Dockerfile with,
```
docker build client -t carla-client
```

#### Running CARLA client (training code, benchmark code)
To run the client,
```
nvidia-docker run -it --network=host -v $PWD:/app carla-client /bin/bash
```
(`--network=host` flag allows the Docker container to make requests to the server)

Inside the Docker container, run scripts using for example,
```
python client/train.py --config client/config/base.yaml
```
See list of arguments below

#### Config Files and Arguments
`client/train.py` requires either `--config [YAML_FILE]` or `--resume-training [.PTH.TAR_FILE]`

*(Note that all paths are relative to this repository's path)*

Useful flags:

`--save-dir [OUTPUT_PATH]`
`--starting-port [PORT]`
`--video-interval [NUM_EPISODES]`
`--follow-curriculum`

#### Hyperparameter Tuning
To test a set of hyperparemeters see the `scripts/test_hyperparameters_parallel.py` script. This will let you specify a set of hyperparameters to test different from those specified in the `client/config/base.yaml` file.

## Curriculum Learning
To test out the sequencial learning with CL, add the `--follow-curriculum` flag when launching train.py eg,
```
python client/train.py --config client/config/ppo.yaml --follow-curriculum
```

This flag reads the `client/curriculum/curriculum_to_follow.yaml` file. This is where the list of experiments and poses are specified.

## Benchmark Results

### VPG
To reproduce this repo's results, run a CARLA server and inside the `carla-client` docker run,
`python client/train.py --config client/config/vpg.yaml`

### A2C
To reproduce seansegal's results, run a CARLA server and inside the `carla-client` docker run,
`python client/train.py --config client/config/a2c.yaml`

### ACKTR
To reproduce seasegal's results, run a CARLA server and inside the `carla-client` docker run,
`python client/train.py --config client/config/acktr.yaml`

### PPO
To reproduce seansegal's results, run a CARLA server and inside the `carla-client` docker run,
`python client/train.py --config client/config/ppo.yaml`

### On-Policy HER
To reproduce seansegal's results, run a CARLA server and inside the `carla-client` docker run,
`python client/train.py --config client/config/her.yaml`
