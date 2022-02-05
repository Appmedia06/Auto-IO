import cv2
import autopy
import time
import numpy as np
import HandTrackingModule as htm
from directionkeys import NP_4, NP_6, NP_2, NP_8
from directionkeys import PressKey, ReleaseKey

# 1.食指移動滑鼠
# 2.中指碰食指點擊左鍵
# 3.大拇指左方向鍵
# 4.小拇指是右方向鍵
# 5.中指是上方向鍵
# 6.無名指和小拇指是下方向鍵
# 7.五隻手指全開可調整模式(單一，連續)

##################################
right_pressed = NP_6
left_pressed = NP_4
up_pressed = NP_8
down_pressed = NP_2

left_key_pressed = left_pressed
right_key_pressed = right_pressed
up_key_pressed = up_pressed
down_key_pressed = down_pressed

time.sleep(2.0)
current_key_pressed = set()

##################################
wCam, hCam = 640, 480
IndexId, MiddleId = 8, 12
fingerNum = [0, 1, 2, 3, 4]
centerPosxId, centerPosyId = 4, 5
frameR = 100 # Frame Reduction
smoothening = 7

##################################
mono = False
conti = False
mono_key = 0 # 偶數
conti_key = 0 # 奇數
###################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

cTime = 0
pTime = 0

detector = htm.handDector(maxHand=1)

wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

# Previous, Current Location
plocX, plocY = 0, 0
clocX, clocY = 0, 0

####################################

while True:
    keyPressed = False
    left_pressed = False
    right_pressed = False
    up_pressed = False
    down_pressed = False
    #####################
    key_count = 0
    key_pressed = 0

    # Hand Landmarks
    success, img = cap.read()
    img = detector.findHand(img)
    lmList, bbox = detector.findPosition(img)

    # 如果有偵測到手
    if len(lmList) != 0:
        left_direct = False
        right_direct = False
        up_direct = False
        down_direct = False

        x1, y1 = lmList[IndexId][1:] # Index finger
        x2, y2 = lmList[MiddleId][1:] # Middle finger
        # 判斷手指上升
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                    (255,0,255), 2)
        
        # 改變模式(單一[用PTT或打字時一個一個移動]，連續[滑動網站])
        if fingers.count(1) == 5:
            mono_key += 1
            conti_key += 1
            time.sleep(0.7)

        # 單一模式
        if mono_key % 2 == 0:
            cv2.rectangle(img, (345, 0), (640, 96), (173, 222, 255), cv2.FILLED)
            cv2.putText(img, "Mono MODE", (356, 59), cv2.FONT_HERSHEY_PLAIN,
                        3, (135, 51, 36), 5)
            # 食指 : Move Mode
            if fingers[fingerNum[1]] == 1 and fingers[fingerNum[2]] == 0 :
                # Convert Coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                # Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # Move Mouse
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            #  Both index and middle finger are up : Click Mode
            if fingers[fingerNum[1]] == 1 and fingers[fingerNum[2]] == 1 :
                # Find distance between index and meddle finger
                length, img, lineInfo = detector.findDistance(IndexId, MiddleId, img)
                # Click mouse if distance is short
                if length < 40: 
                    cv2.circle(img, (lineInfo[centerPosxId], lineInfo[centerPosyId]), 15, (0,255,0), cv2.FILLED)
                    autopy.mouse.click(None)

            # 3.Thumb : 左
            if fingers[fingerNum[0]] == 1 and fingers[fingerNum[4]] == 0:
                left_direct = True


            # Little finger : 右
            if fingers[fingerNum[0]] == 0 and fingers[fingerNum[4]] == 1:
                right_direct = True

            # Middle finger UP : 上
            if fingers[fingerNum[1]] == 0 and fingers[fingerNum[2]] == 1:
                up_direct = True

            # Ring finger UP : 下
            if fingers[fingerNum[3]] == 1 and fingers[fingerNum[4]] == 0:
                down_direct = True


            # 按方向鍵
            if down_direct:
                cv2.rectangle(img, (0, 355), (250, 480), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "DOWN", (35, 440), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,0,0), 5)
                PressKey(down_key_pressed)
                down_pressed = True
                keyPressed = True
                current_key_pressed.add(down_key_pressed)
                key_pressed = down_key_pressed
                key_count = key_count + 1
                time.sleep(0.2)

            elif right_direct:
                cv2.rectangle(img, (0, 355), (250, 480), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "RIGHT", (38, 440), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,0,0), 5)
                PressKey(right_key_pressed)
                right_pressed = True
                keyPressed = True
                current_key_pressed.add(right_key_pressed)
                key_pressed = right_key_pressed
                key_count = key_count + 1
                time.sleep(0.2)
            
            elif up_direct:
                cv2.rectangle(img, (0, 355), (250, 480), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "UP", (83, 440), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,0,0), 5)
                PressKey(up_key_pressed)
                up_pressed = True
                keyPressed = True
                current_key_pressed.add(up_key_pressed)
                key_pressed = up_key_pressed
                key_count = key_count + 1
                time.sleep(0.2)

            elif left_direct:
                cv2.rectangle(img, (0, 355), (250, 480), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "LEFT", (50, 440), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,0,0), 5)
                PressKey(left_key_pressed)
                left_pressed = True
                keyPressed = True
                current_key_pressed.add(left_key_pressed)
                key_pressed = left_key_pressed
                key_count = key_count + 1
                time.sleep(0.2)



        # 連續模式
        if conti_key % 2 != 0:
            cv2.rectangle(img, (345, 0), (640, 96), (173, 222, 255), cv2.FILLED)
            cv2.putText(img, "Conti MODE", (356, 59), cv2.FONT_HERSHEY_PLAIN,
                        3, (135, 51, 36), 5)

            # 食指 : Move Mode
            if fingers[fingerNum[1]] == 1 and fingers[fingerNum[2]] == 0 :
                # Convert Coordinates

                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                # Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # Move Mouse
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            # 2.Both index and middle finger are up : Click Mode
            if fingers[fingerNum[1]] == 1 and fingers[fingerNum[2]] == 1 :
                # Find distance between index and meddle finger
                length, img, lineInfo = detector.findDistance(IndexId, MiddleId, img)
                # Click mouse if distance is short
                if length < 40:
                    cv2.circle(img, (lineInfo[centerPosxId], lineInfo[centerPosyId]), 15, (0,255,0), cv2.FILLED)
                    autopy.mouse.click(None)

            # 3.Thumb : 左
            if fingers[fingerNum[0]] == 1 and fingers[fingerNum[4]] == 0:
                left_direct = True


            # Little finger : 右
            if fingers[fingerNum[0]] == 0 and fingers[fingerNum[4]] == 1:
                right_direct = True

            # Middle finger UP : 上
            if fingers[fingerNum[1]] == 0 and fingers[fingerNum[2]] == 1:
                up_direct = True

            # Ring finger UP : 下
            if fingers[fingerNum[3]] == 1 and fingers[fingerNum[4]] == 0:
                down_direct = True


            # 按方向鍵
            if down_direct:
                cv2.rectangle(img, (0, 355), (250, 480), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "DOWN", (35, 440), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,0,0), 5)
                PressKey(down_key_pressed)
                down_pressed = True
                keyPressed = True
                current_key_pressed.add(down_key_pressed)
                key_pressed = down_key_pressed
                key_count = key_count + 1

            elif right_direct:
                cv2.rectangle(img, (0, 355), (250, 480), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "RIGHT", (38, 440), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,0,0), 5)
                PressKey(right_key_pressed)
                right_pressed = True
                keyPressed = True
                current_key_pressed.add(right_key_pressed)
                key_pressed = right_key_pressed
                key_count = key_count + 1
            
            elif up_direct:
                cv2.rectangle(img, (0, 355), (250, 480), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "UP", (83, 440), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,0,0), 5)
                PressKey(up_key_pressed)
                up_pressed = True
                keyPressed = True
                current_key_pressed.add(up_key_pressed)
                key_pressed = up_key_pressed
                key_count = key_count + 1

            elif left_direct:
                cv2.rectangle(img, (0, 355), (250, 480), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "LEFT", (50, 440), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,0,0), 5)
                PressKey(left_key_pressed)
                left_pressed = True
                keyPressed = True
                current_key_pressed.add(left_key_pressed)
                key_pressed = left_key_pressed
                key_count = key_count + 1


    if not keyPressed and len(current_key_pressed) != 0: 
        for key in current_key_pressed:
            ReleaseKey(key)
        current_key_pressed = set()
    elif key_count == 1 and len(current_key_pressed) == 2:
        for key in current_key_pressed:
            if key_pressed == key:
                ReleaseKey(key)

        current_key_pressed = set()
        for key in current_key_pressed:
            ReleaseKey(key)
        current_key_pressed = set()


    # Frame Rate幀率(每秒幀數)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),3)
    
    # Show
    if success:
        cv2.imshow("Image", img)
    else:
        break
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()