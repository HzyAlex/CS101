import sys
import os
import pathlib
import shutil

from pydub.silence import detect_nonsilent
from pydub import AudioSegment
from pydub.silence import split_on_silence
from aip import AipSpeech


# 百度验证部分
APP_ID = '16008781'
API_KEY = 'BM5pSQasIIoYKi1D8yk6Smt8'
SECRET_KEY = 'U16yTM3rkqwH9LgGlXHKy7qmXjOiCkXw'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def split_on_silence_with_timeflag(audio_segment, min_silence_len=1000, silence_thresh=-16,
                                   keep_silence=100, seek_step=1):
    """
    audio_segment - original pydub.AudioSegment() object

    min_silence_len - (in ms) minimum length of a silence to be used for
        a split. default: 1000ms

    silence_thresh - (in dBFS) anything quieter than this will be
        considered silence. default: -16dBFS

    keep_silence - (in ms) amount of silence to leave at the beginning
        and end of the chunks. Keeps the sound from sounding like it is
        abruptly cut off. (default: 100ms)
    """

    not_silence_ranges = detect_nonsilent(
        audio_segment, min_silence_len, silence_thresh, seek_step)

    chunks = []
    starttime = []
    endtime = []
    for start_i, end_i in not_silence_ranges:
        start_i = max(0, start_i - keep_silence)
        end_i += keep_silence

        chunks.append(audio_segment[start_i:end_i])
        starttime.append(start_i)
        endtime.append(end_i)

    return chunks, starttime, endtime


# 将音频转换为wav
def gotwave(audio, silent, cache_path):
    new = AudioSegment.empty()
    for inx, val in enumerate(audio):
        new = val + silent
        new.export(cache_path / f'{inx}.wav', format='wav')


# 毫秒换算 根据需要只到分
def ms2s(ms):
    mspart = ms % 1000
    mspart = str(mspart).zfill(3)
    spart = (ms//1000) % 60
    spart = str(spart).zfill(2)
    mpart = (ms//1000)//60
    mpart = str(mpart).zfill(2)

    # srt的时间格式
    stype = "00:"+mpart+":"+spart+","+mspart
    return stype

# 读取切割后的文件


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 语音识别


def audio2text(wavsample):
    rejson = client.asr(wavsample, 'wav', 16000, {'dev_pid': 1536, })
    if (rejson['err_no'] == 0):
        result = rejson['result'][0]
    else:
        result = "erro"+str(rejson['err_no'])
    return result


# 输出字幕
def text2str(inx, text, starttime, endtime):
    if 'erro' in text:
        text = '请手工输入字幕'
    strtext = str(inx)+'\n'+ms2s(starttime)+' --> ' + \
        ms2s(endtime)+'\n'+text+'\n'+'\n'
    return strtext


# 读写文件
def strtxt(text, srt_path):
    with open(srt_path, 'a', encoding='utf-8') as fp:
        fp.write(text)
        fp.close()


def audio_to_srt(audio_path, srt_path):
    if isinstance(audio_path, str):
        audio_path = pathlib.Path(audio_path)
    pro_path = audio_path.parent
    if isinstance(srt_path, str):
        srt_path = pathlib.Path(srt_path)
    cache_path = pro_path / 'ats_cache'
    cache_path.mkdir(exist_ok=True)
    sound = AudioSegment.from_wav(audio_path)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)

    # 切割音频
    min_silence_len = 1000
    silence_thresh = -32
    pieces, start_t, end_t = split_on_silence_with_timeflag(
        sound, min_silence_len, silence_thresh)
    silent = AudioSegment.silent(duration=1000)

    gotwave(pieces, silent, cache_path)
    for inx, val in enumerate(pieces):
        wav = get_file_content(cache_path / f'{inx}.wav')
        text = audio2text(wav)
        text2 = text2str(inx, text, start_t[inx], end_t[inx])
        strtxt(text2, srt_path)
        print(str(round((inx/len(pieces))*100))+'%')
    shutil.rmtree(cache_path.absolute())


if __name__ == '__main__':
    audio_to_srt('/Users/hzyalex/Alex/Coding/title/test.flv')
