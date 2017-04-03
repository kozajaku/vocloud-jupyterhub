# vocloud-jupyterhub

This repository contains necessary files for building and deploying Jupyterhub service directly integrated 
to Vocloud server. 

## Configuration

At first it is necessary to modify configuration for the currently running environment. 
The only file that must be configured is `.env`. File contains documentation and it should be obvious
what values should be set inside.

## Building

*Note*: In order to build and deploy docker images you will have to have Docker properly installed and have proper 
permissions to call docker commands. To do so you will probably have to switch to **root** user. 

To start building docker images simply execute 

```bash
make
```

in the root directory of this repository. This should setup docker network, volume and start building 
of `jupyter-notebook` and `vocloud-jupyterhub` docker images. 

To save up some time the `jupyter-notebook` image is built only when it was not built previously. 
If you want to force the rebuild execute:

```bash
make notebook_rebuild
```

## Deployment

To trigger docker deployment using a docker-compose tool simply execute

```bash
docker-compose up -d
```

or

```bash
docker-compose up
```

if you want to attach to the docker container input/output.

## Stopping and starting

To stop the `vocloud-jupyterhub` invoke

```bash
docker-compose stop
```

To start it again invoke

```bash
docker-compose start
```

## Removal

To remove all containers from docker execute

```bash
docker-compose down
```

This will not remove neither volumes, nor network, nor images. To remove network execute 

```bash
docker network rm jupyterhub-network
```

*Warning*: Be sure to backup users notebook volumes before removing them from the docker!

To remove jupyterhub volumes at first list all volumes using

```bash
docker volume ls
```

and then delete every jupyterhub volume 

```bash
docker volume rm [volumne-name]
```

where `[volume-name]` is name of the volume listed in the previous command.

To remove docker images at first remove `jupyter-notebook` by invoking

```bash
docker rmi jupyter-notebook
```

and then remove `vocloud-jupyterhub` image by executing

```bash
docker rmi vocloud-jupyterhub
```

*Note:* Names in this guide are the same as an implicit settings inside `.env` environment file.
If you manually change those settings you have to alter the removal commands too.