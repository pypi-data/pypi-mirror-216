import threading
import time
import socket
import struct
import time
import sys
import datetime
class ModbusData:
    def __init__(self,IP,port):
        self.IP = IP
        self.port = port
        self.header = ''
        self.X = []
        self.Y = []
        self.Z = []
        self.Pd = []
        self.Dis = []
        self.Stime = []
        self.Etime = ''
        self.SPS = 0
        self.connect_success = False
        self.wait = False
        self.header = 0
        self.packet_type = 0
        self.PGV_1s = 0
        self.PGA_10s = 0
        self.Pd_warning_threshold = 0
        self.PGA_warning_threshold = 0
        self.Pd_flag = 0
        self.Pd_watch_threshold = 0
        self.PGA_warning_threshold = 0
        self.Intensity_now = 0
        self.Intensity_maximum = 0
        self.PGA_1s = 0
        self.tau_c = 0
        self.Trig_mode = 0
        self.Durations_WatchAndWarning = 0
        self.Firmware_version = 0
        self.Connection_flag = 0
        self.DIO_status = 0
        self.Pd_vertical = 0
        self.Pv_vertical = 0
        self.Pa_vertical = 0
        self.Maximum_vector = 0
        self.Maximum_a_axis = 0
        self.Maximum_b_axis = 0
        self.Maximum_c_axis = 0
        self.Maximum_a_axis_vector = 0
        self.Maximum_b_axis_vector = 0
        self.Maximum_c_axis_vector = 0
        self.Packet_length = 0
        self.Packet_no = 0

        self.lock = threading.Lock()
        self.background_thread = threading.Thread(target=self.connect, args=(IP,port), daemon=True)
        self.background_thread.start()

    def connect(self,IP,port):
        arr = [0x01, 0x02, 0x00, 0x00, 0x00, 0x06, 0x01, 0x06, 0x00, 0xc0, 0x00, 0x01]
        link=struct.pack("%dB"%(len(arr)),*arr)

        try: 
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e: 
            print ("Error creating socket: %s" % e) 
            sys.exit(1) 
        
        # Second try-except block -- connect to given host/port 
        try: 
            client.connect((IP,port))
            print("connect success")
            #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' + str(datetime.datetime.now()))
            self.connect_success = True
        except : 
            print ("FAIL") 
            sys.exit(1) 
        

        client.send(link)

        while True:
            link1 = client.recv(2500)
            
            data = link1.hex()
            #print(data)
            if(data == "010200000006010600c00001"):
                continue
            
            #print(len(data))
            header = data[:400]
            self.header = header
            #print(header)
            self.packet_type = int(data[2:4] + data[0:2] ,16)
            #print(packet_type)
            self.event_flag = int(data[6:8] + data[4:6] ,16)
            #print(event_flag)
            Syear =  int(data[10:12] + data[8:10] ,16)
            Smonth =  int(data[14:16] + data[12:14] ,16)
            Sday =  int(data[18:20] + data[16:18] ,16)
            Shour =  int(data[22:24] + data[20:22] ,16) 
            Sminute = int(data[26:28] + data[24:26] ,16)
            Ssecond = int(data[30:32] ,16)
            Smsecond = int(data[28:30] ,16)
            Stime = str(Syear) + "-" + str(Smonth) + "-" + str(Sday) + "-" + str(Shour) + "-" + str(Sminute) + "-" + str(Ssecond) + "-" + str(Smsecond)
            #print(Stime)
            self.Stime.append(Stime)
            Eyear =  int(data[34:36] + data[32:34] ,16)
            Emonth =  int(data[38:40] + data[36:38] ,16)
            Eday =  int(data[42:44] + data[40:42] ,16)
            Ehour =  int(data[46:48] + data[44:46] ,16) 
            Eminute = int(data[50:52] + data[48:50],16)
            Esecond = int(data[54:56],16)
            Emsecond = int(data[52:54],16)
            Etime = str(Eyear) + "-" + str(Emonth) + "-" + str(Eday) + "-" + str(Ehour) + "-" + str(Eminute) + "-" + str(Esecond) + "-" + str(Emsecond)
            #print(Etime)
            self.Etime = Etime

            self.PGV_1s = int(data[58:60] + data[56:58] ,16)

            self.PGA_10s = int(data[66:68] + data[64:66] ,16)

            self.Pd_warning_threshold = int(data[82:84] + data[80:82] ,16)

            self.PGA_warning_threshold = int(data[86:88] + data[84:86] ,16)

            self.Pd_flag = int(data[94:96] + data[92:94] ,16) 

            self.Pd_watch_threshold = int(data[98:100] + data[96:98] ,16)

            self.PGA_warning_threshold = int(data[102:104] + data[100:102] ,16)

            self.Intensity_now = int(data[106:108] + data[104:106] ,16)

            self.Intensity_maximum = int(data[110:112] + data[108:110] ,16)

            self.PGA_1s = int(data[114:116] + data[112:114] ,16)

            self.tau_c = int(data[122:124] + data[120:122] ,16)

            self.Trig_mode = int(data[126:128] + data[124:126] ,16)

            self.Durations_WatchAndWarning = int(data[134:136] + data[132:134] ,16)

            self.Firmware_version = int(data[138:140] + data[136:138] ,16)

            self.Connection_flag = int(data[194:196] + data[192:194] ,16)

            self.DIO_status = int(data[198:200] + data[196:198] ,16)

            self.Pd_vertical = int(data[206:208] + data[204:206] ,16)
    
            self.Pv_vertical = int(data[210:212] + data[208:210] ,16)

            self.Pa_vertical = int(data[214:216] + data[212:214] ,16)

            self.Maximum_vector = int(data[218:220] + data[216:218] ,16)
            
            self.Maximum_a_axis = int(data[222:224] + data[220:222] ,16)

            self.Maximum_b_axis = int(data[226:228] + data[224:226] ,16)
            
            self.Maximum_c_axis = int(data[230:232] + data[228:230] ,16)
            
            self.Maximum_a_axis_vector = int(data[234:236] + data[232:234] ,16)

            self.Maximum_b_axis_vector = int(data[238:240] + data[236:238] ,16)
            
            self.Maximum_c_axis_vector = int(data[242:244] + data[240:242] ,16)

            self.Packet_length = int(data[298:300] + data[296:298] ,16)

            self.Packet_no = int(data[358:360] + data[356:358] ,16)

            self.SPS = int(data[398:400] + data[396:398] ,16)

            XYZdata = data[400:]
            xconnect, yconnect, zconnect, Pdconnect, Disconnect = data_cut(XYZdata)
            #print(len(xconnect)) --- 100
            self.X.extend(xconnect)
            self.Y.extend(yconnect)
            self.Z.extend(zconnect)
            self.Pd.extend(Pdconnect)
            self.Dis.extend(Disconnect)
            #print(len(self.X))
            if(len(self.X)>6000):
                del self.X[:100]
                del self.Y[:100]
                del self.Z[:100]
                del self.Pd[:100]
                del self.Dis[:100]
                del self.Stime[:1]
    

    def get_IP(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.IP
        except :
            print("Connect Fail, so Nothing in list")

    def get_Port(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.port
        except :
            print("Connect Fail, so Nothing in list")

    def get_Header(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.header
        except :
            print("Connect Fail, so Nothing in list")

    def get_Now_Channel1(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.X[-100:]
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_Channel2(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Y[-100:]                  
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_Channel3(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Z[-100:]          
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_Pd(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Pd[-100:]          
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_Displacement(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Dis[-100:]          
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_SystemTime(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Stime[-1]
        except :
            print("Connect Fail, so Nothing in list")
    def get_EventTime(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Etime
        except :
            print("Connect Fail, so Nothing in list")
    def get_SPS(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.SPS
        except :
            print("Connect Fail, so Nothing in list")
    def get_NsecondChannel1Data(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.Stime)<N):
            print("Only have "+ str(len(self.Stime)) + " Second Data")
            N = len(self.Stime)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*100
        Xreturn = []
        UTreturn = []
        try:
            Xreturn.extend(self.X[-N1000:])
            UTreturn.extend(self.Stime[-N:])
            return Xreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")
    def get_NsecondChannel2Data(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.Stime)<N):
            print("Only have "+ str(len(self.Stime)) + " Second Data")
            N = len(self.Stime)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*100
        Yreturn = []
        UTreturn = []
        try:
            Yreturn.extend(self.Y[-N1000:])
            UTreturn.extend(self.Stime[-N:])
            return Yreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")
  
    def get_NsecondChannel3Data(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.Stime)<N):
            print("Only have "+ str(len(self.Stime)) + " Second Data")
            N = len(self.Stime)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*100
        Zreturn = []
        UTreturn = []
        try:
            Zreturn.extend(self.Z[-N1000:])
            UTreturn.extend(self.Stime[-N:])
            return Zreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")

    def get_NsecondPd(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.Stime)<N):
            print("Only have "+ str(len(self.Stime)) + " Second Data")
            N = len(self.Stime)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*100
        Pdreturn = []
        UTreturn = []
        try:
            Pdreturn.extend(self.Pd[-N1000:])
            UTreturn.extend(self.Stime[-N:])
            return Pdreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")

    def get_NsecondDisplacement(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.Stime)<N):
            print("Only have "+ str(len(self.Stime)) + " Second Data")
            N = len(self.Stime)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*100
        Disreturn = []
        UTreturn = []
        try:
            Disreturn.extend(self.Dis[-N1000:])
            UTreturn.extend(self.Stime[-N:])
            return Disreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")

                
    def get_Now_packet_type(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.packet_type        
        except :
            print("Connect Fail, so Nothing in list")

            
    def get_Now_event_flag(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.event_flag          
        except :
            print("Connect Fail, so Nothing in list")
                
    def get_Now_PGV_1s(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.PGV_1s
        except :
            print("Connect Fail, so Nothing in list")
                            
    def get_Now_PGA_10s(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.PGA_10s
        except :
            print("Connect Fail, so Nothing in list")
                            
    def get_Now_Pd_warning_threshold(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Pd_warning_threshold
        except :
            print("Connect Fail, so Nothing in list")
                            
    def get_Now_PGA_warning_threshold(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.PGA_warning_threshold
        except :
            print("Connect Fail, so Nothing in list")
                            
    def get_Now_Pd_flag(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Pd_flag
        except :
            print("Connect Fail, so Nothing in list")
                            
    def get_Now_Pd_watch_threshold(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Pd_watch_threshold
        except :
            print("Connect Fail, so Nothing in list")

    def get_Now_PGA_warning_threshold(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.PGA_warning_threshold
        except :
            print("Connect Fail, so Nothing in list")

    def get_Now_Intensity_now(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Intensity_now
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Intensity_maximum(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Intensity_maximum
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_PGA_1s(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.PGA_1s
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_tau_c(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.tau_c
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Trig_mode(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Trig_mode
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Durations_WatchAndWarning(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Durations_WatchAndWarning
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Firmware_version(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Firmware_version
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Durations_WatchAndWarning(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Durations_WatchAndWarning
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Connection_flag(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Connection_flag
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_DIO_status(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.DIO_status
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Pd_vertical(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Pd_vertical
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Pv_vertical(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Pv_vertical
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Pa_vertical(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Pa_vertical
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Maximum_vector(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Maximum_vector
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Maximum_a_axis(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Maximum_a_axis
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Maximum_b_axis(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Maximum_b_axis
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Maximum_c_axis(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Maximum_c_axis
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Maximum_a_axis_vector(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Maximum_a_axis_vector
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Maximum_b_axis_vector(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Maximum_b_axis_vector
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Maximum_c_axis_vector(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Maximum_c_axis_vector
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Packet_length(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Packet_length
        except :
            print("Connect Fail, so Nothing in list")
            
    def get_Now_Packet_no(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Packet_no
        except :
            print("Connect Fail, so Nothing in list")
            
def data_cut(XYZstr):
    
    xdata_cut = []
    ydata_cut = []
    zdata_cut = []
    PD_cut = []
    Dis_cut = []
    flag = 0
    #Little Endian 轉回正常
    XYZhex = ''
    #print(len(XYZstr))
    
    #每4個byte為一組處理
    for i in range(0, len(XYZstr), 4):
        XYZdecimal=0
        a = XYZstr[i:i+2]
        b = XYZstr[i+2:i+4]
        XYZhex = b+a
        #hex to decimal 
        #print(XYZhex)

        #儲存進XYZ的陣列
        if(flag == 0):
            hex_string = XYZhex  # 十六进制字符串
            unsigned_integer = int(hex_string, 16)  # 将十六进制字符串转换为无符号整数
            XYZdecimal = unsigned_integer if unsigned_integer < 32768 else unsigned_integer - 65536  # 转换为有符号整数
            XYZdecimal = XYZdecimal/16.718
            #print(XYZdecimal)
            xdata_cut.append(XYZdecimal)
            flag = flag +1
        elif(flag == 1):
            hex_string = XYZhex  # 十六进制字符串
            unsigned_integer = int(hex_string, 16)  # 将十六进制字符串转换为无符号整数
            XYZdecimal = unsigned_integer if unsigned_integer < 32768 else unsigned_integer - 65536
            XYZdecimal = XYZdecimal/16.718
            #print(XYZdecimal)
            ydata_cut.append(XYZdecimal)
            flag = flag +1
        elif(flag == 2):
            hex_string = XYZhex  # 十六进制字符串
            unsigned_integer = int(hex_string, 16)  # 将十六进制字符串转换为无符号整数
            XYZdecimal = unsigned_integer if unsigned_integer < 32768 else unsigned_integer - 65536
            XYZdecimal = XYZdecimal/16.718
            #print(XYZdecimal)
            zdata_cut.append(XYZdecimal)
            flag = flag +1
        elif(flag == 3):
            hex_string = int(XYZhex,16) 
            #print(XYZhex)
            XYZdecimal = unsigned_integer if unsigned_integer < 32768 else unsigned_integer - 65536
            XYZdecimal = XYZdecimal/1000
            PD_cut.append(XYZdecimal)
            flag = flag +1
        elif(flag == 4):
            hex_string = int(XYZhex,16) 
            XYZdecimal = unsigned_integer if unsigned_integer < 32768 else unsigned_integer - 65536
            XYZdecimal = XYZdecimal/1000
            Dis_cut.append(XYZdecimal)
            flag = 0

    return xdata_cut, ydata_cut, zdata_cut, PD_cut, Dis_cut

if __name__ == '__main__':

    XXXX = ModbusData('10.0.0.227',502)
    
    while True:
        Stime = XXXX.get_Now_Packet_no()
        print(Stime)

    
        time.sleep(1)
    
