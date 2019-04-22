from time import time
from threading import Thread
import SignalControlCenter as sc

class Main:

    def __init__(self):
        self.startTime = sc.startTime
        self.clearTime = sc.clearTime
        # 语音唤醒
        self.wp = sc.wp
        # 监听录音机
        self.mr = sc.mr
        # 语音转文字
        self.s2t = sc.s2t
        # 文字转语音
        self.tts = sc.tts
        # 语义分割
        self.hw = sc.hw
        # 图灵接口
        self.tl = sc.tl
        # 设备控制模块
        self.cf = sc.cf

    def run(self):
        for phrase in self.wp.speech:
            str_phrase = str(phrase).split(" ")
            print ("唤醒识别 : ", str_phrase)
            if ('FRIDAY' in str_phrase):
                if sc.AUDIO_SIGNAL is False:
                    sc.AUDIO_SIGNAL = True
                    Thread(target=self.entrance).start()
        clearTime = time()

    def entrance(self):
        command = False
        # 成功唤醒
        flow = self.mr.recording()
        result = self.s2t.get_text_by_flow(flow)
        print("语音识别 ： ", result)
        if result is not None:
            # 成功采集到声音
            if self.hw.intention(result) == None or self.hw.intention(result) == False:
                result = self.tl.tail(result)
                print("Turing 回复 ： ", result)
            else:
                command = True
        else:
            # 第一次没有采集到声音
            sc.Play("./material/您说，我在听.wav", False)
            flow = self.mr.recording()
            result = self.s2t.get_text_by_flow(flow)
            print("语音识别 ： ", result)
            if result is not None:
                # 成功采集到声音
                if self.hw.intention(result) == None or self.hw.intention(result) == False:
                    result = self.tl.tail(result)
                    print("Turing 回复 ： ", result)
                else:
                    command = True
            else:
                # 第二次未采集到声音
                sc.Play("./material/抱歉，我没有听到任何指令，请检查麦克风.wav", False)
                exit()
        if command:
            success_device = ""
            error_device = ""
            for command in self.hw.intention(result):
                if self.cf.switchByName(command[0], command[1])[1]:
                    success_device += command[0] + "、"
                else:
                    error_device += command[0] + "、"
            if len(success_device) > 0:
                print("家居控制模块 成功打开： ", success_device)
                self.tts.play("收到," + success_device[:-1] + "已打开")
            if len(error_device) > 0:
                print("家居控制模块 打开失败： ", error_device)
                self.tts.play(error_device[:-1] + "已处于打开或关闭状态")
        else:
            self.tts.play(result)
        sc.AUDIO_SIGNAL = False

if __name__ == '__main__':
    a = Main()
    a.run()
