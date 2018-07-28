from ..common.event import EventDispatcher
from ..common.events import *
from ..engine.vector import Vector

from multiprocessing import Process, Pipe, Pool
import copy
import time
import operator
import numpy as np

def processYImage(y):
    threshold = 200
    radius = 6
    circle_points = list()
    center = np.array([radius, 0])
    circle_points.append(np.array([0, -radius]))
    circle_points.append(np.array([0, radius]))
    circle_points.append(np.array([radius, 0]))
    circle_points.append(np.array([-radius, 0]))
    radius_sqrt_two = radius / 1.414
    circle_points.append(np.array([radius_sqrt_two, radius_sqrt_two]))
    circle_points.append(np.array([radius_sqrt_two, -radius_sqrt_two]))
    circle_points.append(np.array([-radius_sqrt_two, radius_sqrt_two]))
    circle_points.append(np.array([-radius_sqrt_two, -radius_sqrt_two]))

    results = list()
    y[0][0] = 0
    while True:
        candidate_index = np.argmax(y > threshold)
        if candidate_index == 0:
            break
        candidate_origin = np.unravel_index(candidate_index, y.shape)
        candidate = candidate_origin[0:2] + center
        if candidate[0] <= radius or candidate[0] >= y.shape[0] - radius or candidate[1] <= radius or candidate[1] >= y.shape[1] - radius:
            y[candidate_origin] = 0
            continue
        candidate = candidate[0:2]
        is_circle = True
        sub_results = list()
        for circle_point in circle_points:
            point = (candidate + circle_point).astype(int)
            sub_results.append(point)
            if y[point[0]][point[1]] < threshold:
                is_circle = False
                break
        if is_circle:
            results.append(candidate)
            top_left = candidate - (radius, radius)
            bot_right = candidate + (radius, radius)
            y[top_left[0]:bot_right[0], top_left[1]:bot_right[1]] = 0
        y[candidate_origin] = 0

    return results

def yImageWorker(pipe):
    main_conn, worker_conn = pipe
    while True:
        data = worker_conn.recv()
        if data == ImageProcess.END_MESSAGE:
           break;
        result = processYImage(data.data)
        worker_conn.send((data.timestamp, result))

class ImageProcess(object):
    END_MESSAGE = 'END'
    def __init__(self):
        EventDispatcher().add_event_listener(YImageEvent.TYPE, self.onYImageEvent)

        self._main1_conn, self._worker1_conn = Pipe()
        self._worker1_ready = True
        self._worker1 = Process(target=yImageWorker, args=((self._main1_conn, self._worker1_conn),))
        self._worker1.daemon = True
        self._worker1.start()

        self._main2_conn, self._worker2_conn = Pipe()
        self._worker2_ready = True
        self._worker2 = Process(target=yImageWorker, args=((self._main2_conn, self._worker2_conn),))
        self._worker2.daemon = True
        self._worker2.start()

    def onYImageEvent(self, event):
        if self._worker1_ready:
            self._worker1_ready = False
            self._main1_conn.send(event.data()[0])
        if self._worker2_ready:
            self._worker2_ready = False
            self._main2_conn.send(event.data()[1])

    def stop(self):
        self._main1_conn.send(ImageProcess.END_MESSAGE)
        while self._main1_conn.poll():
           self._main1_conn.recv()
        self._main2_conn.send(ImageProcess.END_MESSAGE)
        while self._main2_conn.poll():
           self._main2_conn.recv()
        self._worker1.join()
        self._worker2.join()

    def update(self):
        if self._main1_conn.poll():
            data = self._main1_conn.recv()
            self._worker1_ready = True
            EventDispatcher().dispatch_event(LatencyEvent(LatencyEvent.P1_PROCESSING, data[0]))
            EventDispatcher().dispatch_event(CameraResultEvent(CameraResultEvent.P1, data[1]))
        if self._main2_conn.poll():
            data = self._main2_conn.recv()
            self._worker2_ready = True
            EventDispatcher().dispatch_event(LatencyEvent(LatencyEvent.P2_PROCESSING, data[0]))
            EventDispatcher().dispatch_event(CameraResultEvent(CameraResultEvent.P2, data[1]))
