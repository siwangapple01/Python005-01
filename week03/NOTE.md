学习笔记

本周学习以下重要的点

-   在服务器下载 mysql，安装。
-   通过 python 采用多种方式跟数据进行链接。
-   学会通过 ACID 的原则对事务的特性以及隔离级别以及进行处理方式。
-   深入理解隔离级别的四个方式

作业

#1 第一题:

所涉及代码如下
[client]
default_character_set = utf8mb4

[mysql]
default_character_set = utf8mb4

```
interactive_timeout = 28800
wait_timeout = 28800
max_connections = 1000
character_set_server = utf8mb4
init_connect = 'SET NAMES utf8mb4'
character_set_client_handshake = FALSE
collation_server = utf8mb4_unicode_ci
```

```
show variables like '%chara%';
show variables like 'collation_%';

GRANT ALL PRIVILEGES ON testdb.* TO 'username'@'%' IDENTIFIED by 'password888';
```

#3 第三题
顺序如下所示

```
SELECT DISTINCT player_id, player_name, count(*) as num -->5
FROM player JOIN team ON player.team_id = team.team_id -->1
WHERE height > 1.80 -->2
GROUP BY player.team_id -->3
HAVING num > 2   -->4
ORDER BY num DESC -->6
LIMIT 2 -->7
```

#5 第五题

索引有点像数据结构中的列表 Array, 有较快的查询速度，但是在插入，删除，修改会有一定损耗，且会占用额外的磁盘空间。

基于查询快的特点，以下集中几种情况需要创建索引：

-   聚合的字段，过滤的，排序的字段的情况下需要对对应的字段建立索引

以下下几种情况不需要建立索引

-   数据比较稀疏的字段
-   数据类别比较少的字段（性别，学历等等）
-
