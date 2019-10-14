import PySimpleGUI as sg
# import subprocess
import pathlib
import time
import ffmpeg

from auto_srt import audio_to_srt


layout = [[sg.Text('欢迎使用自动srt字幕生成')],
          [sg.Text('请选择输入视频或音频文件：'), sg.InputText(), sg.FileBrowse()],
          [sg.Text('请选择输出目录:'), sg.InputText(), sg.FileSaveAs()],
          [sg.Submit('提交')]]
(event, (source_filename, srt_path)) = sg.Window(
    'srt字幕自动生成工具').Layout(layout).Read()
print(event, source_filename)
src_path = pathlib.Path(source_filename)
wav_path = pathlib.Path(source_filename).with_suffix('.wav')
print(src_path, wav_path)
if src_path.suffix.lower() != '.wav' and not wav_path.exists():
    # notice_window = sg.Window('处理中...').Layout([[sg.Text('视频转换中，请耐心等待...', key='notice')]])
    # notice_window.Read(timeout=1)
    # notice_window.FindElement('notice').Update('视频转换中，请耐心等待...')
    sg.PopupNonBlocking('视频转换中...')
    ffmpeg.input(src_path.absolute()).output(filename=wav_path.absolute()).run()
    # subprocess.call(f'ffmpeg -i {src_path.absolute()} {wav_path.absolute()}', shell=True)
    print('ffmpeg done')
time.sleep(3)
# notice_window = sg.Window('处理中...').Layout([[sg.Text('字幕生成中，请耐心等待...', key='notice')]])
# notice_window.Read(timeout=1)
# notice_window.FindElement('notice').Update('字幕生成中，请耐心等待...')
sg.PopupNonBlocking('字幕生成中...')
audio_to_srt(wav_path, srt_path)
sg.Window('处理完成！').Layout([[sg.Text('完成！请在输出目录下找到.srt格式文件')], [sg.OK()]]).Read()
print('Done')
