--размеры таблиц
select pg_size_pretty( pg_total_relation_size('users') );
--362 MB
select pg_size_pretty( pg_total_relation_size('friends') );
--219 MB


--запрос на выборку друзей пользователя, сортировка по количеству друзей
select users.id, name, email, count(friends.friend_id) as friends_count
from users
join friends
on friends.user_id = users.id
group by users.id
order by friends_count desc
limit 1
;


--запрос на выборку друзей пользователя, сортировка по дате последнего логина

EXPLAIN ANALYZE
SELECT users.last_login, users.id, users.name
FROM users
JOIN
(
    select user_id, friend_id
    from friends
    where user_id = 589424
) AS friend
on users.id = friend.friend_id
AS user  -- comment AS user to get not optimal plan :)
ORDER BY last_login DESC
--LIMIT 10
;

--Nested Loop  (cost=0.85..41.81 rows=3 width=26) (actual time=0.162..33.380 rows=8760 loops=1)
--  ->  Index Only Scan using friends_user_id_friend_id_key on friends  (cost=0.43..16.48 rows=3 width=4) (actual time=0.066..6.837 rows=8760 loops=1)
--        Index Cond: (user_id = 589424)
--        Heap Fetches: 8760
--  ->  Index Scan using users_id_last_login_desc_index on users  (cost=0.42..8.44 rows=1 width=26) (actual time=0.003..0.003 rows=1 loops=8760)
--        Index Cond: (id = friends.friend_id)
--Planning Time: 1.073 ms
--Execution Time: 33.822 ms
