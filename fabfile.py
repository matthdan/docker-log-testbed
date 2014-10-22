# -*- coding: utf-8 -*-
#
# Author : Matthieu DANIEL <matth.daniel@gmail.com>
# Some functions to build and run a small docker tested for rsyslog
#

from fabric.api import run, env, task
from fabric.colors import yellow, red
import sys
env.use_ssh_config = True
env.parallel = False
env.hosts = ['localhost']

ContainerList = []


@task
def whoami():
    """
    Information about the container
    """
    uname = run('uname -a', quiet=True)
    fqdn = run('hostname -f', quiet=True)
    print(yellow('Informations : ')+uname)
    print(yellow('FQDN : ')+fqdn)


@task
def getContainerIPWithName(name=None):
    """
    To find the Container IP with its name
    """
    CIP = run('docker inspect -f "{{ .NetworkSettings.IPAddress }}" '+name, quiet=True)
    print(yellow('\n Container : ' + name + ' has the following IP : '+CIP))


@task
def runDns():
    """
    Run the SkyDNS and SkyDock containers to create a complete and simple DNS
    """
    #  Small check to be sure that all the container are available
    global ContainerList
    skydns_check = run(
        "docker images |grep \"crosbymichael/skydns\" |awk '{print $3}'",
        quiet=True)
    skydock_check = run(
        "docker images |grep \"crosbymichael/skydock\" |awk '{print $3}'",
        quiet=True)
    if skydns_check is None:
        print(red('SkyDns container is not present \n' +
                  ' Please solve this trouble before retrying... \n'))
        sys.exit(1)

    if skydock_check is None:
        print(red('SkyDock container is not present \n' +
                  ' Please solve this trouble before retrying... \n'))
        sys.exit(1)

    print(yellow('Starting the DNS server ...'))
    print(yellow('Starting ... SkyDNS ...'))
    skydns_CID = run('docker run -d -p 172.17.42.1:53:53/udp \
                     -p 172.17.42.1:8080:8080 \
                     --name skydns crosbymichael/skydns \
                     --nameserver 8.8.8.8:53 \
                     --domain skydns.local')
    ContainerList.append(skydns_CID)
    print(yellow('Starting ... SkyDock ...'))
    skydock_CID = run('docker run -d -v /var/run/docker.sock:/docker.sock \
                      --name skydock \
                      --link skydns:skydns crosbymichael/skydock \
                      --ttl 30 \
                      --environment dev \
                      --s /docker.sock \
                      --domain skydns.local')
    ContainerList.append(skydock_CID)
    print ContainerList


@task
def runNodes(num=0):
    """
    Start container as nodes
    """
    global ContainerList
    #  Small check to be sure that the container are available
    centos7_check = run(
        "docker images |grep \"matthdan/docker-centos7-evo\" |awk '{print $3}'",
        quiet=True)
    if centos7_check is None:
        print(red('The docker image is not present \n' +
                  ' Please solve this trouble before retrying... \n'))
        sys.exit(1)

    print(yellow('Starting the master node ...'))
    rhel7_master_CID = run('docker run -d --name master \
                           --dns 172.17.42.1 matthdan/docker-centos7-evo')
    ContainerList.append(rhel7_master_CID)

    print(yellow('Starting the compute node ...'))
    for x in range(0, int(num)):
        rhel7_compute_CID = run('docker run -d --name node' + str(x)
                                + ' --dns  172.17.42.1 matthdan/docker-centos7-evo')
        ContainerList.append(rhel7_compute_CID)

    print ContainerList


@task
def runDockerTestBed():
    """
    Run the complete docker testbed from scratch
    """
    #  Pull all the docker images
    print(yellow('Pull all the Docker images'))
    run('docker pull crosbymichael/skydns', quiet=True)
    run('docker pull crosbymichael/skydock', quiet=True)
    run('docker pull matthdan/docker-centos7-evo', quiet=True)
    print(yellow('Complete ...'))

    runDns()
    runNodes(10)