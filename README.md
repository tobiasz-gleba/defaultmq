# defaultmq
Defaultmq is REST based message queue witch any database as a storage.

# TODO 
1. scheduled emiter
2. auth using db user
3. docs
4. factory for cache
5. better settings
6. SQL, mongo, cassandra support
7. azure tabele, big query, amazon
8. helm chart
9. open telemetry support


1. get all scheduled items
2. get next exectution time from last_exec
3. if time > next_exec
4. reserve id in cache
5. emite event to queue
6. save next_exectution_time to last_exec
7. delete cache reservation