from multiprocessing import Value, Pool
import time

PROCESSES = 10
ITERATIONS = 1000

class dummy:
    counter = Value("i", 0)

def repeat_add(number):
    start = time.perf_counter()
    for _ in range(ITERATIONS):
        with dummy.counter.get_lock():
            dummy.counter.value += 1
    return time.perf_counter() - start

def pool_init(x):
    dummy.counter = x

if _name_ == "_main_":
    # create the shared barrier
    with Pool(PROCESSES, initializer=pool_init, initargs=(dummy.counter, )) as pool:    

        # Pool initialization
        start = time.perf_counter()
        _ = pool.map(range, range(PROCESSES), chunksize=1)
        end = time.perf_counter()
        print("pool map took first time", end - start)

        # Buffer
        for _ in range(10):
            start = time.perf_counter()
            _ = pool.map(range, range(PROCESSES), chunksize=1)
            end = time.perf_counter()

        # Measurement of external times
        normal_external_times = []
        for i in range(10):
            start = time.perf_counter()
            _ = pool.map(range, range(PROCESSES), chunksize=1)
            end = time.perf_counter()
            normal_external_times.append(end-start)
        
        print("pool map light function external times", int(min(normal_external_times)*1e6), int(max(normal_external_times)*1e6))

        assert max(normal_external_times) / min(normal_external_times) < 10, f"external timing {normal_external_times} not consistent"
        print("VERIFIED MULTIPROCESSING POOL TIMINGS ARE CONSISTENT")

        start = time.perf_counter()
        counter_internal_time = pool.map(repeat_add, range(PROCESSES), chunksize=1)
        end = time.perf_counter()
        counter_time = end - start
        assert dummy.counter.value == PROCESSES * ITERATIONS, f"bad counter value, {dummy.counter.value}"
        print("VERIFIED COUNTER IS WORKING CORRECTLY")

        print("pool map counter external time (us)", int((counter_time)*1e6))
        print("counter max internal time (us)", int(max(counter_internal_time)*1e6))
        
        start = time.perf_counter()
        x = sum(1 for _ in range(dummy.counter.value))
        end = time.perf_counter()
        single_process_time = end - start
        assert x == dummy.counter.value, "strange counter failure"
        print("single process time (us)", int((single_process_time)*1e6))
        print("approximate speed factor estimates", 
              int((counter_time - max(normal_external_times)) / single_process_time) , 
              int((counter_time - min(normal_external_times)) / single_process_time), 
              int(max(counter_internal_time) / single_process_time))
