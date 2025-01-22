from ultralytics import YOLO
import cv2


class Predict:

    model = YOLO("./predict/yolo11x.pt")

    def __init__(self):
        pass

    def predict(self, chosen_model, img, classes=[], conf=0.5):
        if classes:
            results = chosen_model.predict(img, classes=classes, conf=conf)
        else:
            results = chosen_model.predict(img, conf=conf)

        return results

    def predict_and_detect(
        self,
        chosen_model,
        img,
        classes=[],
        conf=0.5,
        rectangle_thickness=2,
        text_thickness=1,
    ):
        results = self.predict(chosen_model, img, classes, conf=conf)
        for result in results:
            for box in result.boxes:
                cv2.rectangle(
                    img,
                    (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                    (int(box.xyxy[0][2]), int(box.xyxy[0][3])),
                    (255, 0, 0),
                    rectangle_thickness,
                )
                cv2.putText(
                    img,
                    f"{result.names[int(box.cls[0])]}",
                    (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (255, 0, 0),
                    text_thickness,
                )
        return img, results


# read the image
# image = cv2.imread("YourImagePath.png")
# result_img, _ = predict_and_detect(Predict.model, image, classes=[], conf=0.5)

# cv2.imshow("Image", result_img)
# cv2.imwrite("YourSavePath.png", result_img)
# cv2.waitKey(0)
