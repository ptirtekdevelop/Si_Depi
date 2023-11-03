# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run YOLOv5 detection inference on images, videos, directories, globs, YouTube, webcam, streams, etc.

Usage - sources:
    $ python3 detect.py --weights hand.pt --source 0                               # webcam
                                                     img.jpg                         # image
                                                     vid.mp4                         # video
                                                     screen                          # screenshot
                                                     path/                           # directory
                                                     list.txt                        # list of images
                                                     list.streams                    # list of streams
                                                     'path/*.jpg'                    # glob
                                                     'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                     'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python3 detect.py --weights yolov5s.pt                 # PyTorch
                                 yolov5s.torchscript        # TorchScript
                                 yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                 yolov5s_openvino_model     # OpenVINO
                                 yolov5s.engine             # TensorRT
                                 yolov5s.mlmodel            # CoreML (macOS-only)
                                 yolov5s_saved_model        # TensorFlow SavedModel
                                 yolov5s.pb                 # TensorFlow GraphDef
                                 yolov5s.tflite             # TensorFlow Lite
                                 yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                 yolov5s_paddle_model       # PaddlePaddle
"""

import argparse
import os
import platform
import sys
import time
import numpy as np
from pathlib import Path

import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode
from libsearchimages.ctracker import CTracker
from libsearchimages.trackobject import TrackObject
import simplejpeg
import base64
import io
import cv2
import imutils
import queue
import threading

from apps import db, app
from apps.models_db import RoadData, RoadDamage
import random
import string

mylist = []
mycount = []

weights=ROOT / 'augment.pt' # model path or triton URL
data='data/coco128.yaml'  # dataset.yaml path
imgsz=(720, 720)  # inference size (height, width)
conf_thres=0.25  # confidence threshold
iou_thres=0.45  # NMS IOU threshold
max_det=1000  # maximum detections per image
device=''  # cuda device, i.e. 0 or 0,1,2,3 or cpu
view_img=False  # show results
save_txt=False  # save results to *.txt
save_conf=False  # save confidences in --save-txt labels
save_crop=False  # save cropped prediction boxes
nosave=False  # do not save images/videos
classes=None  # filter by class: --class 0, or --class 0 2 3
agnostic_nms=False  # class-agnostic NMS
augment=False  # augmented inference
update=False  # update all models
project='apps/static/videodetect' 
name=''  # save results to project/name
exist_ok=True # existing project/name ok, do not increment
line_thickness=3  # bounding box thickness (pixels)
hide_labels=False  # hide labels
hide_conf=False  # hide confidences
half=False  # use FP16 half-precision inference
dnn=False  # use OpenCV DNN for ONNX inference
vid_stride=1  # video frame-rate stride

# Load model
device = select_device(device)
model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
stride, names, pt = model.stride, model.names, model.pt
imgsz = check_img_size(imgsz, s=stride)  # check image size

def generateCentroid(rects):
    inputCentroids = np.zeros((len(rects), 2), dtype="int")
    for (i, (startX, startY, endX, endY)) in enumerate(rects):
        cX = int((startX + endX) / 2.0)
        cY = int((startY + endY) / 2.0)
        inputCentroids[i] = (cX, cY)
    return inputCentroids

def _8bit_to_base64(frame,quality=50):
	frame_buffer =  simplejpeg.encode_jpeg(image=frame,quality=quality,colorspace='BGR',fastdct=True)
	frame_64 = base64.encodebytes(frame_buffer).decode("utf-8")
	return frame_64

def frame_to_base64(path):
    buffer = cv2.imread(path)  # Ubah ke format JPEG atau format lain sesuai kebutuhan
    frame_encoded = _8bit_to_base64(buffer)
    return frame_encoded

class StreamMainDetect():
    
    def __init__(self):
        self.frame = None
        self.road_id = None
        self.source = None
        self.socketio = None

        self.totalPathole= 0
        self.totalCrocodile = 0
        self.totalLongitudinal = 0
        self.totalTransversal = 0
        self.save_path = None

        self.vid_cap = None

        self.stopcamera = None

        self.dataset = []

        self.stop_thread = False
        self.stop_event = threading.Event()

        self.start_th_run = threading.Thread(target=self.run, daemon=True)


    @smart_inference_mode()
    def run(self,source=None):  
        
        source = str(self.source)

        save_img = not nosave and not self.source.endswith('.txt')

        # Directories
        save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Dataloader
        bs = 1  # batch_size

        view_img = False

        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        self.dataset = dataset
        
        self.stopcamera = dataset.__stop_stream__
        bs = len(dataset)

        vid_path, vid_writer = [None] * bs, [None] * bs
       
        # Run inference
        t0 = time.time()
        ct = CTracker()
        listDet = ['Pathole','crocodile_crack','logitudinal_crack','transverse_cracks']

        totalPathole= 0
        totalCrocodile = 0
        totalLongitudinal = 0
        totalTransversal = 0
        pub = False
        trackableObjects = {}
        model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup

        visualize=False  # visualize features
        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())


        for path, im, im0s, vid_cap, s, in self.dataset:
            if self.stop_event.is_set():
                self.stopcamera()
                break 

            with dt[0]:
                im = torch.from_numpy(im).to(model.device)
                im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
                im /= 255  # 0 - 255 to 0.0 - 1.0
                if len(im.shape) == 3:
                    im = im[None]  # expand for batch dim

            # Inference
            with dt[1]:
                visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
                pred = model(im, augment=augment, visualize=visualize)

            # NMS
            with dt[2]:
                pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

            rects = []
            labelObj = []
            yObj = []
            arrCentroid = []
            
            # Process predictions
            for i, det in enumerate(pred):  # per image
                seen += 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
               
                s += f'{i}: '

                height, width, channels = im0.shape
                # cv2.line(im0, (0, int(height/2.5)), (int(width), int(height/2.5)), (0, 0, 255), thickness=1)
                p = Path(p)  # to Path
                save_path = str(save_dir)  # im.jpg
                txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
                s += '%gx%g ' % im.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                imc = im0.copy() if save_crop else im0  # for save_crop
                annotator = Annotator(im0, line_width=line_thickness, example=str(names))

                if det is not None and len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += '%g %s, ' % (n, names[int(c)])  # add to string                        
                    for *xyxy, conf, cls in det:
                        if conf >= 0.45:
                            label = '%s' % (names[int(cls)])
                            x = xyxy
                            tl = None or round(0.002 * (im0.shape[0] + im0.shape[1]) / 2) + 1  # line/font thickness
                            c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))

                            label1 = label.split(' ')
                            if label1[0] in listDet:
                                box = (int(x[0]), int(x[1]), int(x[2]), int(x[3]))
                                rects.append(box)
                                labelObj.append(label1[0])
                                cv2.rectangle(im0, c1 , c2, (130,115,229), thickness=tl, lineType=cv2.LINE_AA)
                                tf = max(tl - 1, 1)  
                                t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
                                c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
                                cv2.rectangle(im0, c1, c2, (130,115,229), -1, cv2.LINE_AA)
                                cv2.putText(im0, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

                detCentroid = generateCentroid(rects)
                objects = ct.update(rects)  
                for (objectID, centroid) in objects.items():
                    arrCentroid.append(centroid[1])
                for (objectID, centroid) in objects.items():
                    #print(idxDict)
                    to = trackableObjects.get(objectID, None)
                    if to is None:
                        to = TrackObject(objectID, centroid)
                    else:           
                        y = [c[1] for c in to.centroids]
                        direction = centroid[1] - np.mean(y)
                        to.centroids.append(centroid)
                        if not to.counted: #arah up
                            if direction > 0 and centroid[1] > height / 2.5:  #arah down
                                idx = detCentroid.tolist().index(centroid.tolist())
                                if(labelObj[idx] == 'Pathole'):
                                    totalPathole += 1
                                    to.counted = True
                                elif(labelObj[idx] == 'crocodile_crack'):
                                    totalCrocodile += 1
                                    to.counted = True
                                elif(labelObj[idx] == 'logitudinal_crack'):
                                    totalLongitudinal += 1
                                    to.counted = True
                                elif(labelObj[idx] == 'transverse_cracks'):
                                    totalTransversal += 1
                                    to.counted = True
                        

                    trackableObjects[objectID] = to

                # Stream results
                im0 = annotator.result()
                socketio = self.socketio
                socketio.emit('road_damage', {
                    'pathole':totalPathole,
                    'crocodile': totalCrocodile,
                    'longitudinal': totalLongitudinal,
                    'transversal': totalTransversal
                })

                self.totalPathole = totalPathole
                self.totalCrocodile = totalCrocodile 
                self.totalLongitudinal = totalLongitudinal 
                self.totalTransversal = totalTransversal 

                frame_encode = _8bit_to_base64(im0)
                socketio.emit('cam', frame_encode)

                cv2.waitKey(1)  # 1 millisecond

                # Save results (image with detections)
                if save_img:
                    if dataset.mode == 'image':
                        cv2.imwrite(save_path, im0)
                    else:  # 'video' or 'stream'
                        if vid_path[i] != save_path:  # new video
                            vid_path[i] = save_path
                            if isinstance(vid_writer[i], cv2.VideoWriter):
                                vid_writer[i].release()  # release previous video writer
                            if vid_cap:  # video
                                fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            else:  # stream
                                fps, w, h = 30, im0.shape[1], im0.shape[0]
                            # save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                            random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(8))  # 8 karakter acak
                            save_path = str(Path(save_path) / f'record_{random_suffix}.webm')
                            self.save_path = save_path
                            
                            # vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                            vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'VP90'), fps, (w, h))
                        vid_writer[i].write(im0)
               
    def save_to_db(self):
        with app.app_context():

            save_path = os.path.abspath(self.save_path)

            root, ext = os.path.splitext(save_path)
            new_video_path = f"{root}.webm"
            new_video_name = os.path.basename(new_video_path)

            road_data = RoadData.query.filter_by(id=self.road_id).first()
            
            road_data.video_path = new_video_name

            damage_types = ['pathole', 'crocodile', 'longitudinal', 'transversal']
            damage_sums = [self.totalPathole, self.totalCrocodile, self.totalLongitudinal, self.totalTransversal]
            for damage_type, damage_sum in zip(damage_types, damage_sums):
                road_damage = RoadDamage(type_damage=damage_type, sum_damage=damage_sum, road_data_id=self.road_id)
                db.session.add(road_damage)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error: {e}")

    def start_run(self, road_id, source, socketio):
        self.stop_event.clear()
        self.stop_thread = False
        self.road_id = road_id
        self.source = source
        self.socketio = socketio
        try:
            self.start_th_run.start()
        except RuntimeError:
            self.stopcamera()
            self.start_th_run = threading.Thread(target=self.run, daemon=True)
            self.start_th_run.start()
        except Exception as ex:
            print(ex)

    
    def stop_run(self):
        self.save_to_db()
        self.stop_thread = True
        self.stopcamera()
        self.dataset=[]
        self.stop_event.set()
        self.start_th_run.join()
        return

