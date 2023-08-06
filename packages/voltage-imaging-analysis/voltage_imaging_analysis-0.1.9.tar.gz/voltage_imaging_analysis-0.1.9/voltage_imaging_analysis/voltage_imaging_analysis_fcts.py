import numpy as np
import copy
import cv2
import scipy
import warnings
import skimage
from sklearn import linear_model
from matplotlib import pyplot as plt
import sys
from scipy import stats
import statistics
from scipy.spatial import distance
from numpy.lib.stride_tricks import as_strided

# timings analysis:
    # generate timeseries from stack 
    # segmentation
    # ... 
    # take a long time

def generate_timeseries_from_stack(stack_to_analyse, whiten_data=True, no_border_pixels=1):

    # segment image to get initial estimate of trace
    # use local correlation image for initial segmentations: expect pixels within cell to be more correlated with oneanother than noisy pixels outside cell
    local_correlation_img = compute_local_correlation_image(stack_to_analyse, no_neighbours=8, to_whiten_data=whiten_data)

    # remove edge artefact
    mask = np.zeros_like(local_correlation_img)
    mask[no_border_pixels:-no_border_pixels, no_border_pixels:-no_border_pixels] = 1

    img_to_segment_mask = copy.deepcopy(mask*local_correlation_img)

    init_timeseries = np.divide(np.matmul(stack_to_analyse.reshape(stack_to_analyse.shape[0], -1), np.ravel(img_to_segment_mask)), np.sum(img_to_segment_mask))

    if whiten_data is True:
        return whiten_trace(init_timeseries)

    else:
        return init_timeseries


def compute_local_correlation_image(data, no_neighbours=4, to_whiten_data=True):

    if to_whiten_data is True:
        whitened_data = whiten_data(data)
    else:
        whitened_data = data

    if no_neighbours==4:
        sz = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]).astype(np.float32)
        
    if no_neighbours==8:
        sz = np.ones((3, 3)).astype(np.float32)
        sz[1, 1] = 0

    if no_neighbours==24:
        sz = np.ones((5, 5)).astype(np.float32)
        sz[2, 2] = 0

    if no_neighbours==48:
        sz = np.ones((7, 7)).astype(np.float32)
        sz[3, 3] = 0

    local_correlation_img = whitened_data.copy()

    for idx, img in enumerate(local_correlation_img):
        local_correlation_img[idx] = scipy.ndimage.filters.convolve(img,sz,origin=0)

    norm = scipy.ndimage.filters.convolve(np.ones(whitened_data.shape[1:], dtype='float32'), sz, origin=0)

    local_correlation_img = np.divide(np.mean(local_correlation_img * whitened_data, axis=0), norm)

    return np.divide(local_correlation_img - np.min(local_correlation_img), np.max(local_correlation_img) - np.min(local_correlation_img))

def whiten_data(data):
    # subtract mean and divide by standard deviation
    # note assumption format of data is: t, x, y
    data = data.astype(np.float32)
    data = data - np.mean(data, axis=0)
    stdev_data = np.std(data, axis=0)
    stdev_data[stdev_data == 0] = np.inf
    whitened_data = np.divide(data, stdev_data)

    return whitened_data

def whiten_trace(trace):
    # subtract mean and divide by standard deviation
    # note assumption format of data is: t, x, y
    trace = trace.astype(np.float32)
    trace = trace - np.mean(trace)
    stdev_trace = np.std(trace)
    whitened_trace = np.divide(trace, stdev_trace)

    return whitened_trace

def generate_segmentation_mask(_img_to_segment, _disk_diameter=10, _dilation_diameter_coeff=1.2, _fill_gaps=False, _compute_anti_cell_mask=False):

    _threshold_value = skimage.filters.threshold_otsu(scipy.ndimage.gaussian_filter(_img_to_segment, _disk_diameter/2))

    _markers = np.zeros(_img_to_segment.shape, dtype=np.uint)
    _markers[_img_to_segment < _threshold_value] = 1
    _markers[_img_to_segment > _threshold_value] = 2

    # random walker segmentation
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        _labels = skimage.segmentation.random_walker(_img_to_segment, _markers, beta=130, mode='cg')

    _labels = _labels - 1

    # get rid of holes
    _labels_tmp = scipy.ndimage.binary_fill_holes(_labels).astype(int)

    if np.sum(_labels_tmp) > 0:
        if np.sum(_labels_tmp) < np.sum(np.ones_like(_labels_tmp)):
            _labels = _labels_tmp

    if _fill_gaps is True:
        # get rid of unconnected pixels
        _labels = skimage.morphology.erosion(_labels, skimage.morphology.disk(_disk_diameter/2))
        _segmentation_mask = skimage.morphology.dilation(_labels, skimage.morphology.disk(_dilation_diameter_coeff*_disk_diameter))

        if np.sum(_segmentation_mask) == 0:

            _segmentation_mask = _markers - 1
    else:
        _segmentation_mask = _labels

    # keep largest segment
    labels = skimage.measure.label(_segmentation_mask, return_num=False)
    _segmentation_mask = labels == np.argmax(np.bincount(labels.flat, weights=_segmentation_mask.flat))

    if _compute_anti_cell_mask is False:
        return _segmentation_mask

    else:
        _anti_cell_mask = copy.deepcopy(_segmentation_mask)
        _anti_cell_mask = scipy.ndimage.binary_fill_holes(_anti_cell_mask).astype(np.float64)
        _anti_cell_mask = np.abs(_anti_cell_mask - 1).astype(np.float64)

        return _segmentation_mask, _anti_cell_mask

    
def find_idxs_laser_on(init_timeseries, laser_on_off_border_pix, no_bins=4, return_unconcatenated_idxs=False, kernel_diameter=2):

    init_timeseries_filt = scipy.ndimage.gaussian_filter(init_timeseries, kernel_diameter)
    init_timeseries_filt = np.divide((init_timeseries_filt - np.min(init_timeseries_filt)), np.max(init_timeseries_filt) - np.min(init_timeseries_filt))

    # calculate transition indexes
    # histogram of intensity should have two prominant peaks, one for idxs where laser off, one where laser on
    # _time_series_histogram, bin_edges = np.histogram(_init_timeseries_filt, bins='auto')
    time_series_histogram, bin_edges = np.histogram(init_timeseries_filt, bins=no_bins)

    # Step 1: find indexes where laser turned on and off
    peak_idxs = np.argsort(-1*time_series_histogram)[:2]

    # peak corresponding to laser off will have lower pixel value
    # the average intensity of this peak corresponds to dark noise
    background_estimate = np.min(bin_edges[peak_idxs])

    # find idxs where counts above threshold
    condition = init_timeseries_filt - (background_estimate + (bin_edges[1] - bin_edges[0]))  > 0

    # take 1d derivative to find transitions light on/off or off/on
    diff_1d = np.diff(condition)
    idxs_laser_on_off = np.sort(np.nonzero(diff_1d)[0]) + 1 

    # find average length of epoch (note assuming same length here)
    no_epochs = np.rint(np.divide(idxs_laser_on_off.shape[0], 2)).astype(int)
    avg_no_frames_laser_on = np.ceil(np.mean(np.diff(idxs_laser_on_off.reshape(no_epochs, -1), axis=1))).astype(int)

    all_idxs_laser_on = [np.arange(idxs_laser_on_off[2*_epoch_idx] + laser_on_off_border_pix + 1, idxs_laser_on_off[2*_epoch_idx] + avg_no_frames_laser_on - laser_on_off_border_pix - 1) for _epoch_idx in np.arange(no_epochs)]

    # concatenate all indexes laser on
    if return_unconcatenated_idxs:
        return all_idxs_laser_on, no_epochs
    else:
        return np.concatenate(all_idxs_laser_on), no_epochs

def detrend_fluorescence_imaging_trace(initial_trace, filter_cut_on_hz, _fs=100):

    b, a = scipy.signal.butter(1, filter_cut_on_hz, "hp", fs=_fs)
    detrended_trace = np.single(scipy.signal.filtfilt(b, a, initial_trace, axis=0, padtype="odd", padlen=(3*(max(len(b), len(a))-1)))) + initial_trace[0]

    return detrended_trace

def detrend_voltage_imaging_data(data, filter_cut_on_hz, _fs=100):

    b, a = scipy.signal.butter(1, filter_cut_on_hz, "hp", fs=_fs)
    detrended_trace = np.single(scipy.signal.filtfilt(b, a, data, axis=0, padtype="odd", padlen=(3*(max(len(b), len(a))-1)))) + data[0, :, :]

    return detrended_trace


def update_segmentation_mask(_detrended_data, no_border_pixels=2):

    correlation_image = compute_local_correlation_image(_detrended_data, no_neighbours=8, to_whiten_data=True) 

    segmentation_mask = generate_segmentation_mask(correlation_image, _dilation_diameter_coeff=1.2, _fill_gaps=False, _compute_anti_cell_mask=False)

    # keep largest segment
    labels = skimage.measure.label(segmentation_mask, return_num=False)
    segmentation_mask = labels == np.argmax(np.bincount(labels.flat, weights=segmentation_mask.flat))

    # remove edge artefact
    _mask = np.zeros_like(segmentation_mask)
    _mask[no_border_pixels:-no_border_pixels, no_border_pixels:-no_border_pixels] = 1

    return _mask*segmentation_mask

def generate_pixel_weights(_denoised_data_tx1x2, _pixel_weighted_trace, _segmentation_mask):

    # ensure data cleared outside of segmentation
    _segmentation_mask_1 = np.expand_dims(_segmentation_mask, 0)

    if _segmentation_mask_1.shape[-1] == _denoised_data_tx1x2.shape[-1]:
        _denoised_data_tx1x2 = _denoised_data_tx1x2*_segmentation_mask_1
    else:
        _denoised_data_tx1x2 = _denoised_data_tx1x2*(_segmentation_mask_1.reshape(1,-1))

    _denoised_data_tx1x2 = _denoised_data_tx1x2 - np.mean(_denoised_data_tx1x2, axis=0)
    _denoised_data_tx1x2 = _denoised_data_tx1x2 - np.mean(_denoised_data_tx1x2, axis=0)

    pred = np.hstack((np.ones((_denoised_data_tx1x2.shape[0], 1), dtype=np.single), _denoised_data_tx1x2.reshape(_denoised_data_tx1x2.shape[0], -1)))

    lambdamax = np.single(np.linalg.norm(pred[:, 1:], ord='fro')**2)
    lambdas = lambdamax*np.logspace(-4, -2, 3)

    recon = np.hstack((np.ones((_denoised_data_tx1x2.shape[0], 1), dtype=np.single), _denoised_data_tx1x2.reshape(_denoised_data_tx1x2.shape[0], -1)))

    tr = np.single(copy.deepcopy(_pixel_weighted_trace))

    Ri = linear_model.Ridge(alpha=lambdas[2], fit_intercept=True, positive=True)

    Ri.fit(recon, tr)
    weights = Ri.coef_
    weights[0] = Ri.intercept_

    return weights

def background_segmentation(data, idxs_laser_on, border_pix=10):

    # calculate correlation image of entire stack
    img_to_segment = compute_local_correlation_image(data, no_neighbours=8)

    # segment background by simple thresholding 
    threshold_value = skimage.filters.threshold_otsu(scipy.ndimage.gaussian_filter(img_to_segment, 10))

    markers = np.zeros(img_to_segment.shape, dtype=np.uint)
    markers[img_to_segment < threshold_value] = 1
    markers[img_to_segment > threshold_value] = 0

    # keep largest segment
    labels = skimage.measure.label(markers)
    largestCC = labels == np.argmax(np.bincount(labels.flat)[1:]) + 1

    # erode 3x
    for _ in np.arange(5):
        if np.sum(largestCC) > 0:
            ero = skimage.morphology.binary_erosion(largestCC)
            if np.sum(ero) > 0:
                largestCC = ero

    corr_pixels_laser_on = compute_local_correlation_image(data[idxs_laser_on, :, :], no_neighbours=4)
    corr_pixels_laser_on[~largestCC] = np.inf
    
    min_no_background_pixels = np.max([np.rint(np.divide(np.sum(largestCC), 20)).astype(int), 20])

    # take the bottom 5 percent of correlated pixels
    valid_pix_idxs = np.unravel_index(np.argsort(corr_pixels_laser_on, axis=None)[:min_no_background_pixels], corr_pixels_laser_on.shape)

    least_corr_pixels = np.zeros_like(img_to_segment)
    least_corr_pixels[valid_pix_idxs] = 1

    mask = np.zeros_like(img_to_segment)

    while np.sum(least_corr_pixels*mask) < min_no_background_pixels:
        mask = np.zeros_like(img_to_segment)
        mask[border_pix:-border_pix, border_pix:-border_pix] = 1

        valid_pixels = least_corr_pixels*mask
        border_pix = border_pix - 1

    return valid_pixels

def find_f_idxs_df_idxs(avg_trace, no_epochs, df_border_pix=17, threshold=1e-3, gaussian_filter_kernel_pix=50): 

    # find peaks in derivative
    derivative_trace = np.square(np.diff(scipy.ndimage.gaussian_filter(avg_trace, gaussian_filter_kernel_pix)))
    peaks_derivative_trace, _ = scipy.signal.find_peaks(derivative_trace)

    # keep top 2*number epochs
    df_peaks = np.sort(peaks_derivative_trace[np.argsort(derivative_trace[peaks_derivative_trace])[::-1][:2*no_epochs]]).reshape(no_epochs, -1)

    # find df idxs
    all_df_idxs = []

    for _df in df_peaks:
        invert_derivative_trace = -1*derivative_trace[_df[0]:_df[-1]]
        invert_derivative_trace = invert_derivative_trace - np.min(invert_derivative_trace)

        df_idxs_no_border = np.arange(invert_derivative_trace.shape[0])[np.abs(invert_derivative_trace[np.argmax(invert_derivative_trace)] - invert_derivative_trace) - threshold < 0]
        df_idxs = df_idxs_no_border[df_border_pix:-df_border_pix]
        
        all_df_idxs.append(df_idxs + _df[0] + 1)

    # all_df_idxs = np.concatenate(all_df_idxs)

    # find f indexes
    all_f_idxs = np.array(list(set(list(np.arange(avg_trace.shape[0]))) - set(list(np.concatenate([np.arange(df_idxs[0] - 5*df_border_pix, df_idxs[1] + 5*df_border_pix) for df_idxs in df_peaks])))))

    return all_f_idxs, all_df_idxs


def find_df_idxs_spectrum(avg_trace, no_epochs, df_border_pix=3, threshold=1e-3): 

    # find peaks in derivative
    derivative_trace = np.square(np.diff(scipy.ndimage.gaussian_filter(avg_trace, 2)))
    peaks_derivative_trace, _ = scipy.signal.find_peaks(derivative_trace)

    # keep top 2*number epochs
    df_peaks = np.sort(peaks_derivative_trace[np.argsort(derivative_trace[peaks_derivative_trace])[::-1][:2*no_epochs]]).reshape(no_epochs, -1)

    return np.arange(df_peaks[0][0] + 1, df_peaks[0][-1])

def crop_or_pad_and_align_data(_data):

    try:
        _array_shapes = [item.shape[0] for sublist in _data for item in sublist]
        output = 0
    except IndexError:
        output = 1
        _array_shapes = [item.shape[0] for item in _data]

    # if all data same length, do nothing 
    if np.abs(np.std(_array_shapes) - 0) < 1e-15:
        if output == 0:
            return [item for sublist in _data for item in sublist]
        if output == 1:
            return [item for item in _data]

    else:
        # calculate "modal" trace
        mode_trace_idxs = np.array([idx for idx, _shape in enumerate(_array_shapes) if _shape == statistics.mode(_array_shapes)])
        outlier_idxs = np.array(list(set(list(np.arange(len(_array_shapes)))) - set(mode_trace_idxs)))

        modal_trace = np.mean([_data[idx][0] for idx in mode_trace_idxs], axis=0)

        modal_trace = np.divide(modal_trace - np.min(modal_trace), np.max(modal_trace) - np.min(modal_trace))

        for outlier_idx in outlier_idxs:
            if _array_shapes[outlier_idx] < modal_trace.shape[0]:
                _upd_array_a = np.lib.pad(_data[outlier_idx][0], (modal_trace.shape[0] -  _array_shapes[outlier_idx], 0), mode="edge")
                _upd_array_b = np.lib.pad(_data[outlier_idx][0], (0, modal_trace.shape[0] -  _array_shapes[outlier_idx]), mode="edge")
            else:
                _upd_array_a = _data[outlier_idx][0][_array_shapes[outlier_idx] - modal_trace.shape[0]:]
                _upd_array_b = _data[outlier_idx][0][:-(_array_shapes[outlier_idx] - modal_trace.shape[0])]

            _upd_array_a_norm = np.divide(_upd_array_a - np.min(_upd_array_a), np.max(_upd_array_a) - np.min(_upd_array_a))
            _upd_array_b_norm = np.divide(_upd_array_b - np.min(_upd_array_b), np.max(_upd_array_b) - np.min(_upd_array_b))

            _data[outlier_idx] = [[_upd_array_a, _upd_array_b][np.argmin(np.array([distance.euclidean(modal_trace, _upd_array_a_norm), distance.euclidean(modal_trace, _upd_array_b_norm)]))]]
        
    return [item for sublist in _data for item in sublist]


def pad_timeseries(_data):
    try:
        _array_shapes = [item.shape[0] for sublist in _data for item in sublist]
        output = 0
    except IndexError:
        output = 1
        _array_shapes = [item.shape[0] for item in _data]

    # if all data same length, do nothing 
    if np.abs(np.std(_array_shapes) - 0) < 1e-15:
        if output == 0:
            return [item for sublist in _data for item in sublist]
        if output == 1:
            return [item for item in _data]

    else:
        no_timepoints = np.max(_array_shapes)
        trace_idx_to_pad = np.argmin(_array_shapes)

        _data[trace_idx_to_pad] = np.lib.pad(_data[trace_idx_to_pad], (0, no_timepoints - _data[trace_idx_to_pad].shape[0]), mode="edge")

        if output == 0:
            return [item for sublist in _data for item in sublist]
        if output == 1:
            return [item for item in _data]


def find_f_idxs_df_idxs_sensitivity(avg_trace, no_epochs, df_border_pix=3, threshold=1e-3): 

    # find peaks in derivative
    derivative_trace = np.square(np.diff(scipy.ndimage.gaussian_filter(avg_trace, 2)))
    peaks_derivative_trace, _ = scipy.signal.find_peaks(derivative_trace)

    # keep top 2*number epochs - 2 (account for zero voltage step)
    df_peaks = np.sort(peaks_derivative_trace[np.argsort(derivative_trace[peaks_derivative_trace])[::-1][:2*no_epochs - 2]]).reshape(no_epochs - 1, -1)

    df_period = statistics.mode(np.ravel(np.diff(df_peaks, axis=1)))
    df_interval = statistics.mode(np.ravel(np.diff(df_peaks, axis=0)))

    # find df idxs
    all_df_idxs = np.array([np.arange(df_peaks[0][0] + epoch_idx*df_interval + 2, df_peaks[0][0] +  epoch_idx*df_interval + df_period - 1) for epoch_idx in np.arange(no_epochs)]).reshape(no_epochs, -1)

    # if more than two df idxs found, take two with most similar df values
    all_df_idxs_upd = []
    for df_idxs in all_df_idxs:
        if df_idxs.shape[0] > 2:
            min_diff_idx = np.argmin(np.diff(avg_trace[df_idxs]))
            df_idxs = [df_idxs[min_diff_idx], df_idxs[min_diff_idx + 1]]
        
        all_df_idxs_upd.append(df_idxs)

    # find f idxs 
    all_f_idxs = np.array(list(set(list(np.arange(avg_trace.shape[0]))) - set(list(np.concatenate(np.array([np.arange(df_peaks[0][0] + epoch_idx*df_interval - 1, df_peaks[0][0] +  epoch_idx*df_interval + df_period + 1) for epoch_idx in np.arange(no_epochs)]))))))

    # keep indexes within 2sd of the mean
    all_f_idxs = all_f_idxs[np.abs(avg_trace[all_f_idxs] - np.mean(avg_trace[all_f_idxs])) < 2*np.std(avg_trace[all_f_idxs])]

    return all_f_idxs, all_df_idxs_upd


def generate_spike_template(timeseries, min_distance=None, min_prominence=0.5):
    """
    Given a timeseries, finds the most prominant peaks (assumed to be action potentials), and takes their average (spike template)

    Arguments:
        timeseries: fluorescent trace assumed to contain action potential like transients
    Returns:
        spike_template: spike template (short timeseries)
        spike_positions: positions of peaks in timeseries
        spike_width: estimated width of spike in trace
    """

    # argsort_prominances = np.argsort(prominences)[::-1]
    # spike_idxs_for_template = peak_idxs[argsort_prominances]
    if min_distance is None:
        peak_idxs, _ = scipy.signal.find_peaks(timeseries, rel_height=0.5)
    else:
        peak_idxs, _ = scipy.signal.find_peaks(timeseries, rel_height=0.5, distance=min_distance)

    spike_idxs_for_template = peak_idxs[timeseries[peak_idxs] > min_prominence*min_prominencenp.max(timeseries[peak_idxs])]
    prominences = scipy.signal.peak_prominences(timeseries, peak_idxs)[0]

    # estimate peak width
    spike_width = np.ceil(np.nanmean(scipy.signal.peak_widths(timeseries, spike_idxs_for_template, rel_height=0.85)[0])).astype(int)
    half_spike_width = np.ceil(np.divide(spike_width - 1, 2)).astype(int) + 3

    # crop peaks (make sure that array large enough)
    spikes = []

    for spike_idx in spike_idxs_for_template:
        if (spike_idx - half_spike_width) > 0 & (spike_idx + half_spike_width + 1) < timeseries.shape[0]:

            cropped_ap = timeseries[spike_idx - half_spike_width:spike_idx + half_spike_width + 1]

            if spike_idx > 0 and len(spikes) > 0:
                if cropped_ap.shape[0] == spikes[0].shape[0]:
                    spikes.append(cropped_ap)
            else:
                spikes.append(cropped_ap)

    spike_template = np.mean(spikes, axis=0)

    peak_position = np.argmax(spike_template)

    spikes_upd = []
    spike_idxs_upd = []

    for spike_idx, spike in enumerate(spikes):
        
        if np.argmax(spike) == peak_position:
            spikes_upd.append(spike)
            spike_idxs_upd.append(spike_idxs_for_template[spike_idx])
    
    spike_template = np.mean(spikes_upd, axis=0)

    spike_template = np.divide(spike_template - np.min(spike_template), np.max(spike_template) - np.min(spike_template))

    return spike_template, spike_idxs_for_template, spike_width

def estimate_noise_and_baseline_ap_trace(timeseries, putative_peak_positions, putative_peak_width):
    """
    Given a timeseries, and estimated positions of peaks, generate an estimate of the noise as the std deviation of the portion of the trace which does not contain any peaks

    Arguments:
        timeseries: fluorescent trace assumed to contain action potential like transients
        putative_peak_positions: estimates (indexes) of action potential locations in the timeseries
    Returns:
        noise_est: estimate of noise level of timeseries 
        baseline_est: estimate of the baseline signal of timeseries 
    """
    # estimate noise of trace
    censor = np.zeros_like(timeseries)
    censor[putative_peak_positions] = 1

    censor = np.int16(np.convolve(censor.flatten(), np.ones([1, putative_peak_width]).flatten(), 'same'))
    censor = (censor < 0.125)

    noise_est = np.std(timeseries[censor])
    baseline_est = np.mean(timeseries[censor])

    return noise_est, baseline_est


def prewhiten_signal_fourier_domain(timeseries, noise_est):
    """
    Pre-whitens the signal in the frequency domain based on the noise spectrum estimated by the Welch method. 
    The prewhitened signal has noise distribution similar to the white noise.
    Based on code from: VolPy: Automated and scalable analysis pipelines for voltage imaging datasets

    Arguments:
        timeseries: trace (signal) for pre-whitening
        noise_est: estimate of noise level of timeseries 
    Returns:
        prewhitened_trace 
        
    """
    # find closest power of 2 and pad for efficient fourier transform
    N = (np.ceil(np.log2(timeseries.shape[0])).astype(int))

    # generate a power spectrum for the provided noise level
    noise_trace_for_psd = noise_est*np.random.randn(2**N)
    _, pxx = scipy.signal.welch(noise_trace_for_psd, fs=2 * np.pi, window=scipy.signal.get_window('hamming', 1000), nfft=2**N, detrend=False, nperseg=1000)

    # calculate corresponding scaling vector
    Nf2 = np.concatenate([pxx, np.flipud(pxx[1:-1])])
    scaling_vector = 1 / np.sqrt(Nf2)

    # rescale data
    cc = np.pad(copy.deepcopy(timeseries), (0, np.rint(2**N - timeseries.shape[0]).astype(int)), 'constant')
    dd = (cv2.dft(cc, flags=cv2.DFT_SCALE + cv2.DFT_COMPLEX_OUTPUT)[:,0,:]*scaling_vector[:,np.newaxis])[:,np.newaxis,:]

    # crop data and take inverse fourier transform
    prewhitened_trace = cv2.idft(dd)[:,0,0][:timeseries.shape[0]]

    return prewhitened_trace

def generate_spike_train_from_template(trace, spike_template, putative_peak_positions):
    """
    Given a spike template and putative peak positions, generate a clean trace. 
    Generally used for regression to update spatial filter.

    Arguments:
        trace: original timeseries
        spike_template: spike template, trace generated by averaging cropped APs
        putative_peak_positions: 
    Returns:
        spike_train: "clean" trace containing action potentials  
    """

    # generate a "noise-less" trace
    spike_train = np.zeros(trace.shape[0])

    # get rid of idxs that are too close to one another
    spike_idxs_upd = np.delete(putative_peak_positions, np.argwhere(np.ediff1d(putative_peak_positions) <= spike_template.shape) + 1)

    spike_train[spike_idxs_upd] = 1

    noiseless_spike_train = np.convolve(spike_train, spike_template, "same")[:trace.shape[0]]

    return noiseless_spike_train

def generate_spike_template_given_peaks(timeseries, spike_idxs, half_spike_width):
    """
    Similar function to <<generate_spike_template>>, but assumes peaks already found. 

    Arguments:
        timeseries: fluorescent trace assumed to contain action potential like transients
        spike_idxs: putative indexes of action potential like transients (list)
        half_spike_width: half width of action potential like transient
    Returns:
        spike_template: spike template (short timeseries)
    """

    # crop peaks (make sure that array large enough)
    spikes = []

    if len(spike_idxs) < 2:
        spike_idxs = [spike_idxs[0], spike_idxs[0]]

    for spike_idx in spike_idxs:
        if (spike_idx - half_spike_width) > 0 & (spike_idx + half_spike_width + 1) < timeseries.shape[0]:

            cropped_ap = timeseries[spike_idx - half_spike_width:spike_idx + half_spike_width + 1]

            if spike_idx > 0 and len(spikes) > 0:
                if cropped_ap.shape[0] == spikes[0].shape[0]:
                    spikes.append(cropped_ap)
            else:
                spikes.append(cropped_ap)

    spike_template = np.mean(spikes, axis=0)

    peak_position = np.argmax(spike_template)

    spikes_upd = []

    for spike_idx, spike in enumerate(spikes):
        
        if np.argmax(spike) == peak_position:
            spikes_upd.append(spike)

    spike_template = np.mean(spikes_upd, axis=0)

    spike_template = np.divide(spike_template - np.min(spike_template), np.max(spike_template) - np.min(spike_template))

    return spike_template

def shift_by_pad_or_crop(trace, shift):
    """
    Simple function to "translate" a trace by an integer number of timepoints by padding and then cropping appropriately

    Arguments:
        timeseries: e.g. fluorescence trace
    Returns:
        shift: amount by which
    """

    if shift < 0:
        trace_translated = np.lib.pad(trace, (0, -shift), mode="edge")[-shift:]
    if shift > 0:
        trace_translated = np.lib.pad(trace, (shift, 0), mode="edge")[:-shift]
    if shift == 0:
        trace_translated = trace
    
    return trace_translated
    

def pad_or_crop(trace_1, trace_2):
    """
    Given two traces, pad or crop them so same length (so can average them)

    Arguments:
        trace 1: template trace
        trace 2: trace to modify
    Returns:
        trace 2 modified so as to match trace 1
    """

    if trace_2.shape[0] > trace_1.shape[0]:
        trace_2 = trace_2[:trace_1.shape[0]]

    if trace_2.shape[0] < trace_1.shape[0]:
        trace_2 = np.lib.pad(trace_2, (0, trace_1.shape[0]-trace_2.shape[0]), mode="edge")
    
    return trace_2


def correlate_and_align_traces(master, trace, no_pix):
    if trace.shape[0] != no_pix:
        if trace.shape[0] > no_pix:
            trace = trace[:no_pix]
        else:
            trace = np.lib.pad(trace, (0, no_pix - trace.shape[0]), mode="edge")

    corr = np.correlate(trace, master, "full")

    lag = trace.shape[0] - np.argmax(corr)

    if lag < 0:
        trace = np.lib.pad(trace, (0, -1*lag))[-lag:]
    if lag > 0:
        trace = np.lib.pad(trace, (lag, 0))[:-lag]
    
    return trace, lag

class R_pca:
    """Class which implements R_pca to decompose matrix into low rank (L) and sparse (S) components.

    Args:
        D: array to be decomposed
        mu: not sure
        lmbda: not sure
    
    Returns:
        resized array a
    
    Raises:

    """

    def __init__(self, D, mu=None, lmbda=None):
        self.D = D
        self.S = np.zeros(self.D.shape)
        self.Y = np.zeros(self.D.shape)

        if mu:
            self.mu = mu
        else:
            self.mu = np.prod(self.D.shape) / (4 * np.linalg.norm(self.D, ord=1))

        self.mu_inv = 1 / self.mu

        if lmbda:
            self.lmbda = lmbda
        else:
            self.lmbda = 1 / np.sqrt(np.max(self.D.shape))

    @staticmethod
    def frobenius_norm(M):
        return np.linalg.norm(M, ord='fro')

    @staticmethod
    def shrink(M, tau):
        return np.sign(M) * np.maximum((np.abs(M) - tau), np.zeros(M.shape))

    def svd_threshold(self, M, tau):
        U, S, V = np.linalg.svd(M, full_matrices=False)
        return np.dot(U, np.dot(np.diag(self.shrink(S, tau)), V))

    def fit(self, tol=None, max_iter=1000, iter_print=100):
        iter = 0
        err = np.Inf
        Sk = self.S
        Yk = self.Y
        Lk = np.zeros(self.D.shape)

        if tol:
            _tol = tol
        else:
            _tol = 1E-7 * self.frobenius_norm(self.D)

        #this loop implements the principal component pursuit (PCP) algorithm
        #located in the table on page 29 of https://arxiv.org/pdf/0912.3599.pdf
        while (err > _tol) and iter < max_iter:
            Lk = self.svd_threshold(
                self.D - Sk + self.mu_inv * Yk, self.mu_inv)                            #this line implements step 3
            Sk = self.shrink(
                self.D - Lk + (self.mu_inv * Yk), self.mu_inv * self.lmbda)             #this line implements step 4
            Yk = Yk + self.mu * (self.D - Lk - Sk)                                      #this line implements step 5
            err = self.frobenius_norm(self.D - Lk - Sk)
            iter += 1
            if (iter % iter_print) == 0 or iter == 1 or iter > max_iter or err <= _tol:
                print('iteration: {0}, error: {1}'.format(iter, err))

        self.L = Lk
        self.S = Sk
        return Lk, Sk
    
def tile_array(a, b0, b1):
    """Resize array using nearest neighbour interpolation.

    Args:
        a: array to be resized
        b0: number of tiles in x1 direction
        b1: number of tiles in x2 direction
    
    Returns:
        resized array a
    
    Raises:

    """

    r, c = a.shape                                    
    rs, cs = a.strides                                
    x = as_strided(a, (r, b0, c, b1), (rs, 0, cs, 0)) 

    return x.reshape(r*b0, c*b1)    