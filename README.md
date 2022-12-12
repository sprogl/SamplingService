# Sampling Service:
Implement a stream sampling service in Python.

The /add endpoint of the service should accept a single integer number.

The /sample10 endpoint of the service should return an array with 10 numbers picked at random with equal probability from all numbers which have been added through the /add endpoint so far.

Whereas you're free to use any wide-spread web app framework (Flask, FastAPI, etc.), please provide your own implementation of the sampling logic.

Along with your implementation of the service, please supply a client script which would help demonstrating that the sampling logic is working.

Make sure we can run/test your solution using Docker.

What is the algorithmic and memory complexity of the /add and /sample10 endpoints? Suggest possible future improvements of your solution, especially for production cases with high loads.

Please make sure your solution is not publicly accessible, i.e., do not push it to a public Github repository or similar.

# `install` script:
To load the docker containers, run the install command via
```
sudo bash install
```
This script
1- makes a docker image from the contents inside the "app" directory,
2- loads the container,
3- downloads and loads the mongodb container,
4- runs a test over the application.

# API:
The endpoint 'add' expects a json post request with the following format:
```
{ "number" : some integer }
```
e.g. '{ "number" : 10 }'

The 'sample10' endpoint get request and responds successful requests with a json with the following format:
 ```
{ "success" : True, "samples" : a list of length 10 }
```
e.g. '{ "success" : True, "samples" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] }'
an unsuccessful request is responded with the following json:
 ```
{ "success" : False, "samples" : [] }
```
# `client` script:
The client script implements the adding/sampling functionality.

The client script assumes that the containers were loaded via 'docker-compose' command, i.e., the web server is listening on the ip address 172.20.0.2.

To add a number to the pool, run
```
./client add num
```
where num is the integer to be added to the pool.

To get 10 samples from the pool, run
```
./client sample10
```

# Complexities:
The `/add` endpoint complexty is O(n) and uses O(n) bytes of memory.
The `/sample10` endpoint complexity is O(1) and uses O(n) bytes of memory.

Ofcourse, the memory usage is suboptimal and can be improved by changing the database calls and structure.
This can be achieved by sending the numbers into a table with unique entry column and calling the samples by row number instead of loading the whole pool and do the sampling inside the program (which is what it is doing in the current version). Redis is seamingly also a good alternative for the traditional relational databses in such improvement. Therefore, I would replace MongoDB with either Redis or PostgreSQL in the code.

