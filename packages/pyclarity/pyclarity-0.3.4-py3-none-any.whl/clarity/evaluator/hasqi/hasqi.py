from clarity.evaluator.haspi import eb


def hasqi_v2(
    reference,
    reference_freq,
    processed,
    processed_freq,
    hearing_loss,
    equalisation=1,
    level1=65,
    silence_threshold=2.5,
    add_noise=0.0,
    segment_covariance=16,
):
    """
    Function to compute the HASQI version 2 quality index using the
    auditory model followed by computing the envelope cepstral
    correlation and BM vibration average short-time coherence signals.
    The reference signal presentation level for NH listeners is assumed
    to be 65 dB SPL. The same model is used for both normal and
    impaired hearing.

    Arguments:
        reference (np.ndarray): Clear input reference speech signal with no noise or
            distortion. If a hearing loss is specified, NAL-R equalization is optional
        reference_freq (int): Sampling rate in Hz for reference signal.
        processed (np.ndarray): Output signal with noise, distortion, HA gain, and/or
            processing.
        processed_freq (int): Sampling rate in Hz for processed signal.
        hearing_loss (np.ndarray): vector of hearing loss at the 6 audiometric
            frequencies [250, 500, 1000, 2000, 4000, 6000] Hz.
        equalisation (int): Mode to use when equalising the reference signal:
                1 = no EQ has been provided, the function will add NAL-R
                2 = NAL-R EQ has already been added to the reference signal
        level1: Optional input specifying level in dB SPL that corresponds to a
              signal RMS = 1. Default is 65 dB SPL if argument not provided.
        silence_threshold (float): Silence threshold sum across bands, dB above audio
            threshold. Default: 2.5
        add_noise (float): Additive noise in dB SL to conditiona cross-covariance.
            Default is 0.0
        segment_covariance (int): Segment size for the covariance calculation.
            Default is 16

    Returns:
        tuple(Combined, Nonlin, Linear, raw)
            Combined: Quality estimate is the product of the nonlinear and linear terms
            Nonlin: Nonlinear quality component = (cepstral corr)^2 x seg BM coherence
            Linear: Linear quality component = std of spectrum and spectrum slope
            raw: Vector of raw values = [CepCorr, BMsync5, Dloud, Dslope]

    James M. Kates, 5 August 2013.
    Translated from MATLAB to Python by Gerardo Roa Dabike, October 2022.
    """

    # Auditory model for quality
    # Reference is no processing or NAL-R, impaired hearing
    (
        reference_db,
        reference_basilar_membrane,
        processed_db,
        processed_basilar_membrane,
        reference_sl,
        processed_sl,
        freq_sample,
    ) = eb.ear_model(
        reference,
        reference_freq,
        processed,
        processed_freq,
        hearing_loss,
        equalisation,
        level1,
    )

    # Envelope and long-term average spectral features
    # Smooth the envelope outputs: 125 Hz sub-sampling rate
    reference_smooth = eb.env_smooth(reference_db, segment_covariance, freq_sample)
    processed_smooth = eb.env_smooth(processed_db, segment_covariance, freq_sample)

    # Mel cepstrum correlation using smoothed envelopes
    (
        average_cepstral_correlation,
        _individual_cepstral_correlations,
    ) = eb.mel_cepstrum_correlation(
        reference_smooth, processed_smooth, silence_threshold, add_noise
    )

    # Linear changes in the log-term spectra
    # dloud  vector: [sum abs diff, std dev diff, max diff] spectra
    # dnorm  vector: [sum abs diff, std dev diff, max diff] norm spectra
    # dslope vector: [sum abs diff, std dev diff, max diff] slope
    d_loud, _d_norm, d_slope = eb.spectrum_diff(reference_sl, processed_sl)

    # Temporal fine structure correlation measurements
    # Compute the time-frequency segment covariances
    (
        signal_cross_covariance,
        reference_mean_square,
        _processed_mean_square,
    ) = eb.bm_covary(
        reference_basilar_membrane,
        processed_basilar_membrane,
        segment_covariance,
        freq_sample,
    )

    # Average signal segment cross-covariance
    # avecov=weighted ave of cross-covariances, using only data above threshold
    # syncov=ave cross-covariance with added IHC loss of synchronization at HF
    silence_threshold = 2.5  # Threshold in dB SL for including time-freq tile
    _, ihc_sync_covariance = eb.ave_covary2(
        signal_cross_covariance, reference_mean_square, silence_threshold
    )
    basilar_membrane_sync5 = ihc_sync_covariance[
        4
    ]  # Ave segment coherence with IHC loss of sync

    # Extract and normalize the spectral features
    # Dloud:std
    d_loud = d_loud[1] / 2.5  # Loudness difference std
    d_loud = 1.0 - d_loud  # 1=perfect, 0=bad
    d_loud = min(d_loud, 1)
    d_loud = max(d_loud, 0)

    # Dslope:std
    d_slope = d_slope[1]  # Slope difference std
    d_slope = 1.0 - d_slope
    d_slope = min(d_slope, 1)
    d_slope = max(d_slope, 0)

    # Construct the models
    # Nonlinear model
    non_linear = (
        average_cepstral_correlation**2
    ) * basilar_membrane_sync5  # Combined envelope and temporal fine structure
    # Linear model
    linear = 0.579 * d_loud + 0.421 * d_slope  # Linear fit

    # Combined model
    combined = non_linear * linear  # Product of nonlinear x linear

    # Raw data
    raw = [average_cepstral_correlation, basilar_membrane_sync5, d_loud, d_slope]
    return combined, non_linear, linear, raw


def hasqi_v2_better_ear(
    reference_left,
    reference_right,
    processed_left,
    processed_right,
    sample_freq,
    audiogram_left,
    audiogram_right,
    audiogram_frequencies,
    level=100,
    audiogram_freq=None,
) -> float:
    """Better ear HASQI.

    Calculates HASQI for left and right ear and selects the better result.

    Args:
        reference_left (np.ndarray): left channel of reference signal
        reference_right (np.ndarray): right channel of reference signal
        reference_left (np.ndarray): left channel of processed signal
        reference_right (np.ndarray): right channel of processed signal
        sample_freq: sampling rate for both signal
        audiogram_l: left ear audiogram
        audiogram_r: right ear audiogram
        audiogram_cfs: audiogram frequencies
        level: level in dB SPL corresponding to RMS=1
        audiogram_freq: selected frequencies to use for audiogram

    Returns:
        float: beHASQI score

    Gerardo Roa Dabike, November 2022
    """
    # Default frequencies
    if audiogram_freq is None:
        audiogram_freq = [250, 500, 1000, 2000, 4000, 6000]

    # Adjust to match the frequencies
    adjusted_left = [
        audiogram_left[i]
        for i in range(len(audiogram_frequencies))
        if audiogram_frequencies[i] in audiogram_freq
    ]
    adjusted_right = [
        audiogram_right[i]
        for i in range(len(audiogram_frequencies))
        if audiogram_frequencies[i] in audiogram_freq
    ]

    score_left, _, _, _ = hasqi_v2(
        reference_left,
        sample_freq,
        processed_left,
        sample_freq,
        adjusted_left,
        equalisation=1,
        level1=level,
    )
    score_right, _, _, _ = hasqi_v2(
        reference_right,
        sample_freq,
        processed_right,
        sample_freq,
        adjusted_right,
        equalisation=1,
        level1=level,
    )

    return max(score_left, score_right)
