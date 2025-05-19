# DDAI Auto

This tool automates the registration and referral process for DDAI using fake human-like data, solves Cloudflare captchas with 2captcha, and saves account results to JSON. Logs are saved to both the terminal and a log folder.

## Features
- Auto-generate email, username, and password
- Randomly select email providers (gmail, yahoo, hotmail)
- Solve Cloudflare captcha using 2captcha-python
- Register and login to DDAI
- Save account info to JSON
- Logging to terminal and file
- Auto extension ping for all accounts
- Export referral accounts to tokens.json
- Configurable referral code system

## Install Requirements
Run `pip install -r requirements.txt`

## Usage
1. Set your 2captcha API key in `.env.example` then rename to `.env`.
2. Run `python main.py`.
3. Check `logs/` and `results/` for outputs.

## Folder Structure
- `src/` - Main source code
- `logs/` - Log files
- `results/` - JSON account results