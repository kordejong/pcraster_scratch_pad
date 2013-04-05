#!/usr/bin/env python
import os
import numpy
import psutil
import pcraster
import pcraster.framework


# User writes 10 scalar values for 10 variables for 10000 timesteps
# for 500 samples: 500.000.000 values.
# During post-processing, reading these values back in takes ages.

first_time_step = 1
last_time_step = 5000 # 10000
nr_samples = 250 # 500
nr_state_variables = 10
nr_locations_to_write = 10


class Model(
    pcraster.framework.DynamicModel,
    pcraster.framework.MonteCarloModel):

    @staticmethod
    def generate_name(
            variable_id,
            sample_nr,
            timestep):
        return "{}/state{}_{}".format(sample_nr, variable_id, timestep)

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
        self.memory_log_file = file("memory.col", "w")
        self.runtime_log_file = file("runtime.col", "w")

    def log_memory_used(self):
        nr_mbytes = self.process.get_memory_info().rss / 1048576.0
        self.memory_log_file.write("{}\n".format(nr_mbytes))

    def log_time_spent(self):
        # System + user.
        cpu_time = sum(self.process.get_cpu_times())
        self.runtime_log_file.write("{}\n".format(cpu_time))

    def log_process_statistics(self):
        self.log_memory_used()
        self.log_time_spent()

    def premcloop(self):
        pass

    def initial(self):
        pass

    def dynamic(self):
        # Per state variable a file with nr_locations_to_write values.
        for i in xrange(1, self.nr_state_variables + 1):
            filename = Model.generate_name(i, self.currentSampleNumber(),
                self.currentTimeStep())
            file(filename, "w").write("\t".join([str(i) for i in xrange(
                self.nr_locations_to_write)]))
            self.log_process_statistics()

    def postmcloop(self):
        for i in xrange(1, self.nr_state_variables + 1):
            output = []
            for timestep in xrange(1, self.nrTimeSteps() + 1):
                all_samples = []
                for sample_nr in xrange(1, self.nrSamples() + 1):
                    filename = Model.generate_name(i, sample_nr, timestep)
                    array = numpy.loadtxt(filename)
                    all_samples.append(array)
                    self.log_process_statistics()
                output.append(all_samples)
            output_as_array = numpy.array(output)


model = Model("clone.map", nr_state_variables, nr_locations_to_write)
dynamic_model = pcraster.framework.DynamicFramework(model,
    firstTimestep=first_time_step, lastTimeStep=last_time_step)
dynamic_model.setQuiet(True)
monte_carlo_model = pcraster.framework.MonteCarloFramework(dynamic_model,
    nrSamples=nr_samples)
monte_carlo_model.run()
