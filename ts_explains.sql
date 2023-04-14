

EXPLAIN ANALYZE SELECT *
FROM messages
WHERE to_tsvector('russian', messages.text) @@ to_tsquery( 'russian', 'рай' );

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


