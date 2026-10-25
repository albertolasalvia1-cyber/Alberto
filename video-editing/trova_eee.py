"""Trova vocali tenute a lungo (es. "eeee"): voce continua con timbro stabile per >= MIN s."""
import subprocess, sys, numpy as np
path, MIN = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0.4
sr = 16000
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'],
                                 capture_output=True, check=True).stdout, np.float32)
hop, win = 160, 640  # 10 ms / 40 ms
n = (len(x) - win) // hop
frames = np.lib.stride_tricks.as_strided(x, (n, win), (x.strides[0] * hop, x.strides[0])) * np.hanning(win)
spec = np.abs(np.fft.rfft(frames, axis=1))[:, :200]          # 0-5 kHz
rms = np.sqrt((frames ** 2).mean(1))
db = 20 * np.log10(rms + 1e-9)
voiced = db > np.percentile(db, 60) - 6
norm = spec / (np.linalg.norm(spec, axis=1, keepdims=True) + 1e-9)
sim = (norm[1:] * norm[:-1]).sum(1)                           # somiglianza tra frame consecutivi
# stabilità su finestra di 100 ms
k = 10
stab = np.convolve(sim, np.ones(k) / k, mode='same')
good = voiced[1:] & (stab > 0.93)
runs, start = [], None
for i, g in enumerate(np.append(good, False)):
    if g and start is None: start = i
    if not g and start is not None:
        if (i - start) * hop / sr >= MIN: runs.append((start * hop / sr, i * hop / sr))
        start = None
for a, b in runs:
    print(f"{a:7.2f}-{b:7.2f}  ({b - a:.2f}s)")
