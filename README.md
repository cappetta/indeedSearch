# indeedSearch

The goal of this project is to pull enormous amounts of data from Indeed via Job Search Queries.  To do that, I've
created a solution which leverages a long list of postal codes and queries the API's for a specific search term.  The
YAML driven config allows you to create dynamically defined script yet this is still under development.

In the current state this script is single-threaded and total time to iterate through all postal codes takes a while per
query but the results are saved as JSON in a local file.

v2 is under development and introduces multi-threading to increase performance.  Writing to files becomes a bit tricker
with multi-threading therefore a local queue will be implemented to bottleneck the file i/o.  v2 might morf into a
distributed queing solution via rabbitmq, redis, or kafka.