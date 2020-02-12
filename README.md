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
- [Ubuntu Installation for CARLA](#ubuntu-install)
  * [REQUIREMENTS](#requirements)
    + [Clone this Repository](#clone)
    + [Update System & Nvidia Drivers](#nvidia-drivers)
    + [Install Docker, Nvidia-Docker & Docker-Compose](#docker-nvidia-compose)
  * [CARLA DOCKER INSTALLATION](#docker-install)
- [Usage](#usage)
  * [QUICK START](#quick-start)
  * [CURRICULUM LEARNING](#curriculum-learning)
  * [OPTIONAL SETTINGS](#optional-settings)
    + [Server](#server)
    + [Client](#client)
    + [Hyperparameter Tuning](#hyperparameter-tuning)
- [Benchmark Results](#benchmark-results)
  * [VPG](#vpg)
  * [A2C](#a2c)
  * [ACKTR](#acktr)
  * [PPO](#ppo)
  * [On-Policy HER](#her)

<a name="ubuntu-install"></a>
## Ubuntu Installation for CARLA
CARLA requires 2 running processes: *Server* and *Client*. The server generates the map. The client runs the training process.

<a name="requirements"></a>
### REQUIREMENTS

<a name="clone"></a>
#### Clone this Repository
```
git clone https://github.com/JeremyFongSP/carla-rl.git
```

<a name="nvidia-drivers"></a>
#### Update System & Nvidia Drivers
This repo uses nvidia-dockers and requires a GPU with updated graphics drivers.
To update nvidia drivers use:
```
sudo apt update
sudo apt upgrade
ubuntu-drivers list
```
Take note of the available drivers then run:
```
sudo apt install nvidia-driver-DRIVER_NUMBER
```

<a name="docker-nvidia-compose"></a>
#### Install Docker, Nvidia-Docker & Docker-Compose
[Docker](https://docs.docker.com/install/) & [Nvidia-Docker](https://github.com/NVIDIA/nvidia-docker) containers automatically install the required dependencies.

[Docker-Compose](https://docs.docker.com/compose/) automatically starts multiple docker services (server and client), see [QUICK START](#quick-start)

<a name="docker-install"></a>
### CARLA DOCKER INSTALLATION
Change directory `cd ~/carla-rl` *(Note that all paths are relative to this repository)*

Install CARLA using the Docker container from Docker-Hub:
```
docker pull carlasim/carla:0.8.2
```

<a name="usage"></a>
## Usage
<a name="quick-start"></a>
### QUICK START
Start Server and Client simultaneously with standard settings using Docker-Compose:
```
docker-compose run --service-ports carla-client bash
```
This starts the server in the background and starts bash on the client container. To start training, use the command:
```
python client/train.py --config client/config/vpg.yaml --follow-curriculum
```

---

<a name="curriculum-learning"></a>
### Curriculum Learning
To test out the sequencial learning with CL, add the `--follow-curriculum` flag when training, eg:
```
python client/train.py --config client/config/ppo.yaml --follow-curriculum
```

This flag reads the `client/curriculum/curriculum_to_follow.yaml` file where the list of experiments and poses are specified.

---

<a name="optional-settings"></a>
### Optional Settings
Specify desired settings for both server and client:

<a name="server"></a>
#### Server
Build modified CARLA server:
```
docker build server -t carla-server
```
Start Server using nvidia-docker with custom settings, eg:
```
nvidia-docker run --rm -it -p 2000-2002:2000-2002 carlasim/carla:0.8.2 /bin/bash
```

From inside the Docker container, run CARLA with custom settings, eg:
```
./CarlaUE4.sh /Game/Maps/Town01 -carla-server -benchmark -fps=15 -windowed -ResX=800 -ResY=600
```

<a name="client"></a>
#### Client
Build modified CARLA client:
```
docker build client -t carla-client
```
Start Client using nvidia-docker with custom settings, eg:
```
nvidia-docker run -it --network=host -v $PWD:/app carla-client /bin/bash
```

From inside the Docker container, start training agent with custom settings, eg:
```
python client/train.py --config client/config/base.yaml --save-dir outputs/base --starting-port 2000 --follow-curriculum
```

Training requires either `--config [YAML_FILE]` or `--resume-training [.PTH.TAR_FILE]`

Useful flags:
* --save-dir [RELATIVE_OUTPUT_PATH]
* --starting-port [PORT_MATCHING SERVER]
* --video-interval [NUM_EPISODES]
* --follow-curriculum

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
