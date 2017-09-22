import sys
sys.path.append('../../mathtools')
from mathtools.utils import Vessel
from mathtools.fit import *
from processor import *
from gazepoint_parser import *
import pylab as plt
from taut_string import taut_string


def q(statement):
    # Return array indices where statement is true
    return nonzero(statement)[0]


def extrema_in_range(t, v, mint, maxt):
    # Find time, index, and value.
    idx = q( (t>mint) * (t<maxt))
    t_ = t[idx]
    v_ = v[idx]
    idx_max = np.argmax(v_)
    idx_min = np.argmin(v_)
    t_min = t_[idx_min]
    t_max = t_[idx_max]
    v_max = v_.max()
    v_min = v_.min()
    idx_max += idx.min()
    idx_min += idx.min()
    return idx_min, idx_max, t_min, t_max, v_min, v_max


def process_raw_data(package, scan):
    # Process data to extract PLR parameters.
    flash_time = package[0]
    raw_data = package[1]
    scan['flash_time'] = flash_time[1]
    scan['raw_data'] = raw_data

    # Parse the raw data; extract time series.
    obs = parse_data(raw_data)
    tser = generate_time_series(obs)
    t = np.array(tser['time'])
    left = np.array(tser['left']['diameter'])
    right = np.array(tser['right']['diameter'])

    try:
        scan['left'] = extract_plr(t, left, flash_time, scan_id=scan['_id'], \
                which_eye='LEFT')
        scan['right'] = extract_plr(t, right, flash_time, scan_id=scan['_id'], \
                which_eye='RIGHT')
        scan['isSuccess'] = True
    except:
        print('Data Processing of Scan Failed')
        scan['isSuccess'] = False

    return scan


def extract_plr(t, dr, flash_time, scan_id='1234', which_eye='LEFT'):
    # Extract PLR parameters from provided time series.

    # Find valid points
    idx = q(t>0)
    t = t[idx]
    dr = dr[idx] * 1000
    t_start = t.min()
    t -= t_start
    dr = taut_string(dr, 0.01)
    
    # Fit with cubic splines
    idx = q( (t>7.0) * (t<12.0))
    t_ = t[idx]
    dr_ = dr[idx]
    f = Fit(t_, 100, basis_type='cubic-spline', reg_coefs=[0, 1e-2, 9e-3])
    r = f.fit(dr_)

    # Grab the latency time.
    try:
        roc = 1/((2 + 1 + (r.dy)**2)**(3/2)/np.abs(r.d2y))
    except:
        roc = inf

    roc = taut_string(roc, 0.10)

    peaks = []
    for itr, val in enumerate(roc):
        if (itr<1) or (itr==len(roc)-1):
            continue
        if val > roc[itr-1] and (val > roc[itr+1]):
            peaks.append(t_[itr])

    # Light flash time.
    closest_index = np.abs(t_ - flash_time[1])
    flash_idx = np.argmin(closest_index)
    flash_time = flash_time[1] - t_start

    # Starting amplitude.
    starting_amplitude = dr[flash_idx]

    # Find the peak in the curvature.
    peaks = np.array(peaks)
    peaks -= flash_time
    peaks = peaks[peaks>0.150]
    peak_time = peaks[0] + flash_time
    med_amplitude = np.median(dr_)
    std_amplitude = dr_.std()
    roc -= mean(roc)
    roc = roc * roc.std() * std_amplitude/5
    roc += med_amplitude
    latency = peak_time - flash_time
    print('Latency is {:0.3f}'.format(latency))

    # Minimum amplitude.
    idx_min, idx_max, t_min, t_max, v_min, v_max =\
            extrema_in_range(r.x, r.y, 7, 10)
    minimum_amplitude = v_min
    minimum_time = t_min
    delta_amplitude = starting_amplitude - minimum_amplitude
    average_speed = (delta_amplitude)/(minimum_time - peak_time)

    # Find the recovery time.
    recovery_amplitude = 0.75 * starting_amplitude
    idx_after_min = q(t>minimum_time)
    t_after_min = t[idx_after_min]
    amp_after_min = dr[idx_after_min]
    recovery_idx = q(amp_after_min >= recovery_amplitude)[0]
    if recovery_idx:
        recovery_time = t_after_min[recovery_idx] - flash_time
    else:
        recovery_time = -1

    package = {}
    package['latency'] = latency
    package['starting_diameter'] = starting_amplitude
    package['minimum_diameter'] = minimum_amplitude
    package['absolute_diameter_change'] = delta_amplitude
    package['relative_diameter_change'] = delta_amplitude/starting_amplitude
    package['average_speed'] = average_speed
    package['recovery_time'] = recovery_time

    plt.ioff()
    plt.close('all')
    plt.plot(r.x, r.y, color='#c62828', linewidth=3)
    plt.plot(t_, roc, color='#305580', linewidth=3, alpha=0.5)
    y_lim = plt.ylim([med_amplitude-3*std_amplitude, med_amplitude + std_amplitude])
    plt.plot([flash_time, flash_time], [0, 10], 'r--')
    plt.plot([peak_time, peak_time], [0, 10], 'r--')
    plt.xlim([7,12])
    plt.savefig('{}_{}.png'.format(scan_id, which_eye))
    return package


if __name__ == '__main__':
    eye = Vessel('eye-scan-04.dat')
    scan = {'_id': 'hello'}

    data = eye.data
    scan = process_raw_data(data, scan)
