# Improving Carla-RL Training with Curriculum Learning
Forked from [carla-rl-gym/carla-rl](https://github.com/carla-rl-gym/carla-rl). This project was done at Insight Data Science in January 2020 (20A.AI.SV). The goal is to reproduce results obtained by [seansegal](https://github.com/seansegal), analyze differences between algorithms and implement curriculum learning (CL). 

__Additions to the original repo__
* Vanilla Policy Gradient algorithm (VPG) added for benchmarking
* Curriculum learning wrapper implemented to original code (run with `--follow-curriculum` flag)
* Docker-compose file created for quick start

__Future work__
* Implement Imitation Learning
* Implement SAC to see improvement and then train with CL

### Contents
- [Ubuntu Requirements](#ubuntu-requirements)
  * [Clone this Repository](#clone)
  * [Update System & Nvidia Drivers](#nvidia-drivers)
  * [Install Docker, Nvidia-Docker & Docker-Compose](#docker-nvidia-compose)
  * [Carla Docker Setup](#docker-setup)
- [Usage](#usage)
  * [Quick Start](#quick-start)
  * [Curriculum Learning](#curriculum-learning)
  * [Optional Settings](#optional-settings)
    + [Server](#server)
    + [Client](#client)
    + [Multiple Instances](#multiple-instances)
    + [Hyperparameter Tuning](#hyperparameter-tuning)
- [Benchmark Results](#benchmark-results)
  * [VPG](#vpg)
  * [A2C](#a2c)
  * [ACKTR](#acktr)
  * [PPO](#ppo)
  * [On-Policy HER](#her)

<a name="ubuntu-requirements"></a>
## Ubuntu Requirements
It is recommended to run this on a cloud computing platform such as AWS EC2.
Installing everything including all dependencies will require:
 * __80GB__  of disk space
 * Nvidia GPU
 * 10-20 minutes

<a name="clone"></a>
### 1. Clone this Repository
```
git clone https://github.com/JeremyFongSP/carla-rl.git
```

<a name="nvidia-drivers"></a>
### 2. Update System & Nvidia Drivers
This repo uses nvidia-dockers and requires a GPU with updated graphics drivers.
To update nvidia drivers use:
```
sudo apt update
sudo apt upgrade
ubuntu-drivers list
```
Take note of the available drivers then run:
```
sudo apt install nvidia-DRIVER_NUMBER
```

<a name="docker-nvidia-compose"></a>
### 3. Install Docker, Nvidia-Docker & Docker-Compose
[Docker](https://docs.docker.com/install/) & [Nvidia-Docker](https://github.com/NVIDIA/nvidia-docker) containers automatically install the required dependencies.

[Docker-Compose](https://docs.docker.com/compose/) automatically starts multiple docker services (server and client)

<a name="docker-setup"></a>
### 4. Carla Docker Setup
CARLA requires 2 running processes: *Server* and *Client*

Change directory `cd ~/carla-rl` *(Note that all paths are relative to this repository)*

Install CARLA using the Docker container from Docker-Hub:
```
docker pull carlasim/carla:0.8.2
```
Install modified Server & Client using:
```
docker-compose up -d
```

<a name="usage"></a>
## Usage
<a name="quick-start"></a>
### Quick Start
 1. Start Server and Client simultaneously with standard settings using Docker-Compose:
```
docker-compose run --service-ports carla-client bash
```
This starts the server in the background and starts bash on the client container. 

2. When the terminal user changes to root (this is within the container), start training with CL, using:
```
python client/train.py --config client/config/vpg.yaml --follow-curriculum
```

---

<a name="curriculum-learning"></a>
### Curriculum Learning
To test out the sequential learning with CL, add the `--follow-curriculum` flag when training

This flag reads the `client/curriculum/curriculum_to_follow.yaml` file where the list of experiments and poses are specified.

---

<a name="optional-settings"></a>
### Optional Settings
<a name="server"></a>
#### Server
 1. Start server container with:
```
nvidia-docker run --rm -it -p 2000-2002:2000-2002 carlasim/carla:0.8.2 /bin/bash
```

 2. From inside the container, execute:
```
./CarlaUE4.sh /Game/Maps/Town01 -carla-server -benchmark -fps=15 -windowed -ResX=800 -ResY=600
```
Possible changes:
* Port number (-p [PORT_NUMBER])
* Town01 or Town02
* Output Frame per second (set -fps=[FPS])
* Windowed (omit for full screen)
* Output Resolution

<a name="client"></a>
#### Client
 3. Start client container with:
```
nvidia-docker run -it --network=host -v $PWD:/app carla-client /bin/bash
```
 4. From inside the container, execute:
```
python client/train.py --config client/config/vpg.yaml
```
Useful flags:
* --config [YAML_FILE]  or  --resume-training [.PTH.TAR_FILE]
* --save-dir [RELATIVE_OUTPUT_PATH]
* --starting-port [PORT_MATCHING SERVER]
* --video-interval [NUM_EPISODES]
* --follow-curriculum

<a name="multiple-instances"></a>
#### Multiple Instances

To run multiple instances, open two new terminal and start client/server with the following modifications:
 1. Change the server port from `2000-2002:2000-2002` to eg: `4000-4002:2000-2002`
 2. Specify the matching *--starting-port* flag for the client, eg: `--starting-port 4000`
 
 (Using tmux is a convenient way to avoid opening too many terminals)

<a name="hyperparameter-tuning"></a>
#### Hyperparameter Tuning
To test a set of hyperparemeters, see the `scripts/test_hyperparameters_parallel.py` script. This allows you to specify a set of hyperparameters to test different from `client/config/base.yaml` config files.

<a name="benchmark-results"></a>
## Benchmark Results

<a name="vpg"></a>
### VPG
To reproduce this repo's results, run a CARLA server and inside the `carla-client` docker run,
`python client/train.py --config client/config/vpg.yaml`

<a name="a2c"></a>
### A2C
To reproduce seansegal's results, run a CARLA server and inside the `carla-client` docker run,
`python client/train.py --config client/config/a2c.yaml`

<a name="acktr"></a>
### ACKTR
To reproduce seasegal's results, run a CARLA server and inside the `carla-client` docker run,
`python client/train.py --config client/config/acktr.yaml`

<a name="ppo"></a>
### PPO
To reproduce seansegal's results, run a CARLA server and inside the `carla-client` docker run,
`python client/train.py --config client/config/ppo.yaml`

<a name="her"></a>
### On-Policy HER
To reproduce seansegal's results, run a CARLA server and inside the `carla-client` docker run,
`python client/train.py --config client/config/her.yaml`
