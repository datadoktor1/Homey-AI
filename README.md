# Homey-AI

Program and control an [Athom Homey](https://homey.app) smart-home hub from your AI IDE. Automation
logic is written as **HomeyScript** (JavaScript that runs on the hub) and deployed
with a small Python toolkit over Homey's local REST API.

<img width="1539" height="1034" alt="image" src="https://github.com/user-attachments/assets/4743880c-f2c9-4fbe-afe8-796ba52454f7" />

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
