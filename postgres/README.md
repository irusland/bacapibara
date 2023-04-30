# HW 10

## start
```shell
docker-compose up -d --force-recreate db db_2
```


## check subnet and slave ip

```shell
docker network inspect bacapibara_backend | grep Subnet
docker network inspect bacapibara_backend
```

## apply config
```shell
./config.sh
```

## restart
```shell
docker restart bacapibara_db_2_1 bacapibara_db_1
```

## on slave: remove pgdata and start replication

```shell
pg_basebackup --host=bacapibara_db_1 --username=irusland --pgdata=/var/lib/postgresql/data --wal-method=stream --write-recovery-conf -P
```

## checking backup processes
```commandline
postgres=# SELECT pid,usename,application_name,state,sync_state FROM pg_stat_replication;
 pid | usename  | application_name | state  | sync_state 
-----+----------+------------------+--------+------------
 615 | irusland | pg_basebackup    | backup | async
(1 row)
```

## see tables on slave

```commandline
postgres=# \dt
          List of relations
 Schema |   Name   | Type  |  Owner   
--------+----------+-------+----------
 public | chats    | table | irusland
 public | friends  | table | irusland
 public | messages | table | irusland
 public | users    | table | irusland
```

## see replication logs 

```shell
2023-04-30 13:39:01.318 UTC [28] LOG:  checkpoint starting: force wait
2023-04-30 13:39:06.859 UTC [28] LOG:  checkpoint complete: wrote 50 buffers (0.3%); 0 WAL file(s) added, 0 removed, 2 recycled; write=5.455 s, sync=0.009 s, total=5.542 s; sync files=38, longest=0.009 s, average=0.001 s; distance=32768 kB, estimate=32768 kB
```
