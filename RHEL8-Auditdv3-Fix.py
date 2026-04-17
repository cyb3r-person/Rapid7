# Used to fix "Auditd Compatibility Mode" Rapid7 error
# Intended for RHEL8 Auditd v3

import os
import subprocess

def append_to_audit_rules():
    append_text = """# REQUIRED (for Insight Agent):
# Watch for execve syscalls, change to arch=b32 for 32 bit systems
-a always,exit -F arch=b64 -S execve -F key=execve"""

    audit_rules_path = "/etc/audit/rules.d/audit.rules"

    try:
        with open(audit_rules_path, 'a') as file:
            file.write("\n" + append_text + "\n")
        return "Successfully appended text to audit.rules"
    except FileNotFoundError:
        return "audit.rules file not found"

def update_af_unix_conf():
    new_text = """# This file controls the configuration of the
# af_unix socket plugin. It simply takes events
# and writes them to a unix domain socket. This
# plugin can take 2 arguments, the path for the
# socket and the socket permissions in octal.

# Old Auditd rules prior to enabling compatibility mode
# active = no
# direction = out
# path = /sbin/audisp-af_unix
# type = always
# args = 0640 /var/run/audispd_events
# format = string

# New Auditd rules to enable compatibility mode
active = yes
direction = out
path = builtin_af_unix
type = builtin
args = 0600 /var/run/audispd_events
format = string"""

    file_path = "/etc/audit/plugins.d/af_unix.conf"

    try:
        with open(file_path, 'w') as file:
            file.write(new_text)
        return "Successfully updated af_unix.conf"
    except FileNotFoundError:
        return "af_unix.conf file not found"

def create_audit_conf():
    audit_conf_path = "/opt/rapid7/ir_agent/components/insight_agent/common/audit.conf"
    audit_conf_content = '{"auditd-compatibility-mode":true}'

    try:
        os.makedirs(os.path.dirname(audit_conf_path), exist_ok=True)
        with open(audit_conf_path, 'w') as file:
            file.write(audit_conf_content)
        return "Successfully created audit.conf"
    except Exception as e:
        return f"Failed to create audit.conf: {e}"

def load_audit_rules():
    try:
        subprocess.run(["augenrules", "--load"], check=True)
        return "Successfully loaded audit rules"
    except subprocess.CalledProcessError as e:
        return f"Failed to load audit rules: {e}"

def restart_services():
    try:
        subprocess.run(["service", "auditd", "start"], check=True)
        subprocess.run(["service", "ir_agent", "start"], check=True)
        return "Successfully restarted auditd and ir_agent services"
    except subprocess.CalledProcessError as e:
        return f"Failed to restart services: {e}"

# Example usage
append_result = append_to_audit_rules()
print(f"Part 1 of 5: {append_result}")

update_result = update_af_unix_conf()
print(f"Part 2 of 5: {update_result}")

if update_result == "Successfully updated af_unix.conf":
    create_conf_result = create_audit_conf()
    print(f"Part 3 of 5: {create_conf_result}")

load_result = load_audit_rules()
print(f"Part 4 of 5: {load_result}")

restart_result = restart_services()
print(f"Part 5 of 5: {restart_result}")
