# Homey-AI

Program and control an [Athom Homey](https://homey.app) smart-home hub from your AI IDE. Automation
logic is written as **HomeyScript** (JavaScript that runs on the hub) and deployed
with a small Python toolkit over Homey's local REST API.

Your AI can program your Homey automatically!

Did you know that you can log in to your Homey on the local network? Using this access you can have Cursor, Claude, Antigravity or any other AI, program your Homey automatically using HomeyScript. It modifies the scripts using AI and uploads them to Homey.

This is very powerful, and once it is set up, anyone can make advanced scripts without any programming knowledge.

Just tell the AI what you want done:

“Set up Light1. At sunset turn it on, at 01:00 off, at 06:00 on, at sunup turn it off. Make sure the long summer nights doesnt mess with the schedule.”

“Make Button1 control Light1. Pressing On once turns it on, pressing Off once turns it off. Pressing On twice or more increases the brightness by 10%. Pressing Off twice or more decreases it. Holding Off for more than 1 sec turns off all lights in the Kitchen.”

And you can control devices directly:

“Turn on Light1.”

The trick is to have the AI create flows for the device, that calls a HomeyScript that does all the work:
<img width="385" height="259" alt="image" src="https://github.com/user-attachments/assets/7b4eb13c-029e-47a4-a8bd-d1d7f9a4da61" />

<img width="385" height="259" alt="image" src="https://github.com/user-attachments/assets/4743880c-f2c9-4fbe-afe8-796ba52454f7" />

And most importantly, a global script that runs every minute to trigger timers:
<img width="385" height="259" alt="image" src="https://github.com/user-attachments/assets/3708e881-b0b9-49a8-bf57-f04b1345c8c6" />

## Quickstart

```bash
cp config.example.py config.py            # add your HOMEY_IP and API key
pip install -r requirements.txt
python homey_cli.py                        # verify: type `devices`
```

## Full guide

See **[docs/GUIDE.md](docs/GUIDE.md)** for how to find your Homey's IP, create an API
key with the right scopes, set up Cursor/VS Code, and the edit -> push -> run workflow.

> Secrets (`config.py`, `api.txt`) are git-ignored. Never commit your API key.
