import soundfile as sf
from inaSpeechSegmenter import Segmenter
import speech_recognition as sr
import glob, pyopenjtalk, librosa
#pyopenjtalkの環境構築が必要

def wav_read(path):
    wave, fs = librosa.core.load(path, sr =  22050, mono = True)
    return wave, fs

if __name__ == "__main__":
    source_file_path = "source_file_folder/*"
    seg_model = Segmenter()
    r = sr.Recognizer()
    surp = 0.2
    num = 0
    f = open('corpusfilepath', 'w')

    for source in glob.glob(source_file_path):
        wave, fs = wav_read(source)
        seg_data = seg_model(source)
        for cat, start, end in seg_data:
            if cat == "male":
                wave_trimed = wave[round((start - surp) * fs):round((end + surp) * fs)]
                save_file = "save_path/" + str(num).zfill(4) + ".wav"
                sf.write(save_file, wave_trimed, fs, subtype = "PCM_16")
                try:
                    with sr.AudioFile(save_file) as audiosource:
                        audio = r.record(audiosource)
                        txt = r.recognize_google(audio, language = 'ja-JP')
                        f.write(save_file + "|" + pyopenjtalk.g2p(txt, kana = False).replace('pau', ',').replace('', '') + "." + "\n")
                        num += 1
                except:
                    pass
    f.close()