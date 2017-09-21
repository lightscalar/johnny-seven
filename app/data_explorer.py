import sys
sys.path.append('../../mathtools')
from mathtools.utils import Vessel
from processor import *
from gazepoint_parser import *
import pylab as plt


def q(statement):
    # Return array indices where statement is true
    return nonzero(statement)[0]


if __name__ == '__main__':
    eye = Vessel('eye-scan-01.dat')
    scan = {'_id': 'hello'}

    flash_time = eye.data[0]
    raw_data = eye.data[1]
    obs = parse_data(raw_data)

    tser = generate_time_series(obs)
    
    t = np.array(tser['time'])
    dr = np.array(tser['right']['diameter'])

    # Find valid points
    idx = q(t>0)
    t = t[idx]
    dr = dr[idx]
    t_start = t.min()
    t -= t_start
    
    # Light flash time.
    flash_time = flash_time[1] - t_start

    plt.ion()
    plt.close('all')
    plt.plot(t, dr) 
    y_lim = plt.ylim()
    plt.plot([flash_time, flash_time], [0, 10], 'r--')
    plt.ylim(y_lim)


    

