#!/usr/bin/env python3
import CoreWLAN
import CoreLocation
from time import sleep
import json
import sys
from datetime import datetime

def wait_for_location_auth(timeout=30):
    """位置情報の権限を待つ"""
    location_manager = CoreLocation.CLLocationManager.alloc().init()
    location_manager.startUpdatingLocation()
    
    for i in range(timeout):
        status = location_manager.authorizationStatus()
        if status == 3 or status == 4:
            return True
        sleep(1)
    
    return False

def get_security_type(network):
    """セキュリティタイプを取得"""
    try:
        security_types = []
        
        if network.supportsSecurity_(CoreWLAN.kCWSecurityWPA3Personal):
            security_types.append("WPA3-Personal")
        if network.supportsSecurity_(CoreWLAN.kCWSecurityWPA3Enterprise):
            security_types.append("WPA3-Enterprise")
        if network.supportsSecurity_(CoreWLAN.kCWSecurityWPA2Personal):
            security_types.append("WPA2-Personal")
        if network.supportsSecurity_(CoreWLAN.kCWSecurityWPA2Enterprise):
            security_types.append("WPA2-Enterprise")
        if network.supportsSecurity_(CoreWLAN.kCWSecurityWPAPersonal):
            security_types.append("WPA-Personal")
        if network.supportsSecurity_(CoreWLAN.kCWSecurityWPAEnterprise):
            security_types.append("WPA-Enterprise")
        if network.supportsSecurity_(CoreWLAN.kCWSecurityWEP):
            security_types.append("WEP")
        if network.supportsSecurity_(CoreWLAN.kCWSecurityNone):
            security_types.append("Open")
        
        return security_types[0] if security_types else "Unknown"
    except:
        return "Unknown"

def get_channel_info(network):
    """チャンネル情報を取得"""
    try:
        if not network.wlanChannel():
            return {"number": None, "bandwidth": "Unknown", "band": "Unknown"}
        
        channel_obj = network.wlanChannel()
        channel_num = channel_obj.channelNumber()
        width = channel_obj.channelWidth()
        
        width_map = {
            0: "Unknown",
            1: "20MHz",
            2: "40MHz",
            3: "80MHz",
            4: "160MHz"
        }
        bandwidth = width_map.get(width, "Unknown")
        
        if 1 <= channel_num <= 14:
            band = "2.4GHz"
        elif 36 <= channel_num <= 177:
            band = "5GHz"
        elif channel_num >= 1:
            band = "6GHz"
        else:
            band = "Unknown"
        
        return {
            "number": channel_num,
            "bandwidth": bandwidth,
            "band": band
        }
    except:
        return {"number": None, "bandwidth": "Unknown", "band": "Unknown"}

def scan_and_output_json():
    """スキャンしてJSON出力（メタデータ付き）"""
    wifi_interface = CoreWLAN.CWInterface.interface()
    if not wifi_interface:
        output = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "error": "Wi-Fi interface not found"
            },
            "networks": []
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return False
    
    networks, error = wifi_interface.scanForNetworksWithName_error_(None, None)
    
    if error:
        output = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "error": str(error)
            },
            "networks": []
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return False
    
    result = []
    for network in networks:
        ch_info = get_channel_info(network)
        
        network_data = {
            "SSID": network.ssid() if network.ssid() else None,
            "BSSID": network.bssid() if network.bssid() else None,
            "RSSI": network.rssiValue(),
            "Channel": ch_info["number"],
            "Band": ch_info["band"],
            "Bandwidth": ch_info["bandwidth"],
            "Security": get_security_type(network)
        }
        result.append(network_data)
    
    # RSSI順にソート（強い順）
    result.sort(key=lambda x: x["RSSI"], reverse=True)
    
    # メタデータ付きで出力
    output = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "interface": wifi_interface.interfaceName(),
            "total_networks": len(result)
        },
        "networks": result
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    
    return True

if __name__ == "__main__":
    if not wait_for_location_auth():
        output = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "error": "Location authorization failed"
            },
            "networks": []
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        exit(1)
    
    if not scan_and_output_json():
        exit(1)