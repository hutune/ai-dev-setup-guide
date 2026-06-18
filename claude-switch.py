#!/usr/bin/env python3
"""Claude Code switch helper — quản lý .claude.json + macOS Keychain"""
import json, os, shutil, sys, subprocess

CLAUDE_JSON = os.path.expanduser('~/.claude.json')
CLAUDE_BACKUP = os.path.expanduser('~/.claude.json.backup')
KEYCHAIN_BACKUP = os.path.expanduser('~/.claude-keychain.bak')
KEYCHAIN_SERVICE = 'Claude Code-credentials'
KEYCHAIN_ACCOUNT = os.environ.get('USER', os.getlogin())

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def keychain_get():
    r = run(['security', 'find-generic-password', '-s', KEYCHAIN_SERVICE,
             '-a', KEYCHAIN_ACCOUNT, '-w'])
    return r.stdout.strip() if r.returncode == 0 else None

def keychain_delete():
    run(['security', 'delete-generic-password', '-s', KEYCHAIN_SERVICE,
         '-a', KEYCHAIN_ACCOUNT])

def keychain_add(pw):
    run(['security', 'add-generic-password', '-s', KEYCHAIN_SERVICE,
         '-a', KEYCHAIN_ACCOUNT, '-w', pw])

mode = sys.argv[1] if len(sys.argv) > 1 else ''

if mode == 'anti':
    d = json.load(open(CLAUDE_JSON))
    if 'oauthAccount' in d:
        shutil.copy2(CLAUDE_JSON, CLAUDE_BACKUP)
        del d['oauthAccount']
    d['hasCompletedOnboarding'] = True
    # Xóa rejected keys + auto-approve API key
    if 'customApiKeyResponses' not in d:
        d['customApiKeyResponses'] = {'approved': [], 'rejected': []}
    d['customApiKeyResponses']['rejected'] = []
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if api_key and api_key not in d['customApiKeyResponses'].get('approved', []):
        d['customApiKeyResponses']['approved'] = [api_key]
    json.dump(d, open(CLAUDE_JSON, 'w'), indent=2)
    pw = keychain_get()
    if pw:
        with open(KEYCHAIN_BACKUP, 'w') as f:
            f.write(pw)
        keychain_delete()
    print('OK')

elif mode == 'real':
    if os.path.exists(CLAUDE_BACKUP):
        shutil.copy2(CLAUDE_BACKUP, CLAUDE_JSON)
    else:
        d = json.load(open(CLAUDE_JSON))
        d['hasCompletedOnboarding'] = True
        json.dump(d, open(CLAUDE_JSON, 'w'), indent=2)
    if os.path.exists(KEYCHAIN_BACKUP):
        pw = open(KEYCHAIN_BACKUP).read().strip()
        if pw:
            keychain_delete()
            keychain_add(pw)
    print('OK')

else:
    print('Usage: claude-switch.py [anti|real]' )