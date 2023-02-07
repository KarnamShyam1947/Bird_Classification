from datetime import datetime
import Bird_Classifier
import Recognition
import labels
import cv2

model = Recognition.load_model()
camera=cv2.VideoCapture(0)

def log_details(msg):
    now = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    msg = f'\n[ {now} ]{msg}'

    with open('logs.txt', 'a') as file:
        file.write(msg)

        file.close()

def if_bird_image(img, bbox):
    x, y, w, h = bbox

    crop_img = img[y:y+w, x:x+h]
    cv2.imwrite('crop_img.png', crop_img)

    bird_name = Bird_Classifier.predict('crop_img.png')

    cv2.rectangle(img, bbox, color=(255, 0, 0), thickness=2)
    cv2.putText(img, bird_name, (bbox[0]+10, bbox[1]+30), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2)

def generate_frames():
    while True:
        
        success,frame=camera.read()
        if not success:
            break
        else:

            idxs, confs, bboxs = model.detect(frame, 0.6)

            if len(idxs) != 0:
                for idx, conf, bbox in zip(idxs.flatten(), confs, bboxs):
                    class_name = labels.label.get(idx, 'Unknown')

                    if class_name == 'bird':
                        if_bird_image(frame, bbox)

                    else:
                        cv2.rectangle(frame, bbox, color=(255, 0, 0), thickness=2)
                        cv2.putText(frame, class_name, (bbox[0]+10, bbox[1]+30), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2)

            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def main():
    log_details('Hello, World')

if __name__ == '__main__' : 
    main()