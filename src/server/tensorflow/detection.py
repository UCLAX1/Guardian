import numpy as np
import tensorflow as tf
import cv2
import os
import time

class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)

        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def processFrame(self, image):
        image_np_expanded = np.expand_dims(image, axis=0)
        start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        end_time = time.time()
        im_height, im_width,_ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0,i,0] * im_height),
                        int(boxes[0,i,1]*im_width),
                        int(boxes[0,i,2] * im_height),
                        int(boxes[0,i,3]*im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        self.default_graph.close()

class Detection:
    def __init__(self):
        model_path = 'model_data/frozen_inference_graph.pb'
        self.odapi = DetectorAPI(path_to_ckpt=model_path)

    def run(self, img):
        
        threshold = 0.28
        found = False
#        TO OUTPUT IMAGES WITH SQUARES
#         directoryImages = 'PATH_TO_FOLDER_TO_OUTPUT_FOLDER'
#        outfile = os.path.join(directoryImages, image_path)
#         if not os.path.exists(directoryImages):
#             os.makedirs(directoryImages)

        img = cv2.resize(img, (1280, 720))
        
        #x_factor = 2560 / 1280
        #y_factor = 1920 / 720
        
        x_factor = 960 / 1280
        y_factor = 720 / 720

        boxes, scores, classes, num = self.odapi.processFrame(img)

        for i in range(len(boxes)):
            # Class 1 represents humanoids
            if classes[i] == 1 and scores[i] > threshold:
                found = True
                box = boxes[i]
                cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)
                x = (box[1]+box[3])/2
                y = (box[0]+box[2])/2
                return [x * x_factor, y * y_factor]
                #cv2.imwrite(outfile, img)
        if not found:   
            return [-1, -1]
