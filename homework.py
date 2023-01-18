import random
import threading
import concurrent.futures
import datetime
import copy
import time

# 宣告全域性變數
beef_source = 10
pork_source = 7
chicken_source = 5
# 建立互斥鎖
mutex = threading.Lock()

#進行肉品處理函式
def work(n):
    global beef, pork, chicken  # 宣告全域變數
    beef_time, pork_time, chicken_time = 1, 2, 3  # 宣告處理肉的時間

    while True:
        if(beef<=0 and pork<=0 and chicken<=0): #所有肉品均非正數，則結束工作
            print(n+'工作結束了')
            break
        meat=random.choice(['beef', 'pork', 'chicken']) #隨機選擇處理肉品
        mutex.acquire()# 檢查前，鎖定資源，確保數量是正確的 
        if(check(meat)): #該肉品，尚有庫存
            print(n+"在 "+now_time()+"取得"+meat) #印出取得肉品時間
            if(meat=='beef'):
                beef-=1 # 扣除已處理肉品
                print("牛肉剩餘{0}".format(beef))
                mutex.release()# 解鎖資源
                time.sleep(beef_time) #處理花費時間
            elif(meat=='pork'):
                pork-=1
                print("豬肉剩餘{0}".format(pork))
                mutex.release()
                time.sleep(pork_time)
            elif(meat=='chicken'):
                chicken-=1
                print("雞肉剩餘{0}".format(chicken))
                mutex.release()
                time.sleep(chicken_time)
            print(n+"在 "+now_time()+"處理完"+meat) #印出處理完肉品時間
        else:
            mutex.release()# 解鎖資源
            

#檢查肉品數量(肉品數量大於零回傳True，否則False)
def check(meat):
    match (meat):
        case "beef":
            meat=beef
        case "pork":
            meat=pork
        case "chicken":
            meat=chicken
    return True if (meat>0) else False
# 取得現在的日期時間
def now_time():
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print(f'\r{now}', end = '')     # 前方加上 \r
        time.sleep(1)
        return now
    

def main():
    # 程式規則五:不能修改進貨的肉量和員工數量，故將資料深複製
    global beef,pork,chicken
    beef = copy.deepcopy(beef_source)
    pork = copy.deepcopy(pork_source)
    chicken = copy.deepcopy(chicken_source)
    # 同時建立及啟用5個執行緒，執行 work函式，並傳入參數(五位員工的代號)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(work, ['A', 'B', 'C', 'D', 'E'])
    

if __name__ == '__main__':
    main()
