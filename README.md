# Improving Carla-RL Project
Forked from [carla-rl-gym/carla-rl](https://github.com/carla-rl-gym/carla-rl), this repo is currently being worked on as an Insight Data Science project (20A.AI). The goal is to reproduce results by seansegal and analyze the difference between the implemented algorithms. Furthermore, REINFORCE (vanilla policy gradient) and SAC (soft actor-critic) may be added to the list.


## Ubuntu Installation and Setup
The Carla simulator requires 2 running processes: Server and Client. The server generates the specifics of the map. The client runs the algorithms and training process.

### Update Nvidia Drivers
To use the nvidia-docker, the machine requires a GPU and updated graphics driver.
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

### CARLA SERVER

#### Build Server
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

For multiple servers instances, it is recommended to use script 
```
server/run_servers.py
```
Start N servers by running,
```
python server/run_servers.py  --num-servers N
```
(You will need GPU ids)
The logs for stdout and stderr will be under `server_output` folder

Servers output `docker logs -ft CONTAINER_ID` follows and tails it.

### CLIENT

#### Build Client
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
(Resume training by using the `--resume-training MODEL_FILE.pth.tar` flag instead)

#### Arguments and Config Files
`client/train.py` script uses both arguments and a configuration file. The configuration file specifies all components of the model. The config file should have everything necessary to reproduce the results of a given model. The arguments of the script deal with things that are independent of the model (for example, how often to create videos or log to Tensorboard)

#### Hyperparameter Tuning
To test a set of hyperparemeters see the `scripts/test_hyperparameters_parallel.py` script. This will let you specify a set of hyperparameters to test different from those specified in the `client/config/base.yaml` file.


## Benchmark Results

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
