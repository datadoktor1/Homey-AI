"""
Homey Controller - Direct access to HomeyScript and device control
"""
import requests
import json
from typing import Optional, Dict, Any, List

class HomeyController:
    def __init__(self, ip: str, api_key: str):
        """
        Initialize Homey controller with local API access.
        
        Args:
            ip: Local IP address of your Homey (e.g., "192.168.1.13")
            api_key: API Key from Homey Web App (Settings → API Keys)
        """
        self.base_url = f"http://{ip}/api"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make an API request to Homey."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(
                method, 
                url, 
                headers=self.headers, 
                json=data,
                timeout=10
            )
            response.raise_for_status()
            # Handle empty responses (e.g., DELETE returns 204 No Content)
            if response.status_code == 204 or not response.text:
                return {"success": True}
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    # ========================
    # DEVICE CONTROL
    # ========================
    
    def get_devices(self) -> Dict[str, Any]:
        """Get all devices."""
        return self._request("GET", "manager/devices/device")
    
    def get_device(self, device_id: str) -> Dict[str, Any]:
        """Get a specific device."""
        return self._request("GET", f"manager/devices/device/{device_id}")
    
    def set_device_capability(self, device_id: str, capability: str, value: Any) -> Dict[str, Any]:
        """
        Set a device capability.
        
        Common capabilities:
        - onoff: True/False (lights, switches)
        - dim: 0.0-1.0 (dimmable lights)
        - target_temperature: float (thermostats)
        - volume_set: 0.0-1.0 (speakers)
        """
        return self._request(
            "PUT", 
            f"manager/devices/device/{device_id}/capability/{capability}",
            {"value": value}
        )
    
    def turn_on(self, device_id: str) -> Dict[str, Any]:
        """Turn on a device."""
        return self.set_device_capability(device_id, "onoff", True)
    
    def turn_off(self, device_id: str) -> Dict[str, Any]:
        """Turn off a device."""
        return self.set_device_capability(device_id, "onoff", False)
    
    def set_brightness(self, device_id: str, level: float) -> Dict[str, Any]:
        """Set brightness (0.0 to 1.0)."""
        return self.set_device_capability(device_id, "dim", level)
    
    # ========================
    # HOMEYSCRIPT
    # ========================
    
    def get_scripts(self) -> Dict[str, Any]:
        """Get all HomeyScript scripts."""
        return self._request("GET", "app/com.athom.homeyscript/script")
    
    def get_script(self, script_id: str) -> Dict[str, Any]:
        """Get a specific script."""
        return self._request("GET", f"app/com.athom.homeyscript/script/{script_id}")
    
    def create_script(self, name: str, code: str) -> Dict[str, Any]:
        """Create a new HomeyScript."""
        return self._request("POST", "app/com.athom.homeyscript/script", {
            "name": name,
            "code": code
        })
    
    def update_script(self, script_id: str, code: str, name: str = None) -> Dict[str, Any]:
        """Update an existing HomeyScript."""
        data = {"code": code}
        if name:
            data["name"] = name
        return self._request("PUT", f"app/com.athom.homeyscript/script/{script_id}", data)
    
    def delete_script(self, script_id: str) -> Dict[str, Any]:
        """Delete a HomeyScript."""
        return self._request("DELETE", f"app/com.athom.homeyscript/script/{script_id}")
    
    def run_script(self, script_id: str, args: dict = None) -> Dict[str, Any]:
        """Run a HomeyScript and get the result."""
        data = args or {}
        return self._request("POST", f"app/com.athom.homeyscript/script/{script_id}/run", data)
    
    def run_code(self, code: str) -> Dict[str, Any]:
        """Run arbitrary HomeyScript code directly (without saving)."""
        return self._request("POST", "app/com.athom.homeyscript/script/run", {"code": code})
    
    # ========================
    # ZONES & FLOWS
    # ========================
    
    def get_zones(self) -> Dict[str, Any]:
        """Get all zones."""
        return self._request("GET", "manager/zones/zone")
    
    def get_flows(self) -> Dict[str, Any]:
        """Get all flows."""
        return self._request("GET", "manager/flow/flow")
    
    def get_flow(self, flow_id: str) -> Dict[str, Any]:
        """Get a specific flow."""
        return self._request("GET", f"manager/flow/flow/{flow_id}")
    
    def trigger_flow(self, flow_id: str) -> Dict[str, Any]:
        """Trigger a flow."""
        return self._request("POST", f"manager/flow/flow/{flow_id}/trigger")
    
    def create_flow(self, name: str, trigger: dict, actions: list, 
                    conditions: list = None, enabled: bool = False) -> Dict[str, Any]:
        """
        Create a new flow.
        
        Args:
            name: Flow name
            trigger: Trigger definition (when the flow starts)
            actions: List of action definitions (what the flow does)
            conditions: Optional list of conditions
            enabled: Whether the flow is enabled (default False for safety)
        
        Example trigger (manual/programmatic):
            {"id": "homey:manager:flow:programmatic_trigger", "uri": "homey:manager:flow", "args": {}}
        
        Example action (turn on device):
            {"id": "homey:device:<device_id>:onoff", "uri": "homey:device:<device_id>", 
             "args": {"onoff": True}, "group": "then"}
        """
        flow_data = {
            "name": name,
            "enabled": enabled,
            "trigger": trigger,
            "conditions": conditions or [],
            "actions": actions
        }
        return self._request("POST", "manager/flow/flow", flow_data)
    
    def update_flow(self, flow_id: str, **kwargs) -> Dict[str, Any]:
        """Update an existing flow. Pass any fields to update (name, enabled, trigger, actions, conditions)."""
        return self._request("PUT", f"manager/flow/flow/{flow_id}", kwargs)
    
    def delete_flow(self, flow_id: str) -> Dict[str, Any]:
        """Delete a flow."""
        return self._request("DELETE", f"manager/flow/flow/{flow_id}")
    
    def enable_flow(self, flow_id: str) -> Dict[str, Any]:
        """Enable a flow."""
        return self.update_flow(flow_id, enabled=True)
    
    def disable_flow(self, flow_id: str) -> Dict[str, Any]:
        """Disable a flow."""
        return self.update_flow(flow_id, enabled=False)
    
    # ========================
    # ADVANCED FLOWS
    # ========================
    
    def get_advanced_flows(self) -> Dict[str, Any]:
        """Get all advanced flows."""
        return self._request("GET", "manager/flow/advancedflow")
    
    def create_advanced_flow(self, name: str, cards: dict = None, enabled: bool = False) -> Dict[str, Any]:
        """Create a new advanced flow."""
        return self._request("POST", "manager/flow/advancedflow", {
            "name": name,
            "enabled": enabled,
            "cards": cards or {}
        })
    
    def delete_advanced_flow(self, flow_id: str) -> Dict[str, Any]:
        """Delete an advanced flow."""
        return self._request("DELETE", f"manager/flow/advancedflow/{flow_id}")
    
    # ========================
    # FLOW HELPERS
    # ========================
    
    def create_device_on_flow(self, name: str, device_id: str, enabled: bool = False) -> Dict[str, Any]:
        """Quick helper: Create a flow that turns on a device (manual trigger)."""
        return self.create_flow(
            name=name,
            trigger={
                "id": "homey:manager:flow:programmatic_trigger",
                "uri": "homey:manager:flow",
                "args": {}
            },
            actions=[{
                "id": f"homey:device:{device_id}:onoff",
                "uri": f"homey:device:{device_id}",
                "args": {"onoff": True},
                "group": "then"
            }],
            enabled=enabled
        )
    
    def create_device_off_flow(self, name: str, device_id: str, enabled: bool = False) -> Dict[str, Any]:
        """Quick helper: Create a flow that turns off a device (manual trigger)."""
        return self.create_flow(
            name=name,
            trigger={
                "id": "homey:manager:flow:programmatic_trigger",
                "uri": "homey:manager:flow",
                "args": {}
            },
            actions=[{
                "id": f"homey:device:{device_id}:onoff",
                "uri": f"homey:device:{device_id}",
                "args": {"onoff": False},
                "group": "then"
            }],
            enabled=enabled
        )
    
    # ========================
    # INSIGHTS & VARIABLES
    # ========================
    
    def get_variables(self) -> Dict[str, Any]:
        """Get all logic variables."""
        return self._request("GET", "manager/logic/variable")
    
    def set_variable(self, variable_id: str, value: Any) -> Dict[str, Any]:
        """Set a logic variable value."""
        return self._request("PUT", f"manager/logic/variable/{variable_id}", {"value": value})
    
    # ========================
    # UTILITY METHODS
    # ========================
    
    def list_devices_summary(self) -> List[Dict[str, str]]:
        """Get a summary list of all devices with their IDs and names."""
        devices = self.get_devices()
        if "error" in devices:
            return devices
        
        summary = []
        for device_id, device in devices.items():
            summary.append({
                "id": device_id,
                "name": device.get("name", "Unknown"),
                "zone": device.get("zoneName", "Unknown"),
                "class": device.get("class", "Unknown"),
                "capabilities": list(device.get("capabilities", []))
            })
        return sorted(summary, key=lambda x: (x["zone"], x["name"]))
    
    def find_device_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a device by name (case-insensitive partial match)."""
        devices = self.get_devices()
        if "error" in devices:
            return devices
        
        name_lower = name.lower()
        for device_id, device in devices.items():
            if name_lower in device.get("name", "").lower():
                return {"id": device_id, **device}
        return None


# ========================
# QUICK TEST
# ========================
if __name__ == "__main__":
    # Load config
    import os
    
    # You'll need to set these
    HOMEY_IP = "192.168.1.13"
    API_KEY = os.environ.get("HOMEY_API_KEY", "YOUR_API_KEY_HERE")
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  Please set your HOMEY_API_KEY environment variable")
        print("   Or update API_KEY in this file")
        print("\n📋 To get an API Key:")
        print("   1. Go to https://my.homey.app")
        print("   2. Settings → API Keys → New API Key")
        print("   3. Select all required permissions")
        print("   4. Copy the key")
    else:
        homey = HomeyController(HOMEY_IP, API_KEY)
        
        print("🏠 Testing Homey Connection...\n")
        
        # Test: Get devices
        print("📱 Devices:")
        devices = homey.list_devices_summary()
        if isinstance(devices, list):
            for d in devices[:10]:  # Show first 10
                print(f"  - {d['name']} ({d['class']}) in {d['zone']}")
                print(f"    ID: {d['id']}")
                print(f"    Capabilities: {', '.join(d['capabilities'][:5])}")
        else:
            print(f"  Error: {devices}")
        
        print("\n📜 Scripts:")
        scripts = homey.get_scripts()
        if "error" not in scripts:
            for script_id, script in scripts.items():
                print(f"  - {script.get('name', 'Unknown')} (ID: {script_id})")
        else:
            print(f"  Error: {scripts}")

