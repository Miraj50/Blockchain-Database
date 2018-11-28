Schema of instructor credentials table
--------------------------------------
+-------+--------------+------+-----+
| Field | Type         | Null | Key |
+-------+--------------+------+-----+
| uid   | varchar(128) | NO   | PRI |
| salt  | varchar(64)  | YES  |     |
| hash  | varchar(64)  | YES  |     |
+-------+--------------+------+-----+

Schema of grades table
----------------------
+------------+--------------+------+-----+
| Field      | Type         | Null | Key |
+------------+--------------+------+-----+
| uid        | varchar(128) | NO   | PRI |
| course     | varchar(10)  | NO   | PRI |
| grade      | varchar(2)   | YES  |     |
| txid       | varchar(64)  | YES  |     |
| identifier | varchar(128) | YES  |     |
+------------+--------------+------+-----+



Commands for Multichain:
------------------------
<!-- Start Node -->
$ multichain-util create chain1
$ multichaind chain1 -daemon
<!-- Create Streams -->
$ create stream stream1 false
$ subscribe stream1
$ create stream pubkey false
$ subscribe pubkey
$ create stream instructor false
$ subscribe instructor
<!-- Publish the courses of instructors -->
$ publish instructor ss 6373333137 <!-- Course is hex encoded -->
$ publish instructor ss 6373333837
$ publish instructor puru 6373333837
