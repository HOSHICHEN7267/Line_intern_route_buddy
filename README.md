# 最懂你的(✪ω✪) 智能路線規劃 chatbot


一款創新的路線規劃應用，專為需要即時公共交通建議和喜愛探索的使用者設計。主要特色在於使用對話形式進行路線規劃，使用者僅需輸入景點或地點名稱，即可獲得準確且詳細的路線建議，希望能為每位使用者帶來前所未有的便利和樂趣，成為智能出行的新標竿。

## 特色

+ 市面上第一款以"對話"進行路線規劃的平台
+ 提供 Real-time 公共旅運路線規劃
+ 可直接以"景點"或"地點"的名稱進行規劃

## 使用教學

傳送訊息告訴小幫手，出發地點、目的地、是否偏好省錢或省時間

    If 能正確找到交通方式:   
    小幫手告訴使用者如何轉乘交通  
    else:   
    小幫手說明錯誤問題，並請使用者再傳一次內容

## 運用技術

+ 串接 Line messaging api 作為聊天平台
+ 整合 OpenAI、Google Map Platform API、TDX MaaS 模組，產出路線建議

## 架構

此專案以 Line 作為聊天平台，串接 OpenAI、Google Map、TDX MaaS 模組，以取得公共運輸旅運規劃。


Step 1. 當 chatbot 獲取使用者輸入後，將字串傳給 OpenAI 進行自然語言處理。


Step 2. OpenAI 將使用者輸入轉為 json 格式，其中包含起訖點地名敘述、使用者偏好。將這份 json 傳給 Google Geocoding。


Step 3. 利用 Google Geocoding API 取得起訖點座標，將這份資料結合先前的使用者輸入傳給 TDX。


Step 4. TDX MaaS 模組取得使用者輸入，將規劃路線傳給 OpenAI。


Step 5. OpenAI 解讀規劃路線，並產出自然語言，將路徑指示字串傳給 chatbot。


Step 6. chatbot 以對話的方式向使用者展示規劃路線。