#!/usr/bin/env python
import os
import sys
import psutil
import pcraster
import pcraster.framework


first_time_step = 1
last_time_step = 100
nr_samples = 20
nr_spinups = 50
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
        self.process = psutil.Process(os.getpid())

    def print_memory_used(self):
        nr_mbytes = self.process.get_memory_info()[0] / 1048576.0
        self.log_file.write("{}\n".format(nr_mbytes))

    def premcloop(self):
        # Mmm, this leaks. Member variables leak, local variables don't.
        self.dummy1 = pcraster.scalar(pcraster.readmap("clone.map")) * 5 * 4 * 3

        # Deleting the instance solves the leak. Why is the instance not
        # deleted once the instance is overwritten?
        # del self.dummy1

    def initial(self):
        pass

    def dynamic(self):
        self.print_memory_used()

    def postmcloop(self):
        pass


for spinup_id in xrange(nr_spinups):
    model = Model("clone.map", log_file)
    print "model (2)", sys.getrefcount(model)
    dynamic_model = pcraster.framework.DynamicFramework(model,
        firstTimestep=first_time_step, lastTimeStep=last_time_step)
    print "model (3)", sys.getrefcount(model)
    print "dynamic_model (2)", sys.getrefcount(dynamic_model)
    dynamic_model.setQuiet(True)
    monte_carlo_model = pcraster.framework.MonteCarloFramework(dynamic_model,
        nrSamples=nr_samples)
    print "model (3)", sys.getrefcount(model)
    print "dynamic_model (3)", sys.getrefcount(dynamic_model)
    print "monte_carlo_model (2)", sys.getrefcount(monte_carlo_model)
    monte_carlo_model.setQuiet(True)
    monte_carlo_model.run()

    del monte_carlo_model
    del dynamic_model
    print "model (2)", sys.getrefcount(model)
    print ""
