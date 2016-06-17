## @package fingerprints
#  Functions for generating fingerprints.
#
#  Some code based on:
#  https://github.com/worldveil/dejavu/blob/master/dejavu/fingerprint.py
##

from pydub import AudioSegment

import numpy as np
import matplotlib.mlab as mlab
import pylab
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)

import os
import md5
from config import *

def generateSpectogram(song):
    """
        Generates spectogram for a song.
        Args:
            song: AugioSegement of song of which spectogram should be created.
        Returns:
            Spectrum from matplotlib.specgram with scale changed to logarithmic.
    """

    song = song.set_channels(1) # sample only one channel
    # song = song.set_frame_rate(FREQ)
    # song = song.low_pass_filter(FREQ/2) # don't use too high frequencies

    frameRate = song.frame_rate
    frames = pylab.fromstring(song.raw_data, 'Int16')

    # generate spectogram
    spectrum, freqs, t = mlab.specgram(frames, Fs=frameRate, NFFT=DATA_POINTS, noverlap=NUM_OVER)

    # change to log scale
    spectrum = 10 * np.log2(spectrum)
    spectrum[spectrum == -np.inf] = 0

    return spectrum

def get2DPeaks(arr2D):
    """
        Generates peaks of a spectogram.
        Args:
            arr2D: spectogram.
        Returns:
            List of pairs (time, frequency) of peaks.
    """

    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our fliter shape
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood,
                                       border_value=1)

    # Boolean mask of arr2D with True at peaks
    detected_peaks = local_max - eroded_background

    # extract peaks
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > AMP_MIN]  # freq, time, amp

    # get indices for frequency and time
    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]

    return zip(frequency_idx, time_idx)

def getHashes(peaks):
    """
        Generates hashes of peaks.
        Args:
            peaks: list of pairs (time, frequenct) of peaks.
        Returns:
            List of pairs (hash, time).
    """

    res = []

    for i in range(0, len(peaks)):
        for j in range(i+1, min(len(peaks), i+NUM_OF_PEAKS+1)):
            f1 = peaks[i][0]
            f2 = peaks[j][0]
            t1 = peaks[i][1]
            t2 = peaks[j][1]

            if t2-t1 <= MAX_TIME_DIFF:
                res.append((md5.md5(str(f1)+str(f2)+str(t2-t1)).hexdigest(), t1))

    return res

def generateFingerprints(path, startTime=0, endTime=60000):
    """
        Calculates array of pairs (hash, time) for a song in a given path.
        By default samples first minute of a song.
        Args:
            path: path to song.
            startTime (Optional): time from which fingerprinting should start.
            endTime (Optional): time at which fingerprinting should end.
        Returns:
            List of pairs (hash, time).
            Empty list if path does not contain a valid music file.
    """

    filename, fileExtension = os.path.splitext(path)
    fileExtension = fileExtension[1:]

    try:
        song = AudioSegment.from_file(path, fileExtension)
        song = song[startTime : endTime]
    except:
        # Couldn't open song correctly
        return []

    spectrum = generateSpectogram(song)
    peaks = get2DPeaks(spectrum)
    fingerprints = getHashes(peaks)

    # print("Number of fingerprints " + str(len(fingerprints)))

    return fingerprints
