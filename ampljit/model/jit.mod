/**
 * A computational server must plan the execution of `n` batches on a single-processor machine, where `n` > 0.
 * Each batch may take a different amount `m` of minutes, where `m > 0`. For simplicity, each item in `m` must
 * be an integer value.
 * The execution sequence `1, 2, ..., n` is given and can't be changed.
 * There can't be any temporal overlapping between the batches.
 * For each batch, the desired delivery time is known.
 * The delivery of the computed batches must be as on time as possible: a fixed fee must be paid
 * for each minute early or late.
 */

# set declarations
set BATCH; # set where each item maps to a single program

# param declarations
param duration{BATCH};        # duration of each program
param expected_finish{BATCH}; # time each program should take to complete
param wrong_time_fee;         # dollars to pay for each program result that
                              # isn't computed in exactly the estimated time

# variable declarations
var start_time{BATCH}; # starting time of each program
var delta_time{BATCH}; # quantity of time wrong with respect to expected arrival

# objective function
# minimize the fixed fee to pay for each computation started either early or late
minimize total_fee:
         wrong_time_fee * sum{b in BATCH} delta_time[b];

# wrong delta time is at least the exact wrong time.
# This is a linearization of a modulo equation
s.t. delta_time_abs_1{b in BATCH}:
     delta_time[b] >= - expected_finish[b] + (start_time[b] + duration[b]);
s.t. delta_time_abs_2{b in BATCH}:
     delta_time[b] >= + expected_finish[b] - (start_time[b] + duration[b]);