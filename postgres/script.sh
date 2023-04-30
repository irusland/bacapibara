#!/usr/bin/env bash

docker network inspect bacapibara_backend | grep Subnet

docker exec -it bacapibara_db_1 bash
psql -U irusland -d postgres
SELECT pg_reload_conf();

docker exec -it bacapibara_db_2_1 bash
psql -U irusland -d postgres
SELECT pg_reload_conf();


docker restart bacapibara_db_2_1 bacapibara_db_1

rm -r postgres/db_2/*
docker exec -it bacapibara_db_2_1 bash
su - postgres -c "pg_basebackup --host=bacapibara_db_1 --username=irusland --pgdata=/var/lib/postgresql/data --wal-method=stream --write-recovery-conf -P"


# CHECK REPLICATION
docker exec -it bacapibara_db_2_1 bash
psql -U irusland -d postgres
select * from pg_stat_wal_receiver;

docker exec -it bacapibara_db_1 bash
psql -U irusland -d postgres
SELECT pid,usename,application_name,state,sync_state FROM pg_stat_replication;
