let mediaRecorder;
let recordedChunks = [];

const video = document.getElementById('video');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Получаем доступ к камере
navigator.mediaDevices.getUserMedia({
    video: {width: 640, height: 480},
    audio: {
        sampleRate: 48000,
        channelCount: 2,
        echoCancellation: false,
        noiseSuppression: false,
        autoGainControl: false
    }
})
    .then(stream => {
        video.srcObject = stream;
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'video/webm; codecs=vp9,opus'
        });

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, {type: 'video/webm'});
            recordedChunks = [];

            // Отправляем видео на сервер
            const formData = new FormData();
            formData.append('video', blob, 'recorded_video.webm');

            const csrftoken = getCookie('csrftoken');

            fetch('http://127.0.0.1:8000/', {
                method: 'POST',
                headers: {
                    "X-CSRFToken": csrftoken,
                },
                body: formData
            }).then(response => response.json())
                .then(data => console.log(data));
        };
    })
    .catch(err => console.error('Ошибка доступа к камере: ', err));

startBtn.onclick = () => {
    mediaRecorder.start();
    console.log('Запись началась');
};

stopBtn.onclick = () => {
    mediaRecorder.stop();
    console.log('Запись остановлена и отправляется');
};
