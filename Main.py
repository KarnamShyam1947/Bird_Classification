import Recognition, os
import Bird_Classifier
import cv2

def write_bird_lables(img, bboxs, result):
    i = 0
    for bbox in bboxs:
        cv2.rectangle(img, bbox, color=(255, 0, 0), thickness=2)
        cv2.putText(img, result[i], (bbox[0]+10, bbox[1]+30), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2)
        i += 1

    cv2.imwrite('result_bird.png', img)

def main():
    img = 'images/birds.png'
    model = Recognition.load_model()

    response, resp_str = Recognition.detect_labels(img, 0.6, model)

    print(response)
    print(resp_str)

    if 'bird' in list(response.keys()):
        print('If Bird is present') 
        img = cv2.imread(img)
        result = list()
        i = 0

        idxs, confs, bboxs = model.detect(img, 0.6)
        for idx, conf, bbox in zip(idxs.flatten(), confs, bboxs):
            x, y, w, h = bbox

            crop_img = img[y:y+w, x:x+h]
            cv2.imwrite(f'cropped/img{i}.png', crop_img)
            i = i + 1

        folder = 'cropped'
        files = os.listdir(folder)

        for file in files:
            result.append(Bird_Classifier.predict(f'{folder}/{file}'))

        print(result)
        
        write_bird_lables(img, bboxs, result)

if __name__ == '__main__' : 
    main()
