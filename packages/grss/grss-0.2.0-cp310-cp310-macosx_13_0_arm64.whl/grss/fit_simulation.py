import numpy as np
import matplotlib.pyplot as plt
import spiceypy as spice

from . import prop
from .fit_utilities import *

__all__ = [ 'fitSimulation',
            'create_simulated_obs_arrays',
]

class iterationParams:
    def __init__(self, iter_number, x_nom, covariance, residuals, obs_array, observer_codes, rejection_flags):
        self.iter_number = iter_number
        self.x_nom = x_nom
        self.covariance = covariance
        variance = np.sqrt(np.diag(self.covariance))
        self.variance = dict(zip([f'var_{k}' for k in self.x_nom.keys()], variance))
        self.residuals = residuals
        self.obs_array = obs_array
        self.observer_codes = observer_codes
        self.is_accepted = np.where(np.logical_not(rejection_flags) == True)[0]
        self.is_rejected = np.where(np.logical_not(rejection_flags) == False)[0]
        self.sigmas = obs_array[:, 3:5]
        self.weight_matrix = np.diag(1/self.flatten_and_clean(self.sigmas)**2)
        self.calculate_rms()
        self.calculate_chis()
        self.assemble_info()
        return None

    def flatten_and_clean(self, arr):
        arr = arr.flatten()
        arr = arr[~np.isnan(arr)]
        return arr

    def calculate_rms(self):
        residual_arr = self.flatten_and_clean(self.residuals[self.is_accepted])
        n_obs = len(residual_arr)
        self.unweighted_rms = float(np.sqrt(residual_arr.T @ residual_arr/n_obs))
        w = np.diag(1/self.flatten_and_clean(self.sigmas[self.is_accepted])**2)
        self.weighted_rms = float(np.sqrt(residual_arr.T @ w @ residual_arr/n_obs))
        return None

    def calculate_chis(self):
        residual_arr = self.flatten_and_clean(self.residuals[self.is_accepted])
        n_obs = len(residual_arr)
        n_fit = len(self.x_nom)
        sigmas = self.flatten_and_clean(self.sigmas[self.is_accepted])
        self.chi = residual_arr/sigmas
        self.chi_squared = np.sum(self.chi**2)
        self.reduced_chi_squared = self.chi_squared/(n_obs-n_fit)
        return None

    def assemble_info(self):
        # sourcery skip: extract-duplicate-method
        # opticalIdx is where neither the ra nor dec residuals are NaN
        opticalIdx = np.where(~np.isnan(self.residuals[:, 0]) & ~np.isnan(self.residuals[:, 1]))[0]
        # radarIdx is where either the ra or dec residuals are NaN
        radarIdx = np.where(np.isnan(self.residuals[:, 0]) | np.isnan(self.residuals[:, 1]))[0]

        optical_info = self.obs_array.copy()
        optical_info[radarIdx, :] = np.nan
        ra_obs = optical_info[:, 1]
        dec_obs = optical_info[:, 2]
        ra_noise = optical_info[:, 3]
        dec_noise = optical_info[:, 4]
        optical_residuals = self.residuals.copy()
        optical_residuals[radarIdx, :] = np.nan

        radar_info = self.obs_array.copy()
        radar_info[opticalIdx, :] = np.nan
        delay_obs = radar_info[:, 1]
        doppler_obs = radar_info[:, 2]
        delay_noise = radar_info[:, 3]
        doppler_noise = radar_info[:, 4]
        radar_residuals = self.residuals.copy()
        radar_residuals[opticalIdx, :] = np.nan

        self.all_info = {
            'ra_res': optical_residuals[:, 0],
            'dec_res': optical_residuals[:, 1],
            'ra_obs': ra_obs,
            'dec_obs': dec_obs,
            'ra_noise': ra_noise,
            'dec_noise': dec_noise,
            'ra_comp': ra_obs - optical_residuals[:, 0],
            'dec_comp': dec_obs - optical_residuals[:, 1],
            'delay_res': radar_residuals[:, 0],
            'doppler_res': radar_residuals[:, 1],
            'delay_obs': delay_obs,
            'doppler_obs': doppler_obs,
            'delay_noise': delay_noise,
            'doppler_noise': doppler_noise,
            'delay_comp': delay_obs - radar_residuals[:, 0],
            'doppler_comp': doppler_obs - radar_residuals[:, 1],
        }
        # self.all_info['ra_cosdec_res'] = ( (ra_obs/3600*np.pi/180*np.cos(dec_obs/3600*np.pi/180)) - (self.all_info['ra_comp']/3600*np.pi/180*np.cos(self.all_info['dec_comp']/3600*np.pi/180)) )*180/np.pi*3600
        self.all_info['ra_cosdec_res'] = self.all_info['ra_res']*np.cos(dec_obs/3600*np.pi/180)
        self.all_info['ra_chi'] = self.all_info['ra_res']/self.all_info['ra_noise']
        self.all_info['dec_chi'] = self.all_info['dec_res']/self.all_info['dec_noise']
        self.all_info['ra_chi_squared'] = self.all_info['ra_chi']**2
        self.all_info['dec_chi_squared'] = self.all_info['dec_chi']**2
        self.all_info['delay_chi'] = self.all_info['delay_res']/self.all_info['delay_noise']
        self.all_info['doppler_chi'] = self.all_info['doppler_res']/self.all_info['doppler_noise']
        self.all_info['delay_chi_squared'] = self.all_info['delay_chi']**2
        self.all_info['doppler_chi_squared'] = self.all_info['doppler_chi']**2
        return None

    # adapted from https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_hist.html
    def scatter_hist(self, x, y, ax, ax_histx, ax_histy, size, show_logarithmic):
        color = 'C0'
        fill = False
        nbins = 100
        # no labels
        ax_histx.tick_params(   top=True, labeltop=False,
                                bottom=True, labelbottom=False,
                                left=True, labelleft=True,
                                right=True, labelright=False,
                                direction='in')
        ax_histy.tick_params(   left=True, labelleft=False,
                                right=True, labelright=False,
                                top=True, labeltop=False,
                                bottom=True, labelbottom=True,
                                direction='in')
        ax.tick_params( left=True, labelleft=True,
                        right=True, labelright=False,
                        top=True, labeltop=False,
                        bottom=True, labelbottom=True,
                        direction='in')
        # the scatter plot:
        ax.scatter(x, y, s=size, c=color)
        # now determine nice limits:
        if show_logarithmic:
            hist, bins = np.histogram(x, bins=nbins)
            bins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
        else:
            bins = nbins
        ax_histx.hist(x, bins=bins, orientation='vertical', color=color, edgecolor=color, linewidth=0.75, fill=fill, histtype='step')
        ax_histy.hist(y, bins=bins, orientation='horizontal', color=color, edgecolor=color, linewidth=0.75, fill=fill, histtype='step')
        return None

    def plot_residuals(self, t_arr, ra_residuals, dec_residuals, ra_cosdec_residuals, delay_residuals, doppler_residuals, radar_scale, markersize, show_logarithmic, title, savefig, figname):
        # sourcery skip: extract-duplicate-method
        is_rejected = self.is_rejected
        is_accepted = self.is_accepted
        fig = plt.figure(figsize=(21,6), dpi=150)
        iter_string = f'Iteration {self.iter_number} (prefit)' if self.iter_number == 0 else f'Iteration {self.iter_number}'
        iter_string = title if title is not None else iter_string
        plt.suptitle(iter_string, y=0.95)
        gs = fig.add_gridspec(1, 3, width_ratios=(1,1,1))
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(t_arr, ra_residuals, '.', label='RA', markersize=markersize)
        ax1.plot(t_arr, dec_residuals, '.', label='Dec', markersize=markersize)
        ax1.plot(t_arr[is_rejected], ra_residuals[is_rejected], 'ro', markersize=2*markersize, markerfacecolor='none')
        ax1.plot(t_arr[is_rejected], dec_residuals[is_rejected], 'ro', markersize=2*markersize, markerfacecolor='none')
        ax1.legend()
        ax1.set_xlabel('MJD [UTC]')
        ax1.set_ylabel('Residuals, O-C [arcsec]')
        ax1.grid(True, which='both', axis='both', alpha=0.2)
        if show_logarithmic: ax1.set_yscale('log')

        ax2 = gs[0,1].subgridspec(2, 2, width_ratios=(4,1), height_ratios=(1,4), wspace=0.05, hspace=0.05)
        ax2main = fig.add_subplot(ax2[1,0])
        ax2histx = fig.add_subplot(ax2[0,0], sharex=ax2main)
        ax2histy = fig.add_subplot(ax2[1,1], sharey=ax2main)
        self.scatter_hist(ra_cosdec_residuals, dec_residuals, ax2main, ax2histx, ax2histy, markersize, show_logarithmic)
        ax2main.plot(ra_cosdec_residuals[is_rejected], dec_residuals[is_rejected], 'ro', markersize=2*markersize, markerfacecolor='none')
        ax2main.set_xlabel('RA cos(Dec) Residuals, O-C [arcsec]')
        ax2main.set_ylabel('Dec Residuals, O-C [arcsec]')
        ax2main.grid(True, which='both', axis='both', alpha=0.2, zorder=-100)
        if show_logarithmic: ax2main.set_yscale('log'); ax2main.set_xscale('log')
        
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.plot(t_arr, delay_residuals, '.', mfc='C2', mec='C2', label='Delay', markersize=radar_scale*markersize)
        ax3.plot(t_arr, doppler_residuals, '.', mfc='C3', mec='C3', label='Doppler', markersize=radar_scale*markersize)
        ax3.legend()
        ax3.set_xlabel('MJD [UTC]')
        ax3.set_ylabel('Residuals, O-C [$\mu$s, Hz]')
        ax3.grid(True, which='both', axis='both', alpha=0.2)
        if show_logarithmic: ax3.set_yscale('log')
        plt.tight_layout()
        if savefig:
            figname = f'residuals_iter_{self.iter_number}' if figname is None else figname
            plt.savefig(f'{figname}_residuals.pdf', bbox_inches='tight')
        plt.show()

    def plot_chi(self, t_arr, ra_chi, dec_chi, delay_chi, doppler_chi, ra_chi_squared, dec_chi_squared, delay_chi_squared, doppler_chi_squared, sigma_limit, radar_scale, markersize, show_logarithmic, title, savefig, figname):
        is_rejected = self.is_rejected
        is_accepted = self.is_accepted
        # opticalIdx is where neither the ra nor dec residuals are NaN
        opticalIdx = np.where(~np.isnan(self.residuals[:, 0]) & ~np.isnan(self.residuals[:, 1]))[0]
        # radarIdx is where either the ra or dec residuals are NaN
        radarIdx = np.where(np.isnan(self.residuals[:, 0]) | np.isnan(self.residuals[:, 1]))[0]
        # plot chi values
        plt.figure(figsize=(21,6), dpi=150)
        iter_string = f'Iteration {self.iter_number} (prefit)' if self.iter_number == 0 else f'Iteration {self.iter_number}'
        iter_string = title if title is not None else iter_string
        plt.suptitle(f'{iter_string}. Chi Squared: RA={np.sum(ra_chi_squared[np.intersect1d(is_accepted, opticalIdx)]):.2f}, Dec={np.sum(dec_chi_squared[np.intersect1d(is_accepted, opticalIdx)]):.2f}, Delay={np.nansum(delay_chi_squared[np.intersect1d(is_accepted, radarIdx)]):.2f}, Doppler={np.nansum(doppler_chi_squared[np.intersect1d(is_accepted, radarIdx)]):.2f}', y=0.95)
        plt.subplot(1,2,1)
        plt.plot(t_arr, ra_chi, '.', markersize=markersize, label='RA')
        plt.plot(t_arr, dec_chi, '.', markersize=markersize, label='Dec')
        plt.plot(t_arr[is_rejected], ra_chi[is_rejected], 'ro', markersize=2*markersize, markerfacecolor='none')
        plt.plot(t_arr[is_rejected], dec_chi[is_rejected], 'ro', markersize=2*markersize, markerfacecolor='none')
        plt.plot(t_arr, delay_chi, '.', mfc='C2', mec='C2', markersize=radar_scale*markersize, label='Delay')
        plt.plot(t_arr, doppler_chi, '.', mfc='C3', mec='C3', markersize=radar_scale*markersize, label='Doppler')
        plt.axhline(-sigma_limit, c='khaki', linestyle='--', alpha=1.0, label=f'$\pm{sigma_limit:.0f}\sigma$')
        plt.axhline(sigma_limit, c='khaki', linestyle='--', alpha=1.0)
        plt.axhline(-2*sigma_limit, c='red', linestyle='--', alpha=0.5, label=f'$\pm{2*sigma_limit:.0f}\sigma$')
        plt.axhline(2*sigma_limit, c='red', linestyle='--', alpha=0.5)
        plt.legend(ncol=3)
        plt.xlabel('MJD [UTC]')
        plt.ylabel('$\chi$, (O-C)/$\sigma$ $[\cdot]$')
        plt.grid(True, which='both', axis='both', alpha=0.2)
        if show_logarithmic: plt.yscale('log')

        plt.subplot(1,2,2)
        plt.plot(t_arr, ra_chi_squared, '.', markersize=markersize, label='RA')
        plt.plot(t_arr, dec_chi_squared, '.', markersize=markersize, label='Dec')
        plt.plot(t_arr[is_rejected], ra_chi_squared[is_rejected], 'ro', markersize=2*markersize, markerfacecolor='none')
        plt.plot(t_arr[is_rejected], dec_chi_squared[is_rejected], 'ro', markersize=2*markersize, markerfacecolor='none')
        plt.plot(t_arr, delay_chi_squared, '.', mfc='C2', mec='C2', markersize=radar_scale*markersize, label='Delay')
        plt.plot(t_arr, doppler_chi_squared, '.', mfc='C3', mec='C3', markersize=radar_scale*markersize, label='Doppler')
        plt.legend(ncol=2)
        plt.xlabel('MJD [UTC]')
        plt.ylabel('$\chi^2$, (O-C)$^2/\sigma^2$ $[\cdot]$')
        plt.grid(True, which='both', axis='both', alpha=0.2)
        # if show_logarithmic: plt.yscale('log')
        plt.yscale('log')
        plt.tight_layout()
        if savefig:
            figname = f'chi_iter_{self.iter_number}' if figname is None else figname
            plt.savefig(f'{figname}_chi.pdf', bbox_inches='tight')
        plt.show()

    def plot_iteration_summary(self, show_logarithmic=False, title=None, savefig=False, figname=None):
        markersize = 3
        sigma_limit = 3
        radar_scale = 3
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.labelsize'] = 12
        
        t_arr = self.obs_array[:, 0]
        ra_residuals = np.abs(self.all_info['ra_res']) if show_logarithmic else self.all_info['ra_res']
        dec_residuals = np.abs(self.all_info['dec_res']) if show_logarithmic else self.all_info['dec_res']
        ra_cosdec_residuals = np.abs(self.all_info['ra_cosdec_res']) if show_logarithmic else self.all_info['ra_cosdec_res']
        ra_chi = np.abs(self.all_info['ra_chi']) if show_logarithmic else self.all_info['ra_chi']
        dec_chi = np.abs(self.all_info['dec_chi']) if show_logarithmic else self.all_info['dec_chi']
        ra_chi_squared = self.all_info['ra_chi_squared']
        dec_chi_squared = self.all_info['dec_chi_squared']
        
        delay_residuals = np.abs(self.all_info['delay_res']) if show_logarithmic else self.all_info['delay_res']
        doppler_residuals = np.abs(self.all_info['doppler_res']) if show_logarithmic else self.all_info['doppler_res']
        delay_chi = np.abs(self.all_info['delay_chi']) if show_logarithmic else self.all_info['delay_chi']
        doppler_chi = np.abs(self.all_info['doppler_chi']) if show_logarithmic else self.all_info['doppler_chi']
        delay_chi_squared = self.all_info['delay_chi_squared']
        doppler_chi_squared = self.all_info['doppler_chi_squared']
        
        self.plot_residuals(t_arr, ra_residuals, dec_residuals, ra_cosdec_residuals, delay_residuals, doppler_residuals, radar_scale, markersize, show_logarithmic, title, savefig, figname)
        self.plot_chi(t_arr, ra_chi, dec_chi, delay_chi, doppler_chi, ra_chi_squared, dec_chi_squared, delay_chi_squared, doppler_chi_squared, sigma_limit, radar_scale, markersize, show_logarithmic, title, savefig, figname)
        return None

class fitSimulation:
    def __init__(self, x_init, cov_init=None, obs_array_optical=None, observer_codes_optical=None, obs_array_radar=None, observer_codes_radar=None, n_iter_max=10, DEkernel=441, DEkernelPath='', radius=0.0, nongravInfo=None, events=None):
        self.check_initial_solution(x_init, cov_init)
        self.check_input_observation_arrays(obs_array_optical, observer_codes_optical, obs_array_radar, observer_codes_radar)
        self.assemble_observation_arrays()
        self.n_iter = 0
        self.n_iter_max = n_iter_max
        self.iters = []
        self.DEkernel = DEkernel
        self.DEkernelPath = DEkernelPath
        self.analytic_partials = False
        self.fixed_propSim_params = {'a1': 0.0, 'a2': 0.0, 'a3': 0.0, 'alpha': 1.0, 'k': 0.0, 'm': 2.0, 'n': 0.0, 'r0_au': 1.0, 'radius': radius, 'mass': 0.0}
        for key in nongravInfo:
            self.fixed_propSim_params[key] = nongravInfo[key]
        if events is not None:
            self.fixed_propSim_params['events'] = events
            self.fit_events = True
        else:
            self.fixed_propSim_params['events'] = []
            self.fit_events = False
        return None

    def check_initial_solution(self, x_init, cov_init):
        if 't' not in x_init:
            raise ValueError("Must provide a time for the initial solution.")
        if all(key in x_init for key in ("x", "y", "z", "vx", "vy", "vz")):
            self.fit_cartesian = True
            self.fit_cometary = False
        elif all(key in x_init for key in ("e", "q", "tp", "om", "w", "i")):
            self.fit_cartesian = False
            self.fit_cometary = True
        else:
            raise ValueError("Must provide at least a full cartesian or cometary state for the initial solution.")
        for key in ["a1", "a2", "a3"]:
            if key in x_init and x_init[key] != 0.0:
                self.fit_nongrav = True
        self.t = x_init['t']
        self.x_init = x_init
        self.x_nom = {key: x_init[key] for key in x_init if key != 't'} # remove t for self.x_nom
        self.n_fit = len(self.x_nom)
        if cov_init.shape != (self.n_fit, self.n_fit):
            raise ValueError("Covariance matrix must be the same size as the number of fitted parameters.")
        self.covariance_init = cov_init
        self.covariance = cov_init
        return None

    def check_input_observation_arrays(self, obs_array_optical, observer_codes_optical, obs_array_radar, observer_codes_radar):
        self.fit_optical = False
        self.fit_radar = False
        if obs_array_optical is None and obs_array_radar is None:
            raise ValueError("Must provide at least one observation array (optical or radar).")
        
        if obs_array_optical is not None and observer_codes_optical is None:
            raise ValueError("Must provide observer codes for optical observations.")
        if obs_array_optical is None and observer_codes_optical is not None:
            raise ValueError("Must provide optical observations for observer codes.")
        if obs_array_optical is not None and observer_codes_optical is not None:
            if len(obs_array_optical) != len(observer_codes_optical):
                raise ValueError("Optical observation array and observer code array must be the same length.")
            else:
                self.fit_optical = True
        if obs_array_radar is not None and observer_codes_radar is None:
            raise ValueError("Must provide observer codes for radar observations.")
        if obs_array_radar is None and observer_codes_radar is not None:
            raise ValueError("Must provide radar observations for observer codes.")
        if obs_array_radar is not None and observer_codes_radar is not None:
            if len(obs_array_radar) != len(observer_codes_radar):
                raise ValueError("Radar observation array and observer code array must be the same length.")
            else:
                self.fit_radar = True
        self.obs_array_optical = obs_array_optical
        self.observer_codes_optical = observer_codes_optical
        self.obs_array_radar = obs_array_radar
        self.observer_codes_radar = observer_codes_radar
        return None

    def flatten_and_clean(self, arr):
        arr = arr.flatten()
        arr = arr[~np.isnan(arr)]
        return arr

    def assemble_observation_arrays(self):
        if self.fit_optical and self.fit_radar:
            self.merge_observation_arrays()
        elif self.fit_optical:
            self.obs_array, sort_idx = self.sort_array_by_another(self.obs_array_optical, self.obs_array_optical[:, 0])
            self.observer_codes = tuple(np.array(self.observer_codes_optical, dtype=tuple)[sort_idx])
        elif self.fit_radar:
            self.obs_array, sort_idx = self.sort_array_by_another(self.obs_array_radar, self.obs_array_radar[:, 0])
            self.observer_codes = tuple(np.array(self.observer_codes_radar, dtype=tuple)[sort_idx])
        self.n_obs = np.count_nonzero(~np.isnan(self.obs_array[:, 1:3])) # number of observations is the number of non-nan values in the second and third columns of the observation array
        self.rejection_flag = [False]*len(self.obs_array)
        self.sigmas = self.obs_array[:, 3:5]
        self.weight_matrix = np.diag(1/self.flatten_and_clean(self.sigmas)**2)
        self.obs_cov_matrix = np.diag(self.flatten_and_clean(self.sigmas)**2)
        self.pastObsIdx = np.where(self.obs_array[:, 0] < self.t)[0]
        self.pastObsExist = len(self.pastObsIdx) > 0
        self.futureObsIdx = np.where(self.obs_array[:, 0] >= self.t)[0]
        self.futureObsExist = len(self.futureObsIdx) > 0
        return None
    
    def sort_array_by_another(self, array, sort_by):
        sort_idx = np.argsort(sort_by)
        return array[sort_idx], sort_idx

    def merge_observation_arrays(self):
        # merge optical and radar arrays
        obs_array = np.vstack((self.obs_array_optical, self.obs_array_radar))
        observer_codes = self.observer_codes_optical + self.observer_codes_radar
        # sort by time
        self.obs_array, sort_idx = self.sort_array_by_another(obs_array, obs_array[:, 0])
        self.observer_codes = tuple(np.array(observer_codes, dtype=tuple)[sort_idx])
        return None

    def get_propSimPast(self, name, tEvalUTC, evalApparentState, convergedLightTime, observerInfo):
        tEvalPast = self.obs_array[self.pastObsIdx, 0]
        tfPast = np.min(tEvalPast) - 1
        propSimPast = prop.propSimulation(name, self.t, self.DEkernel, self.DEkernelPath)
        propSimPast.set_integration_parameters(tfPast, tEvalPast, tEvalUTC, evalApparentState, convergedLightTime, observerInfo)
        return propSimPast

    def get_propSimFuture(self, name, tEvalUTC, evalApparentState, convergedLightTime, observerInfo):
        tEvalFuture = self.obs_array[self.futureObsIdx, 0]
        tfFuture = np.max(tEvalFuture) + 1
        propSimFuture = prop.propSimulation(name, self.t, self.DEkernel, self.DEkernelPath)
        propSimFuture.set_integration_parameters(tfFuture, tEvalFuture, tEvalUTC, evalApparentState, convergedLightTime, observerInfo)
        return propSimFuture

    def get_propSims(self, name):
        tEvalUTC = True
        evalApparentState = True
        convergedLightTime = True
        observerInfo = np.array(get_observer_info(self.observer_codes), dtype=tuple)
        observerInfoPast = tuple(observerInfo[self.pastObsIdx])
        observerInfoFuture = tuple(observerInfo[self.futureObsIdx])
        propSimPast = None
        propSimFuture = None
        if self.pastObsExist:
            propSimPast = self.get_propSimPast(f"{name}_past", tEvalUTC, evalApparentState, convergedLightTime, observerInfoPast)
        if self.futureObsExist:
            propSimFuture = self.get_propSimFuture(f"{name}_future", tEvalUTC, evalApparentState, convergedLightTime, observerInfoFuture)
        return propSimPast, propSimFuture

    def x_dict_to_state(self, x_dict):
        # sourcery skip: extract-method
        if self.fit_cartesian:
            x = x_dict['x']
            y = x_dict['y']
            z = x_dict['z']
            vx = x_dict['vx']
            vy = x_dict['vy']
            vz = x_dict['vz']
            state = [x, y, z, vx, vy, vz]
        elif self.fit_cometary:
            e = x_dict['e']
            q = x_dict['q']
            tp = x_dict['tp']
            om = x_dict['om']
            w = x_dict['w']
            i = x_dict['i']
            cometary_elements = [e, q, tp, om*np.pi/180.0, w*np.pi/180.0, i*np.pi/180.0]
            state = cometary_elements
        else:
            raise ValueError("fit_cartesian or fit_cometary must be True")
        return state

    def x_dict_to_nongrav_params(self, x_dict):
        nongravParams = prop.NongravParamaters()
        a1 = x_dict['a1'] if 'a1' in x_dict.keys() else self.fixed_propSim_params['a1']
        a2 = x_dict['a2'] if 'a2' in x_dict.keys() else self.fixed_propSim_params['a2']
        a3 = x_dict['a3'] if 'a3' in x_dict.keys() else self.fixed_propSim_params['a3']
        nongravParams.a1 = a1
        nongravParams.a2 = a2
        nongravParams.a3 = a3
        nongravParams.alpha = self.fixed_propSim_params['alpha']
        nongravParams.k = self.fixed_propSim_params['k']
        nongravParams.m = self.fixed_propSim_params['m']
        nongravParams.n = self.fixed_propSim_params['n']
        nongravParams.r0_au = self.fixed_propSim_params['r0_au']
        return nongravParams

    def x_dict_to_events(self, x_dict):
        events = []
        for i in range(len(self.fixed_propSim_params['events'])):
            event = self.fixed_propSim_params['events'][i]
            event[1] = x_dict[f"dvx{i}"] if f"dvx{i}" in x_dict.keys() else event[1]
            event[2] = x_dict[f"dvy{i}"] if f"dvy{i}" in x_dict.keys() else event[2]
            event[3] = x_dict[f"dvz{i}"] if f"dvz{i}" in x_dict.keys() else event[3]
            event[4] = x_dict[f"multiplier{i}"] if f"multiplier{i}" in x_dict.keys() else event[4]
            events.append(tuple(event))
        return events

    def check_and_add_events(self, propSimPast, propSimFuture, integBody, events):
        for event in events:
            t_event = event[0]
            dvx = event[1]
            dvy = event[2]
            dvz = event[3]
            multiplier = event[4]
            if t_event < self.t:
                propSimPast.add_event(integBody, t_event, [dvx, dvy, dvz], multiplier)
            else:
                propSimFuture.add_event(integBody, t_event, [dvx, dvy, dvz], multiplier)
        return propSimPast, propSimFuture

    def get_perturbed_state(self, key):
        if self.fit_cartesian:
            if key in ['x', 'y', 'z']:
                fd_pert = 1e-8
            elif key in ['vx', 'vy', 'vz']:
                fd_pert = 1e-10
        elif self.fit_cometary:
            fd_pert = 1e-8
            # if key in ['q']:
            #     fd_pert = 5e-5
            # elif key in ['e']:
            #     fd_pert = 5e-4
            # elif key in ['tp']:
            #     fd_pert = 1e-5
            # elif key in ['om']:
            #     fd_pert = 1e-6
            # elif key in ['w']:
            #     fd_pert = 1e-6
            # elif key in ['i']:
            #     fd_pert = 1e-6
        if key in ['a1', 'a2', 'a3']:
            fd_pert = 1e-3
        if key[:10] == 'multiplier':
            fd_pert = 1e0
        if key[:3] in ['dvx', 'dvy', 'dvz']:
            fd_pert = 1e-4

        x_plus = self.x_nom.copy()
        x_minus = self.x_nom.copy()
        fd_delta = self.x_nom[key]*fd_pert # fd_pert = finite difference perturbation to nominal state for calculating derivatives
        x_plus[key] = self.x_nom[key]+fd_delta
        state_plus = self.x_dict_to_state(x_plus)
        ngParams_plus = self.x_dict_to_nongrav_params(x_plus)
        events_plus = self.x_dict_to_events(x_plus)
        x_minus[key] = self.x_nom[key]-fd_delta
        state_minus = self.x_dict_to_state(x_minus)
        ngParams_minus = self.x_dict_to_nongrav_params(x_minus)
        events_minus = self.x_dict_to_events(x_minus)
        return state_plus, ngParams_plus, events_plus, state_minus, ngParams_minus, events_minus, fd_delta

    def get_perturbation_info(self):
        perturbation_info = []
        for key in self.x_nom:
            pert_result = self.get_perturbed_state(key)
            perturbation_info.append(tuple(pert_result))
        return perturbation_info

    def assemble_and_propagate_bodies(self, perturbation_info):
        # get propagated states
        propSimPast, propSimFuture = self.get_propSims("orbit_fit_sim")
        # create nominal IntegBody object
        consts = prop.Constants()
        state_nom = self.x_dict_to_state(self.x_nom)
        ngParams_nom = self.x_dict_to_nongrav_params(self.x_nom)
        events_nom = self.x_dict_to_events(self.x_nom)
        cov_nom = self.covariance
        if self.fit_cartesian:
            integBody_nom = prop.IntegBody("integBody_nom", self.t, self.fixed_propSim_params['mass'], self.fixed_propSim_params['radius'], state_nom[:3], state_nom[3:6], cov_nom, ngParams_nom, consts)
        elif self.fit_cometary:
            integBody_nom = prop.IntegBody(self.DEkernelPath, "integBody_nom", self.t, self.fixed_propSim_params['mass'], self.fixed_propSim_params['radius'], state_nom, cov_nom, ngParams_nom, consts)
        # add the nominal IntegBody for the residuals
        if self.pastObsExist:
            propSimPast.add_integ_body(integBody_nom)
        if self.futureObsExist:
            propSimFuture.add_integ_body(integBody_nom)
        propSimPast, propSimFuture = self.check_and_add_events(propSimPast, propSimFuture, integBody_nom, events_nom)
        # add the perturbed IntegBodies for numerical derivatives
        if not self.analytic_partials and perturbation_info is not None:
            for i in range(self.n_fit):
                key = list(self.x_nom.keys())[i]
                state_plus, ngParams_plus, events_plus, state_minus, ngParams_minus, events_minus, fd_delta = perturbation_info[i]
                if self.fit_cartesian:
                    integBody_plus = prop.IntegBody(f"integBody_pert_{key}_plus", self.t, self.fixed_propSim_params['mass'], self.fixed_propSim_params['radius'], state_plus[:3], state_plus[3:6], cov_nom, ngParams_plus, consts)
                    integBody_minus = prop.IntegBody(f"integBody_pert_{key}_minus", self.t, self.fixed_propSim_params['mass'], self.fixed_propSim_params['radius'], state_minus[:3], state_minus[3:6], cov_nom, ngParams_minus, consts)
                elif self.fit_cometary:
                    integBody_plus = prop.IntegBody(self.DEkernelPath, f"integBody_pert_{key}_plus", self.t, self.fixed_propSim_params['mass'], self.fixed_propSim_params['radius'], state_plus, cov_nom, ngParams_plus, consts)
                    integBody_minus = prop.IntegBody(self.DEkernelPath, f"integBody_pert_{key}_minus", self.t, self.fixed_propSim_params['mass'], self.fixed_propSim_params['radius'], state_minus, cov_nom, ngParams_minus, consts)
                if self.pastObsExist:
                    propSimPast.add_integ_body(integBody_plus)
                    propSimPast.add_integ_body(integBody_minus)
                if self.futureObsExist:
                    propSimFuture.add_integ_body(integBody_plus)
                    propSimFuture.add_integ_body(integBody_minus)
                propSimPast, propSimFuture = self.check_and_add_events(propSimPast, propSimFuture, integBody_plus, events_plus)
                propSimPast, propSimFuture = self.check_and_add_events(propSimPast, propSimFuture, integBody_minus, events_minus)
        if self.pastObsExist:
            propSimPast.preprocess()
            propSimPast.integrate()
        if self.futureObsExist:
            propSimFuture.preprocess()
            propSimFuture.integrate()
        return propSimPast, propSimFuture

    def get_computed_obs(self, propSimPast, propSimFuture, integBodyIdx):
        if self.pastObsExist and self.futureObsExist:
            apparent_states_past = np.array(propSimPast.xIntegEval)
            apparent_states_future = np.array(propSimFuture.xIntegEval)
            apparent_states = np.vstack((apparent_states_past, apparent_states_future))
            radar_observations_past = np.array(propSimPast.radarObsEval)
            radar_observations_future = np.array(propSimFuture.radarObsEval)
            radar_observations = np.vstack((radar_observations_past, radar_observations_future))
        elif self.pastObsExist:
            apparent_states_past = np.array(propSimPast.xIntegEval)
            apparent_states = apparent_states_past
            radar_observations_past = np.array(propSimPast.radarObsEval)
            radar_observations = radar_observations_past
        elif self.futureObsExist:
            apparent_states_future = np.array(propSimFuture.xIntegEval)
            apparent_states = apparent_states_future
            radar_observations_future = np.array(propSimFuture.radarObsEval)
            radar_observations = radar_observations_future
        integ_body_start_col = 6*integBodyIdx
        integ_body_end_col = 6*integBodyIdx+6
        apparent_states = apparent_states[:,integ_body_start_col:integ_body_end_col]
        radar_observations = radar_observations[:,integBodyIdx]

        measured_obs = self.obs_array[:, 1:3]
        computed_obs = np.nan*np.ones_like(measured_obs)
        observerInfo = get_observer_info(self.observer_codes)
        for i in range(len(self.obs_array)):
            obs_info_len = len(observerInfo[i])
            if obs_info_len == 4:
                computed_obs[i, :] = get_radec(apparent_states[i])
            elif obs_info_len == 9: # delay measurement
                computed_obs[i, 0] = radar_observations[i]
            elif obs_info_len == 10: # dopper measurement
                computed_obs[i, 1] = radar_observations[i]
            else:
                raise ValueError("Observer info length not recognized.")
        return computed_obs

    def get_analytic_partials(self, propSimPast, propSimFuture):
        raise NotImplementedError("Analytic partials not yet implemented. Please use numeric partials.")

    def get_numeric_partials(self, propSimPast, propSimFuture, perturbation_info):
        partials = np.zeros((self.n_obs, self.n_fit))
        for i in range(self.n_fit):
            key = list(self.x_nom.keys())[i]
            state_plus, ngParams_plus, events_plus, state_minus, ngParams_minus, events_minus, fd_delta = perturbation_info[i]
            # get computed_obs for perturbed states
            computed_obs_plus = self.get_computed_obs(propSimPast, propSimFuture, integBodyIdx=2*i+1)
            computed_obs_minus = self.get_computed_obs(propSimPast, propSimFuture, integBodyIdx=2*i+2)
            computed_obs_plus = self.flatten_and_clean(computed_obs_plus)
            computed_obs_minus = self.flatten_and_clean(computed_obs_minus)
            # get partials
            partials[:, i] = (computed_obs_plus - computed_obs_minus)/(2*fd_delta)
        return partials

    def get_partials(self, propSimPast, propSimFuture, perturbation_info):
        return self.get_analytic_partials(propSimPast, propSimFuture) if self.analytic_partials else self.get_numeric_partials(propSimPast, propSimFuture, perturbation_info)

    def get_residuals_and_partials(self):
        perturbation_info = None if self.analytic_partials else self.get_perturbation_info()
        propSimPast, propSimFuture = self.assemble_and_propagate_bodies(perturbation_info)
        # get residuals
        computed_obs = self.get_computed_obs(propSimPast, propSimFuture, integBodyIdx=0)
        residuals = self.obs_array[:, 1:3] - computed_obs
        # get partials
        partials = self.get_partials(propSimPast, propSimFuture, perturbation_info)
        return residuals, partials

    def reject_outliers(self, a, w, b):
        chi_reject = 3.0
        chi_recover = 2.8
        full_cov = np.linalg.inv(a.T @ self.weight_matrix @ a)
        observerInfo = get_observer_info(self.observer_codes)
        j = 0
        residual_chi_squared = np.zeros(len(self.obs_array))
        rejected_indices = []
        resid_cov_full = self.obs_cov_matrix - a @ full_cov @ a.T
        for i in range(len(self.obs_array)):
            obs_info_len = len(observerInfo[i])
            if obs_info_len == 4:
                size = 2
            elif obs_info_len in {9, 10}:
                size = 1
                j += size
                continue
            else:
                raise ValueError("Observer info length not recognized.")
            # calculate chi-squared for each residual
            resid = b[j:j+size].reshape((1, size))
            partials = a[j:j+size, :]
            covs = self.obs_cov_matrix[j:j+size, j:j+size]
            # resid_cov = covs - partials @ full_cov @ partials.T
            resid_cov = resid_cov_full[j:j+size, j:j+size]
            residual_chi_squared[i] = resid @ np.linalg.inv(resid_cov) @ resid.T
            # outlier rejection
            if residual_chi_squared[i] > chi_reject**2 and size == 2: # only reject RA/Dec measurements
                self.rejection_flag[i] = True
            if self.rejection_flag[i] and residual_chi_squared[i] < chi_recover**2:
                self.rejection_flag[i] = False
                print("Recovered observation at time", self.obs_array[i, 0])
            # # sigma clipping
            # if abs(resid[0, 0])/self.obs_array[i,3] >= chi_reject or abs(resid[0, 1])/self.obs_array[i,4] >= chi_reject:
            #     self.rejection_flag[i] = True
            # if self.rejection_flag[i] and (abs(resid[0, 0])/self.obs_array[i,3] < chi_recover and abs(resid[0, 1])/self.obs_array[i,4] < chi_recover):
            #     self.rejection_flag[i] = False
            #     print("Recovered observation at time", self.obs_array[i, 0])
            if self.rejection_flag[i]:
                rejected_indices.extend((j, j+1))
            j += size
        # remove rejected residuals from a, w, and b
        a = np.delete(a, rejected_indices, axis=0)
        w = np.delete(w, rejected_indices, axis=0)
        w = np.delete(w, rejected_indices, axis=1)
        b = np.delete(b, rejected_indices, axis=0)
        # print(rejected_indices)
        num_rejected = len(rejected_indices)//2
        num_total = len(self.obs_array)
        if num_rejected/num_total > 0.25:
            print("WARNING: More than 25% of observations rejected. Consider changing chi_reject and chi_recover values, or turning off outlier rejection altogether.")
        self.residual_chi_squared = residual_chi_squared
        return a, w, b, residual_chi_squared

    def add_iteration(self, iter_number, residuals):
        self.iters.append(iterationParams(iter_number, self.x_nom, self.covariance, residuals, self.obs_array, self.observer_codes, self.rejection_flag))
        return None

    def check_convergence(self):
        if self.n_iter > 1:
            del_rms_convergence = 1e-3
            curr_rms = self.iters[-1].unweighted_rms
            prev_rms = self.iters[-2].unweighted_rms
            del_rms = abs(prev_rms - curr_rms)/prev_rms
            if del_rms < del_rms_convergence:
                self.converged = True
        return None

    def filter_lsq(self, verbose=True):
        self.converged = False
        start_rejecting = False
        spice.furnsh(self.DEkernelPath)
        if verbose:
            print("Iteration\t\tUnweighted RMS\t\tWeighted RMS\t\tChi-squared\t\tReduced Chi-squared")
        for i in range(self.n_iter_max):
            self.n_iter = i+1
            # get residuals and partials
            residuals, a = self.get_residuals_and_partials()
            w = self.weight_matrix
            if i == 0:
                # add prefit iteration
                prefit_residuals = residuals.copy()
                self.add_iteration(0, prefit_residuals)
            b = self.flatten_and_clean(residuals)
            # reject outliers here
            if start_rejecting:
                a_rej, w_rej, b_rej, residual_chi_squared = self.reject_outliers(a, w, b)
            else:
                a_rej, w_rej, b_rej = a, w, b
            # a_rej, w_rej, b_rej = a, w, b
            # get initial guess
            x0 = np.array(list(self.x_nom.values()))
            # get covariance
            cov = self.covariance
            # get state correction
            atwa = a_rej.T @ w_rej @ a_rej
            P = np.linalg.inv(atwa)
            atwb = a_rej.T @ w_rej @ b_rej
            dx = P @ atwb
            # dx = np.linalg.solve(atwa, atwb)
            # get new state
            x = x0 + dx
            self.x_nom = dict(zip(self.x_nom.keys(), x))
            # get new covariance
            self.covariance = P
            # add iteration
            self.add_iteration(i+1, residuals)
            if verbose:
                print("%d%s\t\t\t%.3f\t\t\t%.3f\t\t\t%.3f\t\t\t%.3f" % (self.iters[-1].iter_number, "", self.iters[-1].unweighted_rms, self.iters[-1].weighted_rms, self.iters[-1].chi_squared, self.iters[-1].reduced_chi_squared))
            self.check_convergence()
            if self.converged:
                if start_rejecting:
                    print("Converged after rejecting outliers.")
                    break
                else:
                    print("Converged without rejecting outliers. Starting outlier rejection now...")
                    start_rejecting = True
                    self.converged = False
        if self.n_iter == self.n_iter_max and not self.converged:
            print("WARNING: Maximum number of iterations reached without converging.")
        spice.unload(self.DEkernelPath)
        return None

    def print_summary(self, iter_idx=-1):
        data = self.iters[iter_idx]
        print(f"Summary of the orbit fit calculations at iteration {data.iter_number} (of {self.n_iter}):")
        print("=======================================================")
        print(f"RMS unweighted: {data.unweighted_rms}")
        print(f"RMS weighted: {data.weighted_rms}")
        print(f"chi-squared: {data.chi_squared}")
        print(f"reduced chi-squared: {data.reduced_chi_squared}")
        print(f"square root of reduced chi-squared: {np.sqrt(data.reduced_chi_squared)}")
        print("=======================================================")
        print(f"t: MJD {self.t} TDB")
        print("Fitted Variable\t\tInitial Value\t\t\tUncertainty\t\t\tFitted Value\t\t\tUncertainty\t\t\t\tChange\t\t\t\tChange (sigma)")
        init_variance = np.sqrt(np.diag(self.covariance_init))
        final_variance = np.sqrt(np.diag(self.covariance))
        init_sol = self.iters[0].x_nom
        final_sol = data.x_nom
        with np.errstate(divide='ignore'):
            for i, key in enumerate(init_sol.keys()):
                if key[:10] == 'multiplier':
                    print(f"{key}\t\t{init_sol[key]:.11e}\t\t{init_variance[i]:.11e}\t\t{final_sol[key]:.11e}\t\t{final_variance[i]:.11e}\t\t{final_sol[key]-init_sol[key]:+.11e}\t\t{(final_sol[key]-init_sol[key])/init_variance[i]:+.3f}")
                else:
                    print(f"{key}\t\t\t{init_sol[key]:.11e}\t\t{init_variance[i]:.11e}\t\t{final_sol[key]:.11e}\t\t{final_variance[i]:.11e}\t\t{final_sol[key]-init_sol[key]:+.11e}\t\t{(final_sol[key]-init_sol[key])/init_variance[i]:+.3f}")
        return None

    def plot_summary(self):
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.labelsize'] = 12
        ticks = np.arange(1, self.n_iter+1, 1)
        start_idx = 1
        iters_for_plot = self.iters[start_idx:]
        plt.figure(figsize=(21,10), dpi=150)
        plt.subplot(2, 2, 1)
        plt.semilogy([iteration.iter_number for iteration in iters_for_plot], [iteration.unweighted_rms for iteration in iters_for_plot], label=f"Final Unweighted RMS={iters_for_plot[-1].unweighted_rms:.3e}")
        plt.xticks(ticks)
        plt.xlabel("Iteration #")
        plt.ylabel("Unweighted RMS")
        plt.legend()
        
        plt.subplot(2, 2, 2)
        plt.semilogy([iteration.iter_number for iteration in iters_for_plot], [iteration.weighted_rms for iteration in iters_for_plot], label=f"Final Weighted RMS={iters_for_plot[-1].weighted_rms:.3e}")
        plt.xticks(ticks)
        plt.xlabel("Iteration #")
        plt.ylabel("Weighted RMS")
        plt.legend()
        
        plt.subplot(2, 2, 3)
        plt.semilogy([iteration.iter_number for iteration in iters_for_plot], [iteration.chi_squared for iteration in iters_for_plot], label=f"Final $\chi^2$={iters_for_plot[-1].chi_squared:.3e}")
        plt.xticks(ticks)
        plt.xlabel("Iteration #")
        plt.ylabel("$\chi^2$")
        plt.legend()
        
        plt.subplot(2, 2, 4)
        plt.semilogy([iteration.iter_number for iteration in iters_for_plot], [iteration.reduced_chi_squared for iteration in iters_for_plot], label=f"Final Reduced $\chi^2$={iters_for_plot[-1].reduced_chi_squared:.3e}")
        plt.xticks(ticks)
        plt.xlabel("Iteration #")
        plt.ylabel("Reduced $\chi^2$")
        plt.legend()
        plt.show()
        return None

def _generate_simulated_obs(ref_sol, ref_cov, ref_ngInfo, events, optical_times, optical_obs_types, radar_times, radar_obs_types, DEkernel, DEkernelPath, noise, bias, doppler_freq=8560e6, observatory_code='500'):
    obs_sigma_dict = {  'astrometry': 1, # arcsec
                        'occultation': 2.5e-3, # arcsec
                        'delay': 2, # microseconds
                        'delay_hera': 15 /299792458*1e6, # 15 meter (conservative since it is 1m random + 10m systematic) to light microseconds
                        'doppler': 0.5, # Hz
                        # 'doppler_hera': 0.1 mm/s to Hz (shift * clight/transmission_freq = 0.1 mm/s)
    }
    # check length of times is not zero
    if len(optical_times) == 0 and len(radar_times) == 0:
        raise ValueError("Must provide at least one observation time.")
    # check length of times and obs_types are the same
    if len(optical_times) != len(optical_obs_types):
        raise ValueError("Must provide the same number of optical observation times and observation types.")
    if len(radar_times) != len(radar_obs_types):
        raise ValueError("Must provide the same number of radar observation times and observation types.")
    # check that the reference solution has the requisite information and create integration body
    if 't' not in ref_sol:
        raise ValueError("Must provide a time for the initial solution.")
    consts = prop.Constants()
    nongravParams = prop.NongravParamaters()
    nongravParams.a1 = ref_ngInfo['a1']
    nongravParams.a2 = ref_ngInfo['a2']
    nongravParams.a3 = ref_ngInfo['a3']
    nongravParams.alpha = ref_ngInfo['alpha']
    nongravParams.k = ref_ngInfo['k']
    nongravParams.m = ref_ngInfo['m']
    nongravParams.n = ref_ngInfo['n']
    nongravParams.r0_au = ref_ngInfo['r0_au']
    if all(key in ref_sol for key in ("x", "y", "z", "vx", "vy", "vz")):
        pos = [ref_sol['x'], ref_sol['y'], ref_sol['z']]
        vel = [ref_sol['vx'], ref_sol['vy'], ref_sol['vz']]
        targetBody = prop.IntegBody("body_simulated_obs", ref_sol['t'], ref_sol['mass'], ref_sol['radius'], pos, vel, ref_cov, nongravParams, consts)
    elif all(key in ref_sol for key in ("e", "q", "tp", "om", "w", "i")):
        e = ref_sol['e']
        q = ref_sol['q']
        tp = ref_sol['tp']
        om = ref_sol['om']
        w = ref_sol['w']
        i = ref_sol['i']
        cometary_elements = [e, q, tp, om*np.pi/180.0, w*np.pi/180.0, i*np.pi/180.0]
        targetBody = prop.IntegBody(DEkernelPath, "body_simulated_obs", ref_sol['t'], ref_sol['mass'], ref_sol['radius'], cometary_elements, ref_cov, nongravParams, consts)
    else:
        raise ValueError("Must provide either a full cartesian or cometary state for the initial solution.")
    # initialize past and future times and observer codes
    optical_observer_codes = tuple([observatory_code]*len(optical_times))
    radar_observer_codes = []
    for i in range(len(radar_times)):
        codes = [(observatory_code, observatory_code), 0]
        if radar_obs_types[i].lower() == 'doppler':
            codes.append(doppler_freq)
        radar_observer_codes.append(tuple(codes))
    radar_observer_codes = tuple(radar_observer_codes)
    obs_times = np.array(optical_times + radar_times)
    observer_codes = optical_observer_codes + radar_observer_codes
    obs_types = tuple(optical_obs_types + radar_obs_types)
    sort_idx = np.argsort(obs_times)
    obs_times = obs_times[sort_idx]
    observer_codes = tuple(np.array(observer_codes, dtype=tuple)[sort_idx])
    obs_types = tuple(np.array(obs_types, dtype=tuple)[sort_idx])
    pastObsIdx = np.where(obs_times < ref_sol['t'])[0]
    futureObsIdx = np.where(obs_times > ref_sol['t'])[0]
    pastObsExist = len(pastObsIdx) > 0
    futureObsExist = len(futureObsIdx) > 0
    observerInfo = get_observer_info(observer_codes)
    if pastObsExist:
        tEvalPast = obs_times[pastObsIdx]
        tfPast = np.min(tEvalPast) - 1.0
        observerInfoPast = tuple(np.array(observerInfo, dtype=tuple)[pastObsIdx])
    if futureObsExist:
        tEvalFuture = obs_times[futureObsIdx]
        tfFuture = np.max(tEvalFuture) + 1.0
        observerInfoFuture = tuple(np.array(observerInfo, dtype=tuple)[futureObsIdx])
    # initialize the propagator
    tEvalUTC = True
    evalApparentState = True
    convergedLightTime = True
    propSimPast = prop.propSimulation(f"simulated_obs_past", ref_sol['t'], DEkernel, DEkernelPath)
    propSimFuture = prop.propSimulation(f"simulated_obs_future", ref_sol['t'], DEkernel, DEkernelPath)
    if pastObsExist:
        propSimPast.set_integration_parameters(tfPast, tEvalPast, tEvalUTC, evalApparentState, convergedLightTime, observerInfoPast)
        propSimPast.add_integ_body(targetBody)
    if futureObsExist:
        propSimFuture.set_integration_parameters(tfFuture, tEvalFuture, tEvalUTC, evalApparentState, convergedLightTime, observerInfoFuture)
        propSimFuture.add_integ_body(targetBody)
    # add events
    if events is not None:
        for event in events:
            t_event = event[0]
            dvx = event[1]
            dvy = event[2]
            dvz = event[3]
            multiplier = event[4]
            if t_event < ref_sol['t']:
                propSimPast.add_event(targetBody, t_event, [dvx, dvy, dvz], multiplier)
            else:
                propSimFuture.add_event(targetBody, t_event, [dvx, dvy, dvz], multiplier)
    # propagate
    if pastObsExist:
        propSimPast.preprocess()
        propSimPast.integrate()
    if futureObsExist:
        propSimFuture.preprocess()
        propSimFuture.integrate()
    # get the propagated solution
    if pastObsExist and futureObsExist:
        apparent_states_past = np.array(propSimPast.xIntegEval)
        apparent_states_future = np.array(propSimFuture.xIntegEval)
        apparent_states = np.vstack((apparent_states_past, apparent_states_future))
        radar_observations_past = np.array(propSimPast.radarObsEval)
        radar_observations_future = np.array(propSimFuture.radarObsEval)
        radar_observations = np.vstack((radar_observations_past, radar_observations_future))
    elif pastObsExist:
        apparent_states_past = np.array(propSimPast.xIntegEval)
        apparent_states = apparent_states_past
        radar_observations_past = np.array(propSimPast.radarObsEval)
        radar_observations = radar_observations_past
    elif futureObsExist:
        apparent_states_future = np.array(propSimFuture.xIntegEval)
        apparent_states = apparent_states_future
        radar_observations_future = np.array(propSimFuture.radarObsEval)
        radar_observations = radar_observations_future
    sim_obs_array = np.nan*np.ones((len(obs_times), 5))
    for i in range(len(obs_times)):
        sim_obs_array[i, 0] = obs_times[i]
        obs_info_len = len(observerInfo[i])
        if obs_info_len == 4:
            ra, dec = get_radec(apparent_states[i])
            sim_obs_array[i, 3] = obs_sigma_dict[obs_types[i]]
            sim_obs_array[i, 4] = obs_sigma_dict[obs_types[i]]
            sim_obs_array[i, 1] = ra
            if noise:
                ra_noise = np.random.normal(0, sim_obs_array[i, 3])
                sim_obs_array[i, 1] += ra_noise
            if bias:
                ra_bias = np.random.uniform(-sim_obs_array[i, 3]/2, sim_obs_array[i, 3]/2)
                sim_obs_array[i, 1] += ra_bias
            sim_obs_array[i, 2] = dec
            if noise:
                dec_noise = np.random.normal(0, sim_obs_array[i, 4])
                sim_obs_array[i, 2] += dec_noise
            if bias:
                dec_bias = np.random.uniform(-sim_obs_array[i, 4]/2, sim_obs_array[i, 4]/2)
                sim_obs_array[i, 2] += dec_bias
        elif obs_info_len == 9: # delay measurement
            sim_obs_array[i, 3] = obs_sigma_dict[obs_types[i]]
            sim_obs_array[i, 1] = radar_observations[i]
            if noise:
                delay_noise = np.random.normal(0, sim_obs_array[i, 3])
                sim_obs_array[i, 1] += delay_noise
            if bias:
                delay_bias = np.random.uniform(-sim_obs_array[i, 3]/2, sim_obs_array[i, 3]/2)
                sim_obs_array[i, 1] += delay_bias
        elif obs_info_len == 10: # doppler measurement
            sim_obs_array[i, 4] = obs_sigma_dict[obs_types[i]]
            sim_obs_array[i, 2] = radar_observations[i]
            if noise:
                doppler_noise = np.random.normal(0, sim_obs_array[i, 4])
                sim_obs_array[i, 2] += doppler_noise
            if bias:
                doppler_bias = np.random.uniform(-sim_obs_array[i, 4]/2, sim_obs_array[i, 4]/2)
                sim_obs_array[i, 2] += doppler_bias
    # split sim_obs_array and observer_codes into optical and radar
    optical_astrometry_obs_idx = np.where(np.array(obs_types) == 'astrometry')[0]
    optical_occultation_obs_idx = np.where(np.array(obs_types) == 'occultation')[0]
    optical_obs_idx = np.hstack((optical_astrometry_obs_idx, optical_occultation_obs_idx))
    radar_delay_obs_idx = np.where(np.array(obs_types) == 'delay')[0]
    radar_delay_hera_obs_idx = np.where(np.array(obs_types) == 'delay_hera')[0]
    radar_doppler_obs_idx = np.where(np.array(obs_types) == 'doppler')[0]
    radar_obs_idx = np.hstack((radar_delay_obs_idx, radar_delay_hera_obs_idx, radar_doppler_obs_idx))
    if len(optical_obs_idx) == 0:
        sim_obs_array_optical = None
        observer_codes_optical = None
    else:
        sim_obs_array_optical = sim_obs_array[optical_obs_idx]
        observer_codes_optical = tuple(np.array(observer_codes, dtype=tuple)[optical_obs_idx])
    if len(radar_obs_idx) == 0:
        sim_obs_array_radar = None
        observer_codes_radar = None
    else:
        sim_obs_array_radar = sim_obs_array[radar_obs_idx]
        observer_codes_radar = tuple(np.array(observer_codes, dtype=tuple)[radar_obs_idx])
    return sim_obs_array_optical, observer_codes_optical, sim_obs_array_radar, observer_codes_radar

def create_simulated_obs_arrays(simulated_traj_info, real_obs_arrays, simulated_obs_start_time, add_extra_simulated_obs, extra_simulated_obs_info, noise, bias):
    x_nom, covariance, events, target_radius, nongravInfo, DEkernel, DEkernelPath = simulated_traj_info
    obs_array_optical, observer_codes_optical, obs_array_radar, observer_codes_radar = real_obs_arrays
    if add_extra_simulated_obs:
        extra_simulated_optical_obs_times, extra_simulated_optical_obs_types, extra_simulated_radar_obs_times, extra_simulated_radar_obs_types = extra_simulated_obs_info
    optical_obs_times = obs_array_optical[:,0]
    radar_obs_times = obs_array_radar[:,0]
    simulated_optical_obs_idx = np.where(optical_obs_times >= simulated_obs_start_time)[0]
    simulated_optical_obs_times = tuple(optical_obs_times[simulated_optical_obs_idx])
    simulated_optical_obs_types = ['astrometry']*len(simulated_optical_obs_times)
    if add_extra_simulated_obs and extra_simulated_optical_obs_times is not None and extra_simulated_optical_obs_types is not None and len(extra_simulated_optical_obs_times) == len(extra_simulated_optical_obs_types):
        # add extra simulated optical obs times and types
        simulated_optical_obs_times = simulated_optical_obs_times + extra_simulated_optical_obs_times
        simulated_optical_obs_types = simulated_optical_obs_types + extra_simulated_optical_obs_types
        # add extra rows to obs_array_optical
        extra_simulated_optical_obs_array = np.nan*np.ones((len(extra_simulated_optical_obs_times), 5))
        obs_array_optical = np.vstack((obs_array_optical, extra_simulated_optical_obs_array))
        # add indices to simulated_optical_obs_idx
        simulated_optical_obs_idx = np.hstack((simulated_optical_obs_idx, np.arange(len(optical_obs_times), len(optical_obs_times)+len(extra_simulated_optical_obs_times))))
        # add extra rows to observer_codes_optical
        extra_simulated_optical_observer_codes = tuple(['']*len(extra_simulated_optical_obs_times))
        observer_codes_optical = observer_codes_optical + extra_simulated_optical_observer_codes
    simulated_radar_obs_idx = np.where(radar_obs_times >= simulated_obs_start_time)[0]
    simulated_radar_obs_times = tuple(radar_obs_times[simulated_radar_obs_idx])
    simulated_radar_obs_types = ['delay']*len(simulated_radar_obs_times)
    if add_extra_simulated_obs and extra_simulated_radar_obs_times is not None and extra_simulated_radar_obs_types is not None and len(extra_simulated_radar_obs_times) == len(extra_simulated_radar_obs_types):
        # add extra simulated radar obs times and types
        simulated_radar_obs_times = simulated_radar_obs_times + extra_simulated_radar_obs_times
        simulated_radar_obs_types = simulated_radar_obs_types + extra_simulated_radar_obs_types
        # add extra rows to obs_array_radar
        extra_simulated_radar_obs_array = np.nan*np.ones((len(extra_simulated_radar_obs_times), 5))
        obs_array_radar = np.vstack((obs_array_radar, extra_simulated_radar_obs_array))
        # add indices to simulated_radar_obs_idx
        simulated_radar_obs_idx = np.hstack((simulated_radar_obs_idx, np.arange(len(radar_obs_times), len(radar_obs_times)+len(extra_simulated_radar_obs_times))))
        # add extra rows to observer_codes_radar
        extra_simulated_radar_observer_codes = tuple(['']*len(extra_simulated_radar_obs_times))
        observer_codes_radar = observer_codes_radar + extra_simulated_radar_observer_codes
    simulated_obs_ref_sol = x_nom.copy()
    simulated_obs_ref_sol['mass'] = 0.0
    simulated_obs_ref_sol['radius'] = target_radius
    simulated_obs_ref_cov = covariance.copy()
    simulated_obs_event = events if events is not None else None
    simulated_obs_info = _generate_simulated_obs(simulated_obs_ref_sol, simulated_obs_ref_cov, nongravInfo, simulated_obs_event, simulated_optical_obs_times, simulated_optical_obs_types, simulated_radar_obs_times, simulated_radar_obs_types, DEkernel, DEkernelPath, noise, bias)
    simulated_obs_array_optical, simulated_observer_codes_optical, simulated_obs_array_radar, simulated_observer_codes_radar = simulated_obs_info
    if simulated_obs_array_optical is not None:
        obs_array_optical[simulated_optical_obs_idx,:] = simulated_obs_array_optical
        observer_codes_optical_temp = list(observer_codes_optical)
        for idx, code in enumerate(simulated_observer_codes_optical):
            observer_codes_optical_temp[simulated_optical_obs_idx[idx]] = code
        observer_codes_optical = tuple(observer_codes_optical_temp)
    if simulated_obs_array_radar is not None:
        obs_array_radar[simulated_radar_obs_idx,:] = simulated_obs_array_radar
        observer_codes_radar_temp = list(observer_codes_radar)
        for idx, code in enumerate(simulated_observer_codes_radar):
            observer_codes_radar_temp[simulated_radar_obs_idx[idx]] = code
        observer_codes_radar = tuple(observer_codes_radar_temp)
    return obs_array_optical, observer_codes_optical, obs_array_radar, observer_codes_radar
