from WebApi.wakeUpAndStt import WakeUp,Speak2Text,Play
from Audio.Monitor import Monitor
from NLP.CutWords import CutWords
from WebApi.TTS import TTS
from WebApi.Tuling import Tuling
from time import time
from Contrl import DeviceContrl

room = ["客厅", "厨房", "洗手间"]
sdevice = ["灯",  "门", "窗帘", "电视", "扫地机器人", "微波炉", "冰箱"]
idevice = ["温度", "湿度", "气温", "水流", "桩点1", "桩点2", "桩点3"]
device_list = ["灯", "微波炉", "窗帘"]
state_list = ["打开 开 ", "关闭 关"]

test_device = {"厨房/灯": {"ID": "0010", "state": False, "pin": 18},
                   "客厅/电视": {"ID": "0060", "state": False, "pin": 35},
                   "客厅/灯": {"ID": "0060", "state": False, "pin": 35}}

startTime = time()
clearTime = 0
# 语音唤醒
wp = WakeUp()
# 监听录音机
mr = Monitor(3, 30)
# 语音转文字
s2t = Speak2Text()
# 文字转语音
tts = TTS()
# 语义分割
hw = CutWords(room, sdevice, idevice)
# 文字转语音
tts = TTS()
# 图灵接口
tl = Tuling("00012346")
# 设备控制模块
cf = DeviceContrl(test_device)



'''
------------------------SIGNAL-------------------------
'''
# 语音唤醒signal
AUDIO_SIGNAL = False