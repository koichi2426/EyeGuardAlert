const loadingAreaGrey = document.querySelector('.loading');
const loadingAreaGreen = document.querySelector('.loading-screen');
const loadingText = document.querySelector('.loading > p');

window.addEventListener('load' , () => {//webページが完全に読み込まれたら、
    loadingAreaGrey.animate(
        {
            opacity: [1,0],
            visibility: 'hidden'
        },
        {
            duration: 2000,//アニメーションの持続時間は2000ms(2s)
            delay: 1200,//1.2s後にアニメーション開始
            easing: 'ease',//アニメーションのタイミング関数は"ease"と呼ばれるもので、移動がスムーズに進行します。
            fill: 'forwards',//アニメーションが完了した後、要素の最終状態を維持します。
        }
    );

    loadingAreaGreen.animate(
        {
            translate: ['0 100vh', '0 0', '0 -100vh']
        },
        {
            duration: 2000,
            delay: 800,
            easing: 'ease',
            fill: 'forwards',
        }
    );

    loadingText.animate(
        [
            {
                //アニメーションの80％位置までtextを表示
                opacity: 1,
                offset: .8 //80%
            },
            {
                //アニメーションの終了時点（100％）でtextが完全に透明になること
                opacity: 0,
                offset: 1 //100%
            },
        ],
        {
            duration: 1200,
            easing: 'ease',
            fill: 'forwards',
        }
    );
});

// ボタン要素と画像要素、ビデオ要素に対する参照を取得
const changeButton = document.getElementById("runPythonButton");
const myImage = document.querySelector(".camera-image");
const myVideo = document.querySelector(".video-image");

// ボタンがクリックされたときの処理を定義
changeButton.addEventListener("click", function myFunction() {

    // 画像を非表示にし、ビデオを表示する
    myImage.style.display = "none";
    myVideo.style.display = "block";

    const myVideo_message = "別タブで分析中";

    const messageElement = document.querySelector(".video-message");

    messageElement.textContent = myVideo_message;
    
});