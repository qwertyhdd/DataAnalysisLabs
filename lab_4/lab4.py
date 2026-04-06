import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

init_amplitude = 1
init_frequency = 1
init_phase = 0
init_noise_mean = 0
init_noise_cov = 0.2
init_filter_cutoff = 0.05
t = np.linspace(0, 10, 1000)

noise = np.random.normal(init_noise_mean, init_noise_cov, len(t))
prev_mean = init_noise_mean
prev_cov = init_noise_cov

def harmonic(amplitude, frequency, phase):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)


def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    base = harmonic(amplitude, frequency, phase)
    if show_noise:
        return base + noise
    return base


def apply_filter(signal, cutoff):
    b, a = butter(3, cutoff)
    return filtfilt(b, a, signal)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.45)

clean_signal = harmonic(init_amplitude, init_frequency, init_phase)
noisy_signal = harmonic_with_noise(init_amplitude, init_frequency, init_phase,
                                   init_noise_mean, init_noise_cov, True)
filtered_signal = apply_filter(noisy_signal, init_filter_cutoff)

line_clean, = ax.plot(t, clean_signal, label='Clean')
line_noisy, = ax.plot(t, noisy_signal, label='Noisy')
line_filtered, = ax.plot(t, filtered_signal, label='Filtered')

ax.set_title("Harmonic Function with Noise and Filtering")
fig.text(
    0.01, 0.01,
    "Controls:\n"
    "- Sliders: change signal and noise parameters\n"
    "- Show Noise: toggle noise on/off\n"
    "- Filter Cutoff: adjust filtering\n"
    "- Reset: restore default values",
    fontsize=10,
    verticalalignment='bottom'
)
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.legend(loc='upper right')

ax_amp = plt.axes([0.25, 0.35, 0.65, 0.03])
ax_freq = plt.axes([0.25, 0.30, 0.65, 0.03])
ax_phase = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_noise_mean = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_noise_cov = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_filter = plt.axes([0.25, 0.10, 0.65, 0.03])

s_amp = Slider(ax_amp, 'Amplitude', 0.1, 5, valinit=init_amplitude)
s_freq = Slider(ax_freq, 'Frequency', 0.1, 5, valinit=init_frequency)
s_phase = Slider(ax_phase, 'Phase', 0, 2*np.pi, valinit=init_phase)
s_noise_mean = Slider(ax_noise_mean, 'Noise Mean', -1, 1, valinit=init_noise_mean)
s_noise_cov = Slider(ax_noise_cov, 'Noise Cov', 0.01, 1, valinit=init_noise_cov)
s_filter = Slider(ax_filter, 'Filter Cutoff', 0.01, 0.2, valinit=init_filter_cutoff)

ax_check = plt.axes([0.05, 0.5, 0.15, 0.1])
check = CheckButtons(ax_check, ['Show Noise'], [True])
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
btn_reset = Button(ax_reset, 'Reset')

def update(val):
    global noise, prev_mean, prev_cov

    amp = s_amp.val
    freq = s_freq.val
    phase = s_phase.val
    mean = s_noise_mean.val
    cov = s_noise_cov.val
    cutoff = s_filter.val
    show_noise = check.get_status()[0]

    if mean != prev_mean or cov != prev_cov:
        noise = np.random.normal(mean, cov, len(t))
        prev_mean = mean
        prev_cov = cov

    clean = harmonic(amp, freq, phase)
    noisy = harmonic_with_noise(amp, freq, phase, mean, cov, show_noise)
    filtered = apply_filter(noisy, cutoff)

    line_clean.set_ydata(clean)
    line_noisy.set_ydata(noisy)
    line_filtered.set_ydata(filtered)

    fig.canvas.draw_idle()

def reset(event):
    global noise, prev_mean, prev_cov

    s_amp.reset()
    s_freq.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_cov.reset()
    s_filter.reset()

    noise = np.random.normal(init_noise_mean, init_noise_cov, len(t))
    prev_mean = init_noise_mean
    prev_cov = init_noise_cov

s_amp.on_changed(update)
s_freq.on_changed(update)
s_phase.on_changed(update)
s_noise_mean.on_changed(update)
s_noise_cov.on_changed(update)
s_filter.on_changed(update)

check.on_clicked(update)
btn_reset.on_clicked(reset)

plt.show()
