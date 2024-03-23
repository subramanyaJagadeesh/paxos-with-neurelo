# paxos-with-neurelo
This project implements Multi-Decree-Paxos (based on the paper - Paxos Made Moderately Complex, By Robbert van Renesse) with a twist, i.e instead of storing all PaxosMessages in memory, it stores and retrieves the messages in a remote queue table in PostgresQL instance while leveraging Neurelo's Cloud API. 

The reason for using a remote storage to store messages is to fault-tolerant implementation of the paxos algorithm, i.e even if some acceptors, replicas and leaders fail, the messages will still be available for them if and when they come back up.
