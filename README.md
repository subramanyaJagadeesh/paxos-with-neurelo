```markdown
# Paxos With Neurelo

This project implements Multi-Decree-Paxos (based on the paper - Paxos Made Moderately Complex, By Robbert van Renesse).

## Paxos:
Paxos is a consensus protocol for distributed systems. It ensures that multiple nodes (servers or processes) in a distributed system can agree on a single value, even in the face of failures like network partitions or node crashes.

## Problem:
The paper implements the Paxos Algorithm while creating a message queue in memory for each server, while this is okay for a local implementation, where all servers are run in a stable machine, if we deploy this code to be run on servers which crash due to some reason, the messages stored in the in-memory queue will get lost forever.

## Solution:
Instead of storing all PaxosMessages in memory, we create a table in a remote PostgreSQL instance, and use the table like a queue. When we insert a message to the table, we add a timestamp of the message. While retrieving a message for a server, we find the oldest message in the table for a destination server, remove it from the table and return it to the server.

## Enter Neurelo:
While the remote database is ready with all its pieces, we need APIs to get and put data in the database, so we add the database instance in Neurelo's dashboard, then add our schema in the definitions, create our custom queries to pop and push data into the database. Lastly, just call the APIs created for us with just a click of few buttons in our Paxos implementation! This saves us a lot of time!

## Optimization:
If the table is filled with many messages, then reads will start getting slower, to fix this we add an index to the table with 2 columns, destination and timestamp, since these are our main columns for us to pop the data.

## Future Work:
Currently, all the messages are pushed and popped from a single table, while this is fine for a small number of servers and requests, it can inundate the table with a lot of messages as the server numbers requests grow. So, we need to create a separate table for each role of a server in the Paxos protocol.
```