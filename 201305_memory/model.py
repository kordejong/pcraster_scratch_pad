#!/usr/bin/env python
import os
import psutil
import pcraster
import pcraster.framework


first_time_step = 1
last_time_step = 10
nr_samples = 3
nr_state_variables = 64
nr_spinups = 10
log_file = file("memory.col", "w")


class Model(
    pcraster.framework.DynamicModel,
    pcraster.framework.MonteCarloModel):

    def __init__(self,
            clone_map,
            log_file):
        pcraster.framework.DynamicModel.__init__(self)
        pcraster.framework.MonteCarloModel.__init__(self)
        pcraster.setclone(clone_map)
        self.log_file = log_file
        self.nr_state_variables = nr_state_variables
        self.process = psutil.Process(os.getpid())

    def print_memory_used(self):
        nr_mbytes = self.process.get_memory_info()[0] / 1048576.0
        self.log_file.write("{}\n".format(nr_mbytes))

    def premcloop(self):
        self.dummy = pcraster.scalar(pcraster.readmap("clone.map")) * 5.0

    def initial(self):
        pass

    def dynamic(self):
        # Write state, using unique names.
        names = [pcraster.framework.generateNameST("dummy{}x".format(i),
            self.currentSampleNumber(), self.currentTimeStep()) for i in
                range(1, self.nr_state_variables + 1)]

        # Write state.
        for name in names:
            pcraster.report(self.dummy, name)

        # Read state.
        for name in names:
            pcraster.readmap(name)

        # Remove state.
        for name in names:
            os.remove(name)

        self.print_memory_used()

    def postmcloop(self):
        pass


for spinup_id in xrange(nr_spinups):
    model = Model("clone.map", log_file)
    dynamic_model = pcraster.framework.DynamicFramework(model,
        firstTimestep=first_time_step, lastTimeStep=last_time_step)
    # dynamic_model.setQuiet(True)
    monte_carlo_model = pcraster.framework.MonteCarloFramework(dynamic_model,
        nrSamples=nr_samples)
    # monte_carlo_model.setQuiet(True)
    monte_carlo_model.run()
