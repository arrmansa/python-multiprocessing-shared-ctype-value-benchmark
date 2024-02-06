# What this does
[multiprocessing.Value](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Value) can be used to create a counter that works across processes and is decently performant. This repository is an attempt to measure it.

# Steps
1. Create a process pool
2. Initialize it by running some computationally light load
3. Run more light load until the system (processor clock speed etc.) 'adapts' to the this load.
4. Run more light load and time them to see the pool overhead.
5. Run the actual counter function, time it internally and externally
6. Calculate speed factor differences
