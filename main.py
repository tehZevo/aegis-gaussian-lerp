import os
import numpy as np
import time
from protopost import ProtoPost
from nd_to_json import nd_to_json, json_to_nd

PORT = int(os.getenv("PORT", 80))
SHAPE = os.getenv("SHAPE", "2").split()
SHAPE = [int(i) for i in SHAPE]
FLIP_TIME = float(os.getenv("FLIP_TIME", 5.0))

#TODO: env for mean/std?

def sample():
    return np.random.normal(0, 1, SHAPE)

def flip():
    global a, b, last_time
    print("flip")
    a = b
    b = sample()
    last_time = time.time()

def get_value():
    t = (time.time() - last_time) / FLIP_TIME #calculate t 0..1
    #if time since last flip > flip time, flip first
    while t >= 1:
        flip()
        t -= 1
    #calculate lerp
    x = a + (b - a) * t
    return x

a = sample()
b = sample()

last_time = time.time()

routes = {
    "": lambda data: nd_to_json(get_value()),
}

ProtoPost(routes).start(PORT)
