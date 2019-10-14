from pydub import AudioSegment
import sys
import os
from pydub.silence import split_on_silence
from aip import AipSpeech

#百度验证部分
APP_ID = '16008781'
API_KEY = 'BM5pSQasIIoYKi1D8yk6Smt8'
SECRET_KEY = 'U16yTM3rkqwH9LgGlXHKy7qmXjOiCkXw'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#读取音频 预处理
sound=AudioSegment.from_wav('test.wav')
sound=sound.set_frame_rate(16000)
sound=sound.set_channels(1)

#切割音频
min_silence_len=10
silence_thresh=-50
pieces,start_t,end_t=split_on_silence(sound,min_silence_len,silence_thresh)
silent = AudioSegment.silent(duration=1000)
#将音频转换为wav
def gotwave(audio):
    new = AudioSegment.empty()
    for inx,val in enumerate(audio):
        new=val+silent
        new.export('/Users/hzyalex/Alex/Coding/title/%d.wav' % inx,format='wav')    

#毫秒换算 根据需要只到分
def ms2s(ms):
    mspart=ms%1000
    mspart=str(mspart).zfill(3)
    spart=(ms//1000)%60
    spart=str(spart).zfill(2)
    mpart=(ms//1000)//60
    mpart=str(mpart).zfill(2)
    
    #srt的时间格式
    stype="00:"+mpart+":"+spart+","+mspart
    return stype
#读取切割后的文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

#语音识别
def audio2text(wavsample):
    rejson=client.asr(wavsample, 'wav', 16000, {'dev_pid': 1536,})
    if (rejson['err_no']==0):
        result=rejson['result'][0]
    else:
        result="erro"+str(rejson['err_no'])   
    return result

    
#输出字幕
def text2str(inx,text,starttime,endtime):
    strtext=str(inx)+'\n'+ms2s(starttime)+' --> '+ms2s(endtime)+'\n'+text+'\n'+'\n'
    return strtext

#读写文件
def strtxt(text):
    with open('/Users/hzyalex/Alex/Coding/title/yo.txt','a') as fp:
        fp.write(text)
        fp.close()
        

    
#main
if __name__ == '__main__':
    gotwave(pieces)
    for inx,val in enumerate(pieces):
        wav=get_file_content('/Users/hzyalex/Alex/Coding/title/%d.wav' % inx)
        text=audio2text(wav)
        text2=text2str(inx,text,start_t[inx],end_t[inx])
        strtxt(text2)
        print(str(round((inx/len(pieces))*100))+'%')

