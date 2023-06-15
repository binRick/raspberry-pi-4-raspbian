#!/usr/bin/env python3
import hid

for device_dict in hid.enumerate():
  keys = list(device_dict.keys())
  keys.sort()
  for i, key in enumerate(keys):
    print("\t%s : %s" % (key, device_dict[key]))

