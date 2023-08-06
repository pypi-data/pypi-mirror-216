import inspect
import json
from threading import Thread
import os
import tempfile
import time

# Internal class for functions the end user doesn't have to see
class Internal:
  "Functions used internally, Its probably not the best idea to run these!"
  def __init__(self):
    self.messagerInstance = Internal.messager()
  class messager:
    def __init__(self):
      self.connections = []
      self.tempFilePath = os.path.join(tempfile.gettempdir(), "python_messaging")
      if not os.path.exists(self.tempFilePath):
          os.makedirs(self.tempFilePath)
  def empty():
    pass
  def Value_In_Dict(value, dictList):
    return any(value == dictionary['channel'] for dictionary in dictList)
  def get_main_file_name():
    frame = inspect.currentframe().f_back
    while frame.f_globals['__name__'] != '__main__':
      frame = frame.f_back
    main_file_name = frame.f_globals['__file__']
    return main_file_name.split("\\")[-1]
  def listener(func, data, interval:float):
    with open(data['filePath'], 'r') as file:
      oldData = file.read()
    while True:
      with open(data['filePath'], 'r') as file:
        fileContents = file.read()
        if fileContents != oldData:
          func(json.loads(fileContents))
          oldData = fileContents
        time.sleep(interval)
  def make_listener(func, data, interval:float):
    listener = Thread(target=Internal.listener,args=(func, data, interval))
    listener.start()

internalInstance = Internal()

def listen(channel:int, interval:float=1.0):
  "Decorator to make a function a message listener. (function needs a parameter for the message)"
  def inner(func):
    if Internal.Value_In_Dict(channel, internalInstance.messagerInstance.connections):
      for dict in internalInstance.messagerInstance.connections:
        if dict['channel'] == channel:
          data = dict
          break
      Internal.make_listener(func, data, interval)
    else:
      data = {
        'channel': channel,
        'filePath': f"{internalInstance.messagerInstance.tempFilePath}/{channel}.message"
      }
      internalInstance.messagerInstance.connections.append(data)
      Internal.make_listener(func, data, interval)
      
  return inner

def send(channel:int, message:dict):
  if Internal.Value_In_Dict(channel, internalInstance.messagerInstance.connections):
    for dict in internalInstance.messagerInstance.connections:
      if dict['channel'] == channel:
        data = dict
        break
    jsonMessage = json.dumps(message)
    with open(data['filePath'], 'w') as file:
      file.write(jsonMessage)
  else:
    data = {
      'channel': channel,
      'filePath': f"{internalInstance.messagerInstance.tempFilePath}/{channel}.message"
    }
    internalInstance.messagerInstance.connections.append(data)
    jsonMessage = json.dumps(message)
    with open(data['filePath'], 'w') as file:
      file.write(jsonMessage)