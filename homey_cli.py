"""
Homey Interactive CLI - Control your Homey from the command line
"""
import json
import sys
from homey_control import HomeyController
from config import HOMEY_IP, HOMEY_API_KEY


def print_json(data, indent=2):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=indent, default=str))


def main():
    if not HOMEY_API_KEY:
        print("❌ No API Key configured!")
        print("\n📋 To get an API Key:")
        print("   1. Go to https://my.homey.app")
        print("   2. Settings → API Keys → New API Key")
        print("   3. Select all required permissions")
        print("   4. Paste the key in config.py or set HOMEY_API_KEY env var")
        sys.exit(1)
    
    homey = HomeyController(HOMEY_IP, HOMEY_API_KEY)
    print(f"🏠 Connected to Homey at {HOMEY_IP}")
    print("Type 'help' for available commands\n")
    
    while True:
        try:
            cmd = input("homey> ").strip()
            if not cmd:
                continue
            
            parts = cmd.split(maxsplit=2)
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            # ========================
            # GENERAL COMMANDS
            # ========================
            if command in ("quit", "exit", "q"):
                print("👋 Bye!")
                break
            
            elif command == "help":
                print("""
📋 AVAILABLE COMMANDS:

DEVICES:
  devices                  - List all devices
  device <id>             - Get device details
  on <device_id>          - Turn device on
  off <device_id>         - Turn device off
  dim <device_id> <0-100> - Set brightness %
  set <device_id> <cap> <value> - Set any capability
  find <name>             - Find device by name

HOMEYSCRIPT:
  scripts                 - List all scripts
  script <id>            - Get script details/code
  run <script_id>        - Run a script
  code <javascript>      - Run arbitrary code directly
  newscript <name> <code> - Create new script
  updatescript <id> <code> - Update script code
  deletescript <id>       - Delete a script

FLOWS:
  flows                   - List all flows
  flow <id>              - Get flow details
  trigger <flow_id>      - Trigger a flow
  newflow <name>         - Create flow (turns on device, prompts for device)
  deleteflow <id>        - Delete a flow
  enableflow <id>        - Enable a flow
  disableflow <id>       - Disable a flow
  advflows               - List advanced flows

ZONES & VARIABLES:
  zones                   - List all zones
  vars                    - List all variables
  setvar <id> <value>    - Set variable value

OTHER:
  raw <endpoint>          - Make raw GET request
  help                    - Show this help
  quit                    - Exit
""")
            
            # ========================
            # DEVICE COMMANDS
            # ========================
            elif command == "devices":
                devices = homey.list_devices_summary()
                if isinstance(devices, list):
                    print(f"\n📱 Found {len(devices)} devices:\n")
                    current_zone = None
                    for d in devices:
                        if d['zone'] != current_zone:
                            current_zone = d['zone']
                            print(f"\n🏠 {current_zone}")
                            print("-" * 40)
                        caps = ', '.join(d['capabilities'][:4])
                        if len(d['capabilities']) > 4:
                            caps += f" +{len(d['capabilities'])-4} more"
                        print(f"  {d['name']}")
                        print(f"    ID: {d['id']}")
                        print(f"    Class: {d['class']}, Caps: {caps}")
                else:
                    print_json(devices)
            
            elif command == "device" and args:
                device = homey.get_device(args[0])
                print_json(device)
            
            elif command == "find" and args:
                name = " ".join(args)
                device = homey.find_device_by_name(name)
                if device:
                    print(f"\n✅ Found: {device.get('name')}")
                    print(f"   ID: {device.get('id')}")
                    print(f"   Zone: {device.get('zoneName')}")
                    print(f"   Class: {device.get('class')}")
                    print(f"   Capabilities: {', '.join(device.get('capabilities', []))}")
                else:
                    print(f"❌ No device found matching '{name}'")
            
            elif command == "on" and args:
                result = homey.turn_on(args[0])
                print("✅ Turned on" if "error" not in result else f"❌ {result}")
            
            elif command == "off" and args:
                result = homey.turn_off(args[0])
                print("✅ Turned off" if "error" not in result else f"❌ {result}")
            
            elif command == "dim" and len(args) >= 2:
                level = float(args[1]) / 100  # Convert percentage to 0-1
                result = homey.set_brightness(args[0], level)
                print(f"✅ Set brightness to {args[1]}%" if "error" not in result else f"❌ {result}")
            
            elif command == "set" and len(args) >= 3:
                device_id, capability = args[0], args[1]
                value = args[2]
                # Try to parse value as JSON/number/bool
                try:
                    value = json.loads(value.lower())
                except:
                    try:
                        value = float(value)
                    except:
                        pass
                result = homey.set_device_capability(device_id, capability, value)
                print(f"✅ Set {capability}={value}" if "error" not in result else f"❌ {result}")
            
            # ========================
            # SCRIPT COMMANDS
            # ========================
            elif command == "scripts":
                scripts = homey.get_scripts()
                if "error" not in scripts:
                    print(f"\n📜 Found {len(scripts)} scripts:\n")
                    for script_id, script in scripts.items():
                        print(f"  {script.get('name', 'Unnamed')}")
                        print(f"    ID: {script_id}")
                else:
                    print_json(scripts)
            
            elif command == "script" and args:
                script = homey.get_script(args[0])
                if "error" not in script:
                    print(f"\n📜 Script: {script.get('name')}")
                    print(f"   ID: {script.get('id')}")
                    print("\n--- CODE ---")
                    print(script.get('code', 'No code'))
                    print("--- END ---")
                else:
                    print_json(script)
            
            elif command == "run" and args:
                print(f"🚀 Running script {args[0]}...")
                result = homey.run_script(args[0])
                print("\n📤 Result:")
                print_json(result)
            
            elif command == "code" and args:
                code = " ".join(args)
                print(f"🚀 Running code...")
                result = homey.run_code(code)
                print("\n📤 Result:")
                print_json(result)
            
            elif command == "updatescript" and len(args) >= 2:
                script_id = args[0]
                code = args[1] if len(args) > 1 else ""
                result = homey.update_script(script_id, code)
                print("✅ Script updated" if "error" not in result else f"❌ {result}")
            
            elif command == "newscript" and len(args) >= 1:
                name = args[0]
                code = args[1] if len(args) > 1 else "// New script\nreturn 'Hello!';"
                result = homey.create_script(name, code)
                if "error" not in result:
                    print(f"✅ Script created with ID: {result.get('id')}")
                else:
                    print(f"❌ {result}")
            
            elif command == "deletescript" and args:
                result = homey.delete_script(args[0])
                print("✅ Script deleted" if "error" not in result else f"❌ {result}")
            
            # ========================
            # FLOW COMMANDS
            # ========================
            elif command == "flows":
                flows = homey.get_flows()
                if "error" not in flows:
                    print(f"\n⚡ Found {len(flows)} flows:\n")
                    for flow_id, flow in flows.items():
                        enabled = "✅" if flow.get('enabled') else "❌"
                        print(f"  {enabled} {flow.get('name')}")
                        print(f"     ID: {flow_id}")
                else:
                    print_json(flows)
            
            elif command == "flow" and args:
                flow = homey.get_flow(args[0])
                if "error" not in flow:
                    print(f"\n⚡ Flow: {flow.get('name')}")
                    print(f"   ID: {flow.get('id')}")
                    print(f"   Enabled: {flow.get('enabled')}")
                    print(f"   Triggerable: {flow.get('triggerable')}")
                    print(f"\n   Trigger: {flow.get('trigger', {}).get('id')}")
                    print(f"   Conditions: {len(flow.get('conditions', []))}")
                    print(f"   Actions: {len(flow.get('actions', []))}")
                    print("\n--- FULL JSON ---")
                    print_json(flow)
                else:
                    print_json(flow)
            
            elif command == "trigger" and args:
                print(f"⚡ Triggering flow {args[0]}...")
                result = homey.trigger_flow(args[0])
                print("✅ Flow triggered" if "error" not in result else f"❌ {result}")
            
            elif command == "newflow" and args:
                name = args[0]
                print(f"Creating flow '{name}'...")
                print("Enter device ID for the action (or 'list' to see devices):")
                device_input = input("  device> ").strip()
                
                if device_input.lower() == 'list':
                    devices = homey.list_devices_summary()
                    if isinstance(devices, list):
                        for d in devices[:15]:
                            print(f"    {d['name']}: {d['id']}")
                    device_input = input("  device> ").strip()
                
                if device_input:
                    result = homey.create_device_on_flow(name, device_input, enabled=False)
                    if "error" not in result:
                        print(f"✅ Flow created with ID: {result.get('id')}")
                        print("   (disabled by default, use 'enableflow <id>' to enable)")
                    else:
                        print(f"❌ {result}")
                else:
                    print("❌ No device ID provided")
            
            elif command == "deleteflow" and args:
                result = homey.delete_flow(args[0])
                print("✅ Flow deleted" if "error" not in result else f"❌ {result}")
            
            elif command == "enableflow" and args:
                result = homey.enable_flow(args[0])
                print("✅ Flow enabled" if "error" not in result else f"❌ {result}")
            
            elif command == "disableflow" and args:
                result = homey.disable_flow(args[0])
                print("✅ Flow disabled" if "error" not in result else f"❌ {result}")
            
            elif command == "advflows":
                flows = homey.get_advanced_flows()
                if "error" not in flows:
                    print(f"\n⚡ Found {len(flows)} advanced flows:\n")
                    for flow_id, flow in flows.items():
                        enabled = "✅" if flow.get('enabled') else "❌"
                        print(f"  {enabled} {flow.get('name')}")
                        print(f"     ID: {flow_id}")
                else:
                    print_json(flows)
            
            # ========================
            # ZONE/VAR COMMANDS
            # ========================
            elif command == "zones":
                zones = homey.get_zones()
                if "error" not in zones:
                    print(f"\n🏠 Found {len(zones)} zones:\n")
                    for zone_id, zone in zones.items():
                        print(f"  {zone.get('name')}")
                        print(f"    ID: {zone_id}")
                else:
                    print_json(zones)
            
            elif command == "vars":
                variables = homey.get_variables()
                if "error" not in variables:
                    print(f"\n📊 Found {len(variables)} variables:\n")
                    for var_id, var in variables.items():
                        print(f"  {var.get('name')}: {var.get('value')} ({var.get('type')})")
                        print(f"    ID: {var_id}")
                else:
                    print_json(variables)
            
            elif command == "setvar" and len(args) >= 2:
                var_id = args[0]
                value = args[1]
                try:
                    value = json.loads(value.lower())
                except:
                    try:
                        value = float(value)
                    except:
                        pass
                result = homey.set_variable(var_id, value)
                print(f"✅ Variable set to {value}" if "error" not in result else f"❌ {result}")
            
            # ========================
            # RAW REQUESTS
            # ========================
            elif command == "raw" and args:
                endpoint = args[0]
                result = homey._request("GET", endpoint)
                print_json(result)
            
            else:
                print(f"❓ Unknown command: {cmd}")
                print("   Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n👋 Bye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

