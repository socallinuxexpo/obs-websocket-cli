#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
import time
import yaml
from obswebsocket import obsws, requests  # noqa: E402
import logging

functions = []
def current_scene(ws, args):
    response = ws.call(requests.GetCurrentScene())
    print(response.getName())


def is_streaming(ws, args):
    resp = ws.call(requests.GetStreamingStatus())
    if( resp.getStreaming() ):
      print('yes')
      exit(0)
    else:
      print('no')
      exit(1)

def show_scenes(ws, args):
    response = ws.call(requests.GetSceneList())
    for s in response.getScenes():
        print(s['name'])
    exit(0)

def start_stream(ws, args):
    response = ws.call(requests.GetStreamingStatus())
    if not response.getStreaming():
        ws.call(requests.StartStopStreaming())
    
def stop_stream(ws, args):
    response = ws.call(requests.GetStreamingStatus())
    if response.getStreaming():
        ws.call(requests.StartStopStreaming())
    
def set_scene(ws, args):
    if len(args) == 1:
        response = ws.call(requests.GetSceneList())
        for scene in response.getScenes():
            if scene['name'] == args[0]:
              ws.call(requests.SetCurrentScene(args[0]))
              exit(0)
        print("Secne({}) not Found!".format(args))

    exit(1)

def set_camera(wc, args):
    set_scene(ws, ["FullCamera"])

def set_bigcamera(wc, args):
    set_scene(ws, ["BigCamera"])

def set_slides(wc, args):
    set_scene(ws, ["FullSlides"])

def set_mixed(wc, args):
    set_scene(ws, ["MixedScene"])

with open(os.path.join(os.path.dirname(__file__), "config.yml"), 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

logging.basicConfig(level=cfg['log_level'])
ws = obsws(cfg['host'], cfg['port'], cfg['password'])
ws.connect()

try:
    num_args = len(sys.argv)
    args = sys.argv
    if num_args == 1:
        #function = sys.argv.pop(0)
        test='test'
    else:
        args.pop(0)
        #function = sys.argv[1]
    function = sys.argv.pop(0)
    function = os.path.basename(function)
    #print("{}({})".format(function, args))
    if( function in locals() ):
        locals()[function](ws, args)
    else:
        funcs = []
        for key,item in locals().copy().items():
            if str(item).startswith("<function"):
                funcs.append(key)
        funcs.sort()
        #print(' '.join(funcs))
        print("({}) function not found, the following are supported\n[{}]".format(function, ' '.join(funcs)))
        exit(2)
except KeyboardInterrupt:
    pass

ws.disconnect()

