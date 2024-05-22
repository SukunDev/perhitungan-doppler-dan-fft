# Pola Suara Di Pengaruhi Efek Doppler

menentukan terendah dan tertinggi pada pola suara, baik normal maupun yang dipengaruhi efek doppler untuk selanjutnya dihitung FFT nya

<p align="center"><img src="assets/charts.PNG" width="50%"></img></p>

## Cloning

```bash
git clone https://github.com/SukunDev/perhitungan-doppler-dan-fft.git
cd perhitungan-doppler-dan-fft
```

## Buat virtual environment

```bash
python -m venv .venv
```

Masuk ke virtual environment

### Powershell

```bash
.venv/Scripts/activate.ps1
```

### CMD

```bash
cd .venv/Scripts
activate
cd ../..
```

### Git Bash

```bash
source .venv/Scripts/activate
```

## Install depedency

```bash
pip install -r requirements.txt
```

## Menjalankan Program

sebelum menjalankan program alangkah baik nya anda merubah beberapa baris kode di dalam main.py

```python

data, sampling_rate = sf.read('./sample/Data sample 1.wav') # masukkan sample audio
```

```python
# Kecepatan suara dalam udara (m/s)
speed_of_sound = 343.0

# Kecepatan sumber (positif jika mendekat, negatif jika menjauh)
source_speed = 20.0  # m/s, contoh nilai

# Kecepatan pendengar (positif jika mendekat, negatif jika menjauh)
listener_speed = 0.0  # m/s, contoh nilai
```

```python
df.to_excel('hasil_analisis_audio.xlsx', index=False) # rubah nama file excel sesuai dengan kesukaan anda
```

jika sudah jalan kan program dengan

```bash
python main.py
```
