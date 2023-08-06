# PyConvox
------------------
## Description

A Wrapper application built around convox cli application. This can be modified more to restrict/limit convox access.

------------------

## Requirements

- Python version 3 and above
- Convox cli installed and configured with the key

------------------

## Installation

```sh
#Install Pyconvox using pip package (Only supported python3 and above)
pip install pyconvox
```
------------------

## Usage
```sh
usage: pyconvox [-h] [--version]
                {env,railsconsole,bash,scale,instances,apps,logs,releases,ps}
                ...

pyconvox - a wrapper for the convox application

positional arguments:
  {env,railsconsole,bash,scale,instances,apps,logs,releases,ps}
                        Commands
    env                 list/set env vars
    railsconsole        run rails console
    bash                run bash
    scale               scale of a application
    instances           instances details of the rack
    apps                apps details of the rack
    logs                logs of a service
    releases            releases of a application
    ps                  processes running for application

optional arguments:
  -h, --help            show this help message and exit
  --version, -V         show program's version number and exit
```

### List all the Applications

```sh
usage: pyconvox apps [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### Get environment variables of an application
```sh
pyconvox env -a APPNAME
```
```sh
usage: pyconvox env [-h] [--app APP] [set ...]

positional arguments:
  set                set environment variables KEY=VALUE

optional arguments:
  -h, --help         show this help message and exit
  --app APP, -a APP  application name
```

 - `APPNAME` is the name of the application listed in `pyconvox apps`. 

### Set environment variables to an application
```sh
pyconvox env set VARIABLE=VALUE -a APPNAME
```
```sh
usage: pyconvox env [-h] [--app APP] [--promote PROMOTE] [set ...]

positional arguments:
  set                   set environment variables KEY=VALUE

options:
  -h, --help            show this help message and exit
  --app APP, -a APP     application name
  --promote PROMOTE, -p PROMOTE
                        add "-p 1" at the end if you want to promote the change

```

 - `VARIABLE` is the name of the environment variable.
 - `VALUE` is the value of the environment variable.
 - `APPNAME` is the name of the application listed in `pyconvox apps`. 


### Get into Rails console of the application

```sh
pyconvox railsconsole -a APPNAME
          or 
pyconvox railsconsole -s SERVICE -a APPNAME
```
```sh
usage: pyconvox railsconsole [-h] [--app APP] [--service SERVICE]

optional arguments:
  -h, --help            show this help message and exit
  --app APP, -a APP     application name
  --service SERVICE, -s SERVICE
                        Service name
```

 - `APPNAME` is the name of the application listed in `pyconvox apps`. 
 - `SERVICE` is the name of the service listed in `pyconvox scale -a APPNAME`.


### Get into Bash console of the application

```sh
pyconvox bash -a APPNAME
          or 
pyconvox bash -s SERVICE -a APPNAME
```
```sh
usage: pyconvox bash [-h] [--app APP] [--service SERVICE]

optional arguments:
  -h, --help            show this help message and exit
  --app APP, -a APP     application name
  --service SERVICE, -s SERVICE
                        Service name
```

 - `APPNAME` is the name of the application listed in `pyconvox apps`. 
 - `SERVICE` is the name of the service listed in `pyconvox scale -a APPNAME`.

### Get Count,CPU and Memory of all the services/workers of an application

```sh
pyconvox scale -a APPNAME
```
```sh
usage: pyconvox scale [-h] [--app APP]

optional arguments:
  -h, --help         show this help message and exit
  --app APP, -a APP  application name
```

 - `APPNAME` is the name of the application listed in `pyconvox apps`. 


### Get currently running services/workers of an application

```sh
pyconvox ps -a APPNAME
```
```sh
usage: pyconvox ps [-h] [--app APP]

optional arguments:
  -h, --help         show this help message and exit
  --app APP, -a APP  application name
```

 - `APPNAME` is the name of the application listed in `pyconvox apps`. 

### Get Count,CPU and Memory of all the Instances

```sh
pyconvox instances
```
```sh
usage: pyconvox instances [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### Get release details of an application

```sh
pyconvox releases -a APPNAME
```
```sh
usage: pyconvox releases [-h] [--app APP]

optional arguments:
  -h, --help         show this help message and exit
  --app APP, -a APP  application name
```

 - `APPNAME` is the name of the application listed in `pyconvox apps`. 


### Stream current logs of an application

```sh
pyconvox logs -a APPNAME
```
```sh
usage: pyconvox logs [-h] [--app APP]

optional arguments:
  -h, --help         show this help message and exit
  --app APP, -a APP  application name
```

 - `APPNAME` is the name of the application listed in `pyconvox apps`. 


### Help of pyconvox

```sh
usage: pyconvox [--help|-h]

optional arguments:
  -h, --help  show this help message and exit
```


### Version of pyconvox

```sh
usage: pyconvox [--version|-V]

optional arguments:
  -h, --help  show this help message and exit
```

