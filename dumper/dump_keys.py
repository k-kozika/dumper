#!/usr/bin/env python3

import argparse
import time
import logging
from Helpers.Device import Device

def hook_function(dynamic_function_name, cdm_version, module_names):
    device = Device(dynamic_function_name, cdm_version, module_names)
    for process in device.usb_device.enumerate_processes():
        if 'drm' in process.name:
            for library in device.find_widevine_process(process.name):
                device.hook_to_process(process.name, library)
    return device

def main():
    parser = argparse.ArgumentParser(description='Android Widevine L3 dumper.')
    parser.add_argument('--cdm-version', help='The CDM version of the device e.g. \'14.0.0\'', default='14.0.0')
    parser.add_argument('--function-name', help='The name of the function to hook to retrieve the private key.', default='')
    parser.add_argument('--module-name', 
        nargs='+',
        type=str,
        help='The names of the widevine `.so` modules',
        default=["libwvaidl.so", "libwvhidl.so"]
    )
    args = parser.parse_args()

    dynamic_function_name = args.function_name
    cdm_version = args.cdm_version
    module_names = args.module_name

    logger = logging.getLogger("main")
    logger.info('Connecting to %s and hooking functions...', device.name)
    
    device = hook(dynamic_function_name, cdm_version, module_names)
    logger.info('Functions hooked, now open the DRM stream test on Bitmovin from your Android device! https://bitmovin.com/demos/drm')
    return device


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S %p',
        level=logging.DEBUG,
    )
    
    device = main()
    while not device.dumped:
        time.sleep(1000)
