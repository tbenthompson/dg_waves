import controller
import viscosaur as vc
import defaults
import numpy as np

# Set up the parameters to be used.
params = defaults.default_params()
params['min_corner_x'] = -5.0
params['min_corner_y'] = -5.0
params['max_corner_x'] = 5.0
params['max_corner_y'] = 5.0
params['t_max'] = 5.0
params['time_step'] = params['t_max'] / 250.0
params['test_output'] = False
params['num_threads'] = 4
params['fe_degree'] = 1

params['fault_depth'] = 1e4
params['viscosity'] = 5.0e19
params['shear_modulus'] = 1.0 #30e9

c = controller.Controller(params)

# import pdb;pdb.set_trace()
pd = vc.ProblemData2D(params)
soln = vc.Solution2D(pd)

init_strs = vc.GaussStress2D()
init_vel = vc.ZeroFunction2D(1)

soln.apply_init_cond(init_strs, init_vel);
soln.output(params['data_dir'], 'play.', init_vel)
soln.start_timestep()

inv_visc = vc.InvViscosityTLA2D(params)
inv_rho = 1.0#1.0 / 1e20;

dg = vc.DGStep2D(params['time_step'])
t_max = params['t_max']
t = 0
i = 0
dt = params['time_step']
while t < t_max:
    soln.start_timestep()
    dg.step(pd, soln, inv_visc, inv_rho)
    # if i % 10 == 0:
    soln.output(params['data_dir'], 'play-' + ("%05d" % i) + '.', init_vel)
    t += dt
    i += 1



# pd.start_refine(self.soln.cur_vel)
# soln.start_refine()
# pd.execute_refine()
# soln.reinit()
# soln.post_refine(self.soln)
# scheme.reinit(self.pd);

c.proc0_out("From python: run complete")
c.kill()
