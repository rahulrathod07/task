# Python Version
python3 --version
Python 3.9.2

# Install Requirements
pip install -r requirements.txt

# Postman Collection Usage
1. Login as admin/user
2. Set postman environment variable x-access-token from the login response
3. Use other APIs

# Scaling Suggestions
* As of now my database is hosted on db4free.net which is free and does not give faster execution of query, so I will use those servers whose query execution speed is faster for my database.
* For now, my application has a less amount of metadata about movies but when the size of metadata increases at that time I can use multiple servers to handle tons of requests which comes from clients and for that I will use load balancer which will handle the load receiving from clients and according to number of requests load balancer will divide requests to be handled by each server.
* But we also want that when the load decreases our server should be released automatically. So how we can automate the increase and decrease of server that I haven’t figured out yet.
* When metadata of movies will increase then the searching of movie from whole database will be difficult because we must compare with each value of database. So, for that I can use sorting of data by director name, movie name, popularity and imdb score and then I can apply binary search on sorted data which will reduce number of comparisons.
* Because of lots of data in database it is not possible show all the results on single page so to over come that I can use pagination concept in which we can decide that a single page can contain maximum what amount of data and if client want more data then they to send request again for next data which will be shown on next page.
* In worst case my database might crash due to some technical issues so for that, I can use database replication concept in which I can replicate my database in other system so whenever situation like this occurs, I can use replicated database for temporary purpose.
