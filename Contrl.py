class DeviceContrl:

    def __init__(self, device_dic):
        '''
        device = {"device name":{ID:010101010101,state:True/False,pin:int}}
        '''
        self.device = device_dic
        self.LAMP = False
        self.FAN = False
        self.TEMPERRUTURE = None  # '设备未连接'
        self.HUMIDITY = None  # '设备未连接'
        self.ERROR = False  # '设备本身已处于开启/关闭状态'
        self.SUCCESS = True  # '收到'
        self.room_dic = self.getRoomDic(device_dic)
        print("控制系统已就绪")


    def getState(self, name):
        # 通过设备名称获取设备状态
        return self.device[name]["state"]

    def getPin(self, name):
        # 通过设备名称获取Pin引脚
        return self.device[name]["pin"]

    def getID(self, name):
        # 通过设备名称获取ID
        return self.device[name]["ID"]

    def getName(self, ID):
        # 通过ID获取设备名称
        for name in self.device.keys():
            if self.getID(name) == ID:
                return name
        return None

    def getNameByPin(self, pin):
        # 通过Pin引脚获取设备名称
        for name in self.device.keys():
            if self.getPin(name) == pin:
                return name
        return None

    def getStateByPin(self, pin):
        # 通过Pin引脚获取设备状态
        for name in self.device.keys():
            if self.getPin(name) == pin:
                return self.getState(name)
        return None

    def changeStateByName(self, name):
        # 通过设备名称改变设备状态
        print(name, self.device[name]["state"])
        if self.device[name]["state"]:
            self.device[name]["state"] = False
        else:
            self.device[name]["state"] = True

    def switchByPin(self, pin, goal, name=None):
        if pin == None:
            pin = self.getPin(name)
        # 通过Pin引脚控制设备
        if self.getStateByPin(pin) == goal:
            return name,self.ERROR
        else:
            if name == None:
                name = self.getNameByPin(pin)
            self.changeStateByName(name)
            return name,self.SUCCESS

    def switchByName(self, name, goal):
        # 通过设备名引脚控制设备
        print("name : ", name, "goal :", goal)
        return self.switchByPin(None, goal, name)

    def getRoomDic(self,data_dic):
        # 获取房屋结构
        room_dic = {}
        for line in data_dic.keys():
            room_dic[line.split("/")[0]] = []
        for line in data_dic.keys():
            room_dic[line.split("/")[0]].append(line.split("/")[1])
        return room_dic

    def getDevice(self, device):
        the_device = list()
        # 获取同一设备的所有房间
        for line in self.room_dic.keys():
            if device in self.room_dic[line]:
                the_device.append(line + "/" + device)
        return the_device

    # def contrl(self,command, state):
    #     if room == None:
    #         temp = self.getDevice(command)
    #         if len(temp) == 0:
    #             # 无设备
    #             return None
    #         elif len(temp) == 1:
    #             # 只查到了一个设备
    #             command = temp[0]
    #             print(command)
    #         else:
    #             print("设备表出错了！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！")
    #     return self.switchByName(command, state)

if __name__ == '__main__':
    test_device = {"厨房/灯": {"ID": "0010", "state": False, "pin": 18},
                   "客厅/灯": {"ID": "0060", "state": False, "pin": 35},
                   "客厅/电视": {"ID": "0060", "state": True, "pin": 15}}
    contril_flow = DeviceContrl(test_device)
    print(contril_flow.switchByName("客厅/灯", False))