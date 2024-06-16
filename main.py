from libs import AudioAnalyzer, Plotter, SpeedPredictor
import argparse
import os


parser = argparse.ArgumentParser(
    description="Perhitungan fft dan doppler effect",
    usage="%(prog)s [options] audio_sample operasi -o hasil_analisi_audio\nexample: python main.py 'sample/Data sample 1.wav' spectrum -o hasil_analisi_audio\n         python main.py 'sample/Data sample 1.wav' 3d_spectrum\n         python main.py 'sample/Data sample 1.wav' plot_speed"
)


parser.add_argument(
    'audio_sample',
    type=str,
    help='audio sample yang ingin di perhitungkan'
)

parser.add_argument(
    'operasi',
    type=str,
    help='operasi yang di butuhkan\nlist: spectrum, 3d_spectrum'
)

parser.add_argument(
    '-o',
    '--output',
    nargs='?',
    type=str,
    help='save to excel'
)

args = parser.parse_args()
if args.operasi == "spectrum":
    if not os.path.isfile(args.audio_sample):
        raise Exception("data sample not found")
    analyzer = AudioAnalyzer(args.audio_sample)
    fft_segments = analyzer.compute_fft()
    plotter = Plotter(fft_segments)
    plotter.plot_spectrum()
    if args.output:
        results = analyzer.analyze_frequency_ranges(fft_segments)
        analyzer.save_results_to_excel(results, filename=f"{args.output}.xlsx")
elif args.operasi == "3d_spectrum":
    analyzer = AudioAnalyzer(args.audio_sample)
    fft_segments = analyzer.compute_fft()
    plotter = Plotter(fft_segments)
    plotter.plot_3d_spectrum()
elif args.operasi == "plot_speed":
    analyzer = AudioAnalyzer(args.audio_sample)
    fft_segments = analyzer.compute_fft()
    predictor = SpeedPredictor(fft_segments)
    predictor.plot_average_spectrum()

else:
    parser.error("operasi yang di butuhkan\nlist: spectrum\n      3d_spectrum\n      plot_speed")