docker-log-testbed
==================

Distributed log testbed docker based

This package is only for testing/debugging purpose

Requirements:
--------------

* Docker
* Fabric

HOWTO:
------

At this step, nothing is totally exploitable.

For testing, run :

By default Host=localhost

```
$ fab runDockerTestBed
$ fab getContainerIPWithName:master
[localhost] Executing task 'getContainerIPWithName'

 Container : master has the following IP : 172.17.0.8

Done.
Disconnecting from localhost... done.

$ ssh root@172.17.0.8 

```

Install ping or fping tool and from the master container

```
-bash-4.2# for i in {0..9}; do fping node$i.docker-centos7-evo.dev.skydns.local; done
node0.docker-centos7-evo.dev.skydns.local is alive
node1.docker-centos7-evo.dev.skydns.local is alive
node2.docker-centos7-evo.dev.skydns.local is alive
node3.docker-centos7-evo.dev.skydns.local is alive
node4.docker-centos7-evo.dev.skydns.local is alive
node5.docker-centos7-evo.dev.skydns.local is alive
node6.docker-centos7-evo.dev.skydns.local is alive
node7.docker-centos7-evo.dev.skydns.local is alive
node8.docker-centos7-evo.dev.skydns.local is alive
node9.docker-centos7-evo.dev.skydns.local is alive

```

10 containers are pingable from the master container.

To be continued...