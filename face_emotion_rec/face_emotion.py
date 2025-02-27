import cv2
from fer import FER

# Загружаем видео с камеры
cap = cv2.VideoCapture(0)
detector = FER()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Распознаем эмоции
    result = detector.detect_emotions(frame)

    if result:
        emotion = max(result[0]['emotions'], key=result[0]['emotions'].get)
        print("Эмоция:", emotion)

    # Выход по нажатию 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
