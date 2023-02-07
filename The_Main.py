import cv2
from labels import label
import Bird_Classifier
import Recognition

model = Recognition.load_model()

def further_classification(img, bbox):
    
    x, y, w, h = bbox
    crop_img = img[y:y+h , x:x+w]

    cv2.imwrite('image.png', crop_img)

    result = Bird_Classifier.predict('image.png')
    print(result)

    cv2.rectangle(img, bbox, color=(255,0,0), thickness=2)
    cv2.putText(img, result, (bbox[0]+10,bbox[1]+40), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, thickness=3, color=(0,255,0))
    

def main():
    cap = cv2.VideoCapture(0)

    while True:
        resp, frame = cap.read()

        idxs, confs, bboxs = model.detect(frame, confThreshold=0.6)
        print(idxs, end = '  ')

        if len(idxs) != 0:
            for idx, conf, bbox in zip(idxs.flatten(), confs, bboxs):
                class_name = label.get(idx, 'Unknown')
                print(class_name)
                if class_name == 'bird':
                    further_classification(frame, bbox)

                else:
                    cv2.rectangle(frame, bbox, color=(255,0,0), thickness=2)
                    cv2.putText(frame, class_name, (bbox[0]+10,bbox[1]+40), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, thickness=3, color=(0,255,0))
        
        cv2.imshow('Web Cam', frame)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__' : 
    main()