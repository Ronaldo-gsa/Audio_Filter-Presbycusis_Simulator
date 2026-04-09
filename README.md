# Audio Filter Analysis Project - Presbycusis Simulation

Developed by **Ronaldo Araújo**, this project applies digital signal processing techniques to simulate the effects of **Presbycusis** using the low-pass filter [**Butterworth**](https://en.wikipedia.org/wiki/Butterworth_filter) . The code processes audio files to demonstrate how high-frequency hearing loss affects sound perception.

---

## What is Presbycusis?
[**Presbycusis**](https://en.wikipedia.org/wiki/Presbycusis) is a progressive, irreversible sensorineural hearing loss caused by the natural aging and degeneration of the inner ear. It typically affects both ears equally and is most pronounced at high frequencies, making it difficult to distinguish specific speech sounds or high-pitched noises. This project simulates that experience by using a low-pass filter to remove frequencies above a specific threshold.

The main characteristic of Presbycusis is the difficulty in hearing **high-frequency sounds**. In practical terms, this makes it hard to distinguish certain speech sounds and hear high-pitched noises. By using a low-pass filter, this project mimics that experience by removing frequencies above a specific threshold.

---

## Dependencies

To run this script, you need Python installed along with the following libraries:
* **NumPy**
* **Matplotlib**
* **SciPy**

You can install them via terminal using:

```bash
pip install numpy matplotlib scipy
```

---

## How the Code Works
1.  **Audio Input:** The script reads a `.wav` file and extracts the sample rate and raw data.
2.  **Mono Conversion:** It checks if the audio is stereo. If so, it converts it to mono to simplify the filtering process.
3.  **Normalization:** The signal is converted to a float format ranging from `-1.0` to `1.0` to ensure mathematical precision during processing.
4.  **Butterworth Filter:** An 8th-order Butterworth low-pass filter is created. It is set by default to a **3000Hz** cutoff frequency, meaning frequencies above this point are significantly attenuated.
5.  **FFT Analysis:** The script calculates the **Fast Fourier Transform (FFT)** for both the original and filtered signals. This allows us to see the "frequency fingerprint" of the audio.
6.  **Visualization:** A graph is generated comparing the original and filtered spectrum, highlighting the cutoff point.

---

## Usage
This script is compatible with any audio file in `.wav` format. To use your own file:

1.  Place your audio file in the `audio_files/` folder (or update the path in the code).
2.  Change the `audio_path` variable to match your filename.
3.  Adjust the `freq_cut_off` variable if you want to simulate different levels of hearing loss.
4.  Run the script to generate the filtered file and view the analysis.

> [!NOTE]
> The output file are automatically saved as `filtered_audio_[freq]Hz.wav`.
