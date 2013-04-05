#!/usr/bin/env python
import os
import psutil
import pcraster
import pcraster.framework


# User writes 10 scalar values for 10 variables for 10000 timesteps
# for 500 samples: 500.000.000 values.
# During post-processing, reading these values back in takes ages.

first_time_step = 1
last_time_step = 100 # 10000
nr_samples = 50 # 500
nr_state_variables = 10
nr_locations_to_write = 10


class Model(
    pcraster.framework.DynamicModel,
    pcraster.framework.MonteCarloModel):

    def __init__(self,
            clone_map,
            nr_state_variables,
            nr_locations_to_write):
        pcraster.framework.DynamicModel.__init__(self)
        pcraster.framework.MonteCarloModel.__init__(self)
        pcraster.setclone(clone_map)
        self.nr_state_variables = nr_state_variables
        self.nr_locations_to_write = nr_locations_to_write
        self.process = psutil.Process(os.getpid())
        self.log_file = file("memory_report.col", "w")

    def print_memory_used(self):
        nr_mbytes = self.process.get_memory_info()[0] / 1048576.0
        self.log_file.write("{}\n".format(nr_mbytes))

    def generate_name(self,
            variable_id):
        return "{}/state{}_{}".format(self.currentSampleNumber(), variable_id,
            self.currentTimeStep())

    def premcloop(self):
        pass

    def initial(self):
        pass

    def dynamic(self):
        # Per state variable a file with nr_locations_to_write values.
        for i in xrange(1, self.nr_state_variables + 1):
            filename = self.generate_name(i)
            file(filename, "w").write(", ".join([str(i) for i in xrange(
                self.nr_locations_to_write)]))

        self.print_memory_used()

    def postmcloop(self):
        pass


model = Model("clone.map", nr_state_variables, nr_locations_to_write)
dynamic_model = pcraster.framework.DynamicFramework(model,
    firstTimestep=first_time_step, lastTimeStep=last_time_step)
dynamic_model.setQuiet(True)
monte_carlo_model = pcraster.framework.MonteCarloFramework(dynamic_model,
    nrSamples=nr_samples)
monte_carlo_model.run()
