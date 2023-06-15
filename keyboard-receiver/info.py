#!/usr/bin/env python3
import hid
print("Opening the device")

h = hid.device()
h.open(0x1a6e, 0x089a)

print("Manufacturer: %s" % h.get_manufacturer_string())
print("Product: %s" % h.get_product_string())
print("Serial No: %s" % h.get_serial_number_string())
