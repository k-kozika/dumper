#!/usr/bin/env python3

import argparse
import os
import logging
from Helpers.Device import Device

def hook_function(cdm_version='14.0.0', dynamic_function_name='', module_names=["libwvaidl.so", "libwvhidl.so"]):
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
    
    device = hook_function(cdm_version, dynamic_function_name, module_names)

    logger.info('Connected to %s and function hooked, now open the DRM stream test on Bitmovin from your Android device! https://bitmovin.com/demos/drm')
    
    while not device.dumped:
        pass
    
    save_dir = os.path.join(
        'key_dumps',
        f'{device.name}',
        'private_keys',
        f'{device.sys_id}',
    )

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    with open(os.path.join(save_dir, 'client_id.bin'), 'wb+') as writer:
        writer.write(device.client_id)

    with open(os.path.join(save_dir, 'private_key.pem'), 'wb+') as writer:
        writer.write(device.private_key_pem)



if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S %p',
        level=logging.DEBUG,
    )
    
    main()
