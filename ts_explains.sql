

EXPLAIN ANALYZE SELECT *
FROM messages
WHERE to_tsvector('russian', messages.text) @@ to_tsquery( 'russian', 'рай' );

-- BEFORE INDEX
--                                                            QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------------------
-- Gather  (cost=1000.00..197442.36 rows=6642 width=275) (actual time=37.070..6518.188 rows=44760 loops=1)
--   Workers Planned: 2
--   Workers Launched: 2
--   ->  Parallel Seq Scan on messages  (cost=0.00..195778.16 rows=2768 width=275) (actual time=15.712..6439.098 rows=14920 loops=3)
--         Filter: (to_tsvector('russian'::regconfig, (text)::text) @@ '''ра'''::tsquery)
--         Rows Removed by Filter: 428095
-- Planning Time: 0.830 ms
-- JIT:
--   Functions: 6
--   Options: Inlining false, Optimization false, Expressions true, Deforming true
--   Timing: Generation 13.704 ms, Inlining 0.000 ms, Optimization 12.631 ms, Emission 29.876 ms, Total 56.211 ms
-- Execution Time: 6534.349 ms
--(12 rows)
--

-- AFTER INDEX
--                                                                QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------------------------
-- Gather  (cost=1420.21..61767.92 rows=44414 width=275) (actual time=24.001..97.321 rows=44759 loops=1)
--   Workers Planned: 2
--   Workers Launched: 2
--   ->  Parallel Bitmap Heap Scan on messages  (cost=420.21..56326.52 rows=18506 width=275) (actual time=7.906..67.906 rows=14920 loops=3)
--         Recheck Cond: (to_tsvector('russian'::regconfig, (text)::text) @@ '''ра'''::tsquery)
--         Heap Blocks: exact=12636
--         ->  Bitmap Index Scan on ix_tsvector_text  (cost=0.00..409.10 rows=44414 width=0) (actual time=20.078..20.078 rows=44759 loops=1)
--               Index Cond: (to_tsvector('russian'::regconfig, (text)::text) @@ '''ра'''::tsquery)
-- Planning Time: 0.309 ms
-- Execution Time: 98.897 ms
--(10 rows)




EXPLAIN ANALYZE SELECT users.name, users.age, users.about, users.email, users.password, users.last_login, users.id
FROM users
WHERE to_tsvector('russian', name || ' ' || about) @@ to_tsquery('russian', 'Руслан');

-- BEFORE INDEX
--                                                          QUERY PLAN
--------------------------------------------------------------------------------------------------------------------------------
-- Gather  (cost=1000.00..129431.28 rows=4740 width=151) (actual time=27.742..1336.049 rows=1489 loops=1)
--   Workers Planned: 2
--   Workers Launched: 2
--   ->  Parallel Seq Scan on users  (cost=0.00..127957.28 rows=1975 width=151) (actual time=14.920..1278.123 rows=496 loops=3)
--         Filter: (to_tsvector('russian'::regconfig, (((name)::text || ' '::text) || (about)::text)) @@ '''русла'''::tsquery)
--         Rows Removed by Filter: 315507
-- Planning Time: 1.901 ms
-- JIT:
--   Functions: 6
--   Options: Inlining false, Optimization false, Expressions true, Deforming true
--   Timing: Generation 3.987 ms, Inlining 0.000 ms, Optimization 7.763 ms, Emission 17.743 ms, Total 29.494 ms
-- Execution Time: 1339.010 ms
--(12 rows)


-- AFTER INDEX
--                                                             QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------------
-- Bitmap Heap Scan on users  (cost=968.46..3042.24 rows=576 width=150) (actual time=1.564..25.414 rows=945 loops=1)
--   Recheck Cond: (to_tsvector('russian'::regconfig, (((name)::text || ' '::text) || (about)::text)) @@ '''русла'''::tsquery)
--   Heap Blocks: exact=902
--   ->  Bitmap Index Scan on ix_tsvector_name_about  (cost=0.00..968.32 rows=576 width=0) (actual time=1.485..1.485 rows=945 loops=1)
--         Index Cond: (to_tsvector('russian'::regconfig, (((name)::text || ' '::text) || (about)::text)) @@ '''русла'''::tsquery)
-- Planning Time: 1.018 ms
-- Execution Time: 25.565 ms
--(7 rows)
