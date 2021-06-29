import serial
import pandas as pd
import threading
import time
import numpy as np
from scipy.fftpack import fft

####################################
## collecting raw data from ADXL345
## X Y Z 三軸數據皆採集
####################################
global comA
comA = "COM6"
global comB
comB = "COM8"

def FFT(rawData, t):

    collectionNum = 500
    interval = np.linspace(0, t, collectionNum)

    ampZ_FSD = abs(fft(rawData))/len(interval)    #歸一化處理
    ampZ_FSD_Half = ampZ_FSD[range(int(len(interval)/2))] #由於對稱性，只取一半區間

    return ampZ_FSD_Half

def DataCollectA():
    
    total_collectTime = 200
    volume = 500          #單次取樣筆數
    count_collectTime = 0
    
    All_dataFFT = []
    global comA

    while count_collectTime < total_collectTime:
        count = 1                                        #資料比數計數器
        KeepReading = False                              #是否繼續閱讀
        dataStr = b''                                    #數據疊加字串
        dataLibAx = []                                    #資料暫存庫
        dataLibAy = []
        dataLibAz = []
        All_dataTemp = []
        serA = serial.Serial(comA, 115200, timeout = 1)
        t1 = time.time()
        while count <= volume:                                 #單次取樣筆數          
            data = serA.read(8)
            if data and ( KeepReading or (b'S' in data) ) :
                dataStr += data
                if b'E' in data : #避免開頭第一筆同時節到 "mc & : " ，直接出去
                    KeepReading = False
                    #print(b'A:' + dataStr)
                    try:
                        # 封包萃取
                        dataParts = dataStr.split(b'_')
                        dataLibAx.append(float(dataParts[1]))
                        dataLibAy.append(float(dataParts[2]))
                        dataLibAz.append(float(dataParts[3]))
                        #dataRAW.append(float(dataParts[3])) #Z axis data
                        count += 1    #資料筆數+1
                        dataStr = b'' #重置封包暫存變數
                    except:
                        dataStr = b'' #重置封包暫存變數0
                else:
                    KeepReading = True
            else:
                KeepReading = True
                dataStr = b''
        t2 = time.time()
        tInterval = t2 - t1

        All_dataTemp.extend(FFT(dataLibAx, tInterval))
        All_dataTemp.extend(FFT(dataLibAy, tInterval))
        All_dataTemp.extend(FFT(dataLibAz, tInterval))
        All_dataFFT.append(All_dataTemp)
        
        serA.close() #可以測試看看全部處理完再關
        #print("hello !")
        count_collectTime += 1

    #All_dataFFT.extend(X_dataFFT)
    #All_dataFFT.extend(Y_dataFFT)
    #All_dataFFT.extend(Z_dataFFT) 
    name = np.arange(750)
    totalData_A =  pd.DataFrame(columns = name, data = All_dataFFT) #index 變數預設為數字 0~n
    totalData_A.to_csv(r"C:\Users\Kenny Lin\Desktop\data_0612\0612_normal_A_5.csv", encoding = 'gbk') #編碼 utf-8 or gbk
    

def DataCollectB():

    count_collectTime = 0    #initialze
    total_collectTime = 200
    volume = 500                               #設定總資料筆數
    
    All_dataFFT = []
    global comB
    while count_collectTime < total_collectTime :
        count = 0                                        #資料比數計數器
        KeepReading = False
        dataStr = b''
        dataLibBx = []                                    #資料暫存庫
        dataLibBy = []
        dataLibBz = []
        All_dataTemp = []
        serB = serial.Serial(comB, 115200, timeout = 1)
        t1 = time.time() 
        while count < volume:                                 #資料筆數
            data = serB.read(8)
            if data and ( KeepReading or (b'S' in data) ):
                dataStr += data
                if b'E' in data : 
                    KeepReading = False
                    #print(b'B' + dataStr)
                    try:
                        # 封包萃取
                        dataParts = dataStr.split(b'_')
                        dataLibBx.append(float(dataParts[1]))
                        dataLibBy.append(float(dataParts[2]))
                        dataLibBz.append(float(dataParts[3]))
                        #dataRAW.append(float(dataParts[3])) #Z axis data
                        count += 1    #資料筆數+1
                        dataStr = b'' #重置封包暫存變數
                    except:
                        dataStr = b''
                else:
                    KeepReading = True

            else:
                KeepReading = True
                dataStr = b''
        t2 = time.time()
        tInterval = t2 - t1
        
        All_dataTemp.extend(FFT(dataLibBx, tInterval))
        All_dataTemp.extend(FFT(dataLibBy, tInterval))
        All_dataTemp.extend(FFT(dataLibBz, tInterval))
        All_dataFFT.append(All_dataTemp)
        serB.close()
        count_collectTime += 1
    
    #All_dataFFT.extend(X_dataFFT)
    #All_dataFFT.extend(Y_dataFFT)
    #All_dataFFT.extend(Z_dataFFT)
    name = np.arange(750)
    totalData_B =  pd.DataFrame(columns = name, data = All_dataFFT) #index 變數預設為數字 0~n
    totalData_B.to_csv(r"C:\Users\Kenny Lin\Desktop\data_0612\0612_normal_B_5.csv", encoding = 'gbk') #編碼 utf-8 or gbk

if __name__ == '__main__':

    dataCollectA = threading.Thread(target = DataCollectA)
    dataCollectB = threading.Thread(target = DataCollectB)

    Ts = time.time()
    dataCollectA.start()
    dataCollectB.start()
    dataCollectA.join()
    dataCollectB.join()

    print('collection finished. using {} sec'.format(str(time.time() - Ts)))

    
    

