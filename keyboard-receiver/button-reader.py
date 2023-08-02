#!/usr/bin/env python3
import sys, time
import time
import usb
from ast import literal_eval


ENDPOINT = 0x02
INTERFACE = 0
DEVICE_BYTES = 8
VENDOR_ID = 0x1189
DEVICE_ID = 0x8890

if len(sys.argv) > 2:
    VENDOR_ID = literal_eval(sys.argv[1])
    DEVICE_ID = literal_eval(sys.argv[2])
if len(sys.argv) > 3:
    ENDPOINT = literal_eval(sys.argv[3])
if len(sys.argv) > 4:
    DEVICE_BYTES = int(sys.argv[4])

print(VENDOR_ID)
print(DEVICE_ID)
print(ENDPOINT)
print(DEVICE_BYTES)

class Button:
   def __init__(self, vendor_id, device_id):
      self.vendor_id = vendor_id
      self.device_id = device_id
      self.endpoint = ENDPOINT

      self.device = self.getDevice(vendor_id, device_id)
      if self.device != None:
        print('got device')
      
      if self.device == None:
         raise DeviceNotFound("No recognised device connected.")

      self.handle = self.openDevice(self.device)
   
   def __del__(self):
      try:
         self.handle.releaseInterface()
         del self.handle
      except:
         pass
   
   def getDevice(self, vendor_id, device_id):
      for bus in usb.busses():
         devices = bus.devices
         for device in devices:
            if device.idVendor == vendor_id and device.idProduct == device_id:
               return device
   
      return None
   
   def openDevice(self, device):
      handle = device.open()
      try:
         handle.detachKernelDriver(0)
      except:
         pass
      handle.claimInterface(INTERFACE)
      return handle

   def start(self):
      data = None
      while True:
         try:
            data = self.handle.interruptRead(self.endpoint, DEVICE_BYTES, 0)
            print(time.time())
            print(data)
         except:
            raise

         data = None

class DeviceNotFound(Exception):
 def __init__(self,value):
    self.value = value
 def __str__(self):
    return repr(self.value)

if __name__ == "__main__":
   button = Button(VENDOR_ID,DEVICE_ID)
   button.start()
