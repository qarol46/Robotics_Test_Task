"""
Модуль для определения положения объекта в видеопотоке с веб-камеры в реальном времени.
Использует YOLOv8 для детекции и OpenCV для работы с видео и отрисовки.
"""

import cv2
from ultralytics import YOLO
import numpy as np


class ObjectPositionTracker:
    
    def __init__(self, camera_id=0, model_name='yolov8n.pt', conf_threshold=0.4):
        self.model = YOLO(model_name)
        self.conf_threshold = conf_threshold
        self.target_class_id = None

        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise IOError("Не удалось открыть веб-камеру. Проверьте подключение и ID устройства.")

        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_center = (self.frame_width // 2, self.frame_height // 2)

        print(f"Видеопоток инициализирован. Размер кадра: {self.frame_width}x{self.frame_height}")
        print("Для выбора объекта отслеживания нажмите клавишу 's'")
        print("Нажмите 'q' для выхода.")

    def _calculate_offset(self, object_center):
        dx = object_center[0] - self.frame_center[0]
        dy = object_center[1] - self.frame_center[1]
        return dx, dy

    def _draw_info(self, frame, box, class_name, conf, object_center, bbox_size):
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.circle(frame, object_center, 5, (0, 0, 255), -1)
        cv2.circle(frame, self.frame_center, 5, (255, 0, 0), -1)

        label = f"{class_name}: {conf:.2f}"
        offset = self._calculate_offset(object_center)
        offset_text = f"Offset: dx={offset[0]}, dy={offset[1]}"
        center_text = f"Obj Center: {object_center}"
        bbox_size_text = f"Box Dimensions: {bbox_size}"

        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, offset_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, center_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, bbox_size_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        if self.target_class_id is not None:
            target_text = f"Tracking class ID: {self.target_class_id}"
            cv2.putText(frame, target_text, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    def _select_target_object(self, frame, results):
        """Функция для выбора объекта через интерфейс"""
        display_frame = frame.copy()

        y_offset = 30
        cv2.putText(display_frame, "Detected objects:", (10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        detected_objects = []
        for i, box in enumerate(results.boxes):
            class_id = int(box.cls[0])
            class_name = results.names[class_id]
            confidence = float(box.conf[0])
            
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            object_text = f"{i}: {class_name} (ID: {class_id}) conf: {confidence:.2f}"
            y_offset += 25
            cv2.putText(display_frame, object_text, (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            detected_objects.append((i, class_id, class_name))
        
        if not detected_objects:
            cv2.putText(display_frame, "No objects detected", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return None, display_frame
        
        cv2.putText(display_frame, "Enter object number (0, 1, 2...):", (10, y_offset + 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        return detected_objects, display_frame

    def run(self):
        selecting_object = False
        detected_objects = None
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Не удалось получить кадр с камеры.")
                break

            results = self.model(frame, conf=self.conf_threshold, verbose=False)[0]

            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s') and not selecting_object:
                selecting_object = True
                print("Режим выбора объекта активирован")
            
            if selecting_object:
                detected_objects, display_frame = self._select_target_object(frame, results)
                cv2.imshow('Real-Time Object Position Tracking', display_frame)
                
                if detected_objects is not None:
                    try:
                        key = cv2.waitKey(0) & 0xFF
                        if key >= ord('0') and key <= ord('9'):
                            selected_idx = key - ord('0')
                            if selected_idx < len(detected_objects):
                                self.target_class_id = detected_objects[selected_idx][1]
                                print(f"Выбран объект: {detected_objects[selected_idx][2]} (ID: {self.target_class_id})")
                                selecting_object = False
                    except:
                        pass
                    
                    if key == 27:
                        selecting_object = False
            else:
                detected = False
                
                if self.target_class_id is not None:
                    for box in results.boxes:
                        class_id = int(box.cls[0])
                        if class_id == self.target_class_id:
                            x1, y1, x2, y2 = box.xyxy[0].tolist()
                            confidence = float(box.conf[0])
                            class_name = results.names[class_id]

                            object_center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                            bbox_size = (int(x2 - x1), int(y2 - y1))

                            self._draw_info(frame, (x1, y1, x2, y2), class_name, confidence, object_center, bbox_size)
                            detected = True
                            break
                
                if self.target_class_id is None:
                    cv2.putText(frame, "Press 's' to select object to track", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                elif not detected:
                    cv2.putText(frame, f"Object ID {self.target_class_id} not detected", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                cv2.imshow('Real-Time Object Position Tracking', frame)
            
            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("Ресурсы освобождены. Работа модуля завершена.")


if __name__ == "__main__":
    tracker = ObjectPositionTracker(camera_id=0, model_name='yolov8n.pt', conf_threshold=0.5)
    tracker.run()