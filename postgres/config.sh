#!/usr/bin/env bash

docker cp ./pg_hba_main.conf bacapibara_db_1:/var/lib/postgresql/data/pg_hba.conf
docker cp ./pg_hba_follower.conf bacapibara_db_2_1:/var/lib/postgresql/data/pg_hba.conf
docker cp ./postgresql.conf bacapibara_db_1:/var/lib/postgresql/data/postgresql.conf
