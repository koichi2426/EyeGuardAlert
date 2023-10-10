from flask import Flask, render_template, request
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import time
from pydantic import BaseModel
from statistics import variance
import popup

# デバッグ用の機能を使用するか
Debug = True

# 左目の各部位のランドマークのインデックス
__Up = 159
__Down = 23
__Left = 130
__Right = 243

# 前回の時間計測時の時間
global last_blink_time
last_blink_time = 0
global last_calculate_time
last_calculate_time = 0
#_INTERVAL単位で瞬きの頻度の標準偏差を算出する（以下の場合は10分）
_INTERVAL = 600

class BlinkCounter(BaseModel, strict=True):
    blink_log: list[int]
    interval_to_before: list[int]

log = BlinkCounter(
    blink_log=[],
    interval_to_before=[]
)
# 基準となるまばたき回数を数える時間の長さ(ナノ秒)

# 以下の場合は600秒(10分)
_OBSERVE_NORMAL_TIME = 600 + time.perf_counter()

# 以下の場合は300秒(5分)
#_OBSERVE_NORMAL_TIME = 300 + time.perf_counter()

#以下の場合は60秒
#_OBSERVE_NORMAL_TIME = 60 + time.perf_counter()
global normal_dispersion
normal_dispersion = 0



def check_blink(logger:BlinkCounter):
    global last_calculate_time
    global Tolerance
    last_calculate_time = time.perf_counter()
    if logger.blink_log and logger.interval_to_before:
        print("check")
        print("normal variance : " + str(normal_dispersion))
        print("now variance : " + str(variance(logger.interval_to_before)))
        if Tolerance < abs(variance(logger.interval_to_before) - normal_dispersion):
            popup.popup()
        

app = Flask(__name__)

def run_camera():
    global normal_dispersion
    global last_blink_time
    global last_calculate_time
    global Tolerance
    
    # VideoCaptureインスタンス化
    # カメラを抽出
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # FaceMesh検出器を初期化し、最大で1つの顔を検出するように設定
    detector = FaceMeshDetector(maxFaces=1)
    
    # グラフを表示するためのLivePlotオブジェクトを初期化
    # (ウィンドウ幅,ウィンドウの高さ,yの値の表示範囲,y軸は上向きか)
    if Debug:
        plotY = LivePlot(640,360,[20,50], invert=True)

    # まばたきを検出するための目のランドマークのインデックスのリスト
    #
    #　＜ランドマークとは＞
    # 「ランドマーク（landmark）」は、顔や物体などの特定のポイントや位置を指す用語です。
    
    # 1. `idList` リストは、目のランドマークのインデックスを格納します。
    # これらのインデックスは、FaceMeshモデルが顔の中で特定のランドマークを識別するのに使用する。
    # 2. `ratioList` リストは、まばたきの比率を格納するために使用されます。
    # この比率はまばたきの検出に使用され、まばたきの状態を追跡します。
    idList = [22,23,24,26,110,157,158,159,160,130,243]
    ratioList = []

    # まばたきカウンターとフレームカウンターの初期化
    # このコードでは、2つの変数 `blinkCounter` と `counter` が初期化されています。
    # これらの変数は、まばたきのカウントと関連する情報を追跡するために使用されます。
    # 1. `blinkCounter`: まばたきの回数を格納するための変数です。
    # 2. `counter`: まばたきの間隔を数える変数、連続でまばたきと判定しないようにする。
    blinkCounter = 0
    counter = 0

    # まばたき状態に応じて表示する色の初期化
    color1 = (255,0,255)
    color2 = (0,200,0)
    color = color1

    # 初期のblinklate値
    global blinklate
    blinklate = 34

    # 初期のTolerance値
    global Tolerance
    Tolerance = 100

    # ブリンク遅延を調整するトラックバーのコールバック関数
    def on_blinklate_trackbar(val):
        global blinklate
        blinklate = val
    def on_Tolerance_trackbar(val: int):
        global Tolerance
        Tolerance = val

    # OpenCVウィンドウを作成
    cv2.namedWindow('Blink Detection')
    
    # トラックバーを作成し、初期値を設定
    cv2.createTrackbar('Blink Late', 'Blink Detection', blinklate, 100, on_blinklate_trackbar)
    cv2.createTrackbar('Tolerance', 'Blink Detection', Tolerance, 1000, on_Tolerance_trackbar)

    before_frame = 0
    current_frame = 0
    before_time = 0
    # 無限ループ
    while True:
        
        if time.perf_counter() - before_time > _INTERVAL:
            before_time = time.perf_counter()
            print(time.perf_counter())
        if _OBSERVE_NORMAL_TIME < time.perf_counter():
            if not normal_dispersion:
                normal_dispersion = variance(log.interval_to_before)
                log.blink_log.clear()
                log.interval_to_before.clear()
                print("OVSERVE_NORMAL_DESCRIPTION is ended")
            if time.perf_counter() - last_calculate_time > _INTERVAL:
                print("try to check blink")
                check_blink(logger=log)
                
            
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # ビデオフィードからフレームを取得
        # 1. `cap.read()`: メソッドを呼び出すことで、カメラから1つのフレームを読み込みます。
        # 2. `success`: フレームの読み込みが成功したかどうかを示すブール値を返します。
        # 3. `img`: 読み込まれたビデオフレームがこの変数に格納されます。
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img, draw=False)
        
        if faces:
            # 検出する顔の数に1を指定したが、元々複数の顔を検出できるメソッドだったので、
            # 先頭を指定する
            face = faces[0]

            # 円を描画して目のランドマークを可視化する
            # - `img`: 描画対象のビデオフレーム。
            # - `face[id]`: 描画する円の中心座標。この座標はランドマークの位置に対応します。
            # - `5`: 円の半径。
            # - `color`: 円の色。
            # - `cv2.FILLED`: 円を塗りつぶすオプション。
            for id in idList:
                cv2.circle(img, face[id], 5, color, cv2.FILLED)

            # 目の角度を計算
            Up = face[__Up]
            Down = face[__Down]
            Left = face[__Left]
            Right = face[__Right]
            
            cv2.line(img, Up, Down, color2, 3)
            cv2.line(img, Left, Right, color2, 3)

            lengthVer,_ = detector.findDistance(Up,Down)
            lengthHor,_ = detector.findDistance(Left,Right)

            
            ratio = int((lengthVer/lengthHor)*100)
            ratioList.append(ratio)

            # 直近の3つの比率を保持し、平均を計算
            if len(ratioList) > 3:
                ratioList.pop(0)
            ratioAvg = sum(ratioList) / len(ratioList)

            # まばたきの検出とカウント
            if ratioAvg < blinklate and counter == 0:
                print("blinked")
                time_now = time.perf_counter()
                log.blink_log.append(time_now)
                log.interval_to_before.append(
                    time_now - last_blink_time
                )
                blinkCounter += 1
                color = color1
                counter = 1
                last_blink_time = time_now
                    


            if counter != 0:
                counter +=1
                if counter > 10:
                    counter = 0
                    color = color2

            # まばたき回数を画面に表示
            cvzone.putTextRect(img, f'Count: {blinkCounter}', (50,100), colorR=color)

            # グラフをアップデートし、画像をリサイズ
            imgPlot = plotY.update(ratioAvg, color)
            img = cv2.resize(img, (640,360))

            # 画像を並べて表示
            # - `img` と `imgPlot` は積み重ねる対象の2つの画像です。`img` はビデオフレームであり、
            # `imgPlot` はまばたきの比率を示すグラフです。
            # - `2` は行の数を指定し、`1` は列の数を指定しています。
            imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
        else:
            # 顔が検出されない場合、単にビデオフィードを表示
            img = cv2.resize(img, (640,360))
            imgStack = cvzone.stackImages([img, img], 2, 1)
        
        # 画面にフレームを表示し、キー入力を待機
        # このコードブロックは、OpenCVを使用して画像を表示するためのものです。以下にコードの詳細を説明します：
        # - `cv2.imshow('Image', imgStack)` は、`imgStack` という画像をウィンドウに表示するための関数呼び出しです。
        # `'Image'` はウィンドウのタイトルを指定します。つまり、'Image' というタイトルのウィンドウが作成され、
        # その中に `imgStack` が表示されます。
        # - `cv2.waitKey(1)` は、ウィンドウを表示した後、
        # 指定されたミリ秒数（ここでは1ミリ秒）だけキー入力を待機するための関数呼び出しです。
        # この関数は通常、ウィンドウが表示されている間、キー入力を受け付けるために使用されます。
        # 1ミリ秒の待機時間を持つことで、ウィンドウが非表示になる前にキー入力を受け付けることができます。
        # このコードブロックにより、`imgStack` という画像が表示されるウィンドウが作成され、
        # そのウィンドウが表示された後に1ミリ秒間キー入力を待機します。ユーザーがキーを押すと、
        # その入力に応じて適切な処理を追加できます。たとえば、ウィンドウを閉じたり、
        # スクリーンショットを保存したりするなどのアクションをトリガーすることができます。
        cv2.imshow('Blink Detection', imgStack)
        cv2.waitKey(1)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    # ボタンがクリックされたときに実行するコードをここに書きます
    run_camera()
    return 'Script executed successfully'

if __name__ == "__main__":
    app.run(debug=True)
