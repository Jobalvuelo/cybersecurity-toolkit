# Writeup: Hostel Network Security Audit

## Overview

**Type:** Black-box penetration test
**Target:** Hospitality business network (North Africa)
**Date:** February 2026
**Devices found:** 23
**Critical vulnerabilities:** 3
**Authorization:** Written permission from owner

## Methodology

Followed NIST Cybersecurity Framework. Connected to guest WiFi as a regular guest would, then performed:

1. Network discovery with nmap -sn to map all devices
2. Service and version detection with nmap -sV on infrastructure devices
3. Default credential testing on all admin panels
4. Firmware version analysis
5. Network architecture review

## Findings Summary

| Severity | Count | Description |
|----------|-------|-------------|
| CRITICAL | 3 | Default credentials on router, camera system, WiFi extenders |
| HIGH | 4 | No network segmentation, outdated SSH, UPnP enabled, outdated firmware |
| MEDIUM | 2 | Unmonitored network, unknown devices |

## Critical Findings

### C-01: Router — Factory Default Credentials

The main router had default admin/admin credentials. Any guest on the WiFi could access the admin panel and modify DNS settings, firewall rules, or lock out the administrator. SSH exposed (version from 2014 with known CVEs) and UPnP enabled.

### C-02: Camera System — Default Credentials + Outdated Firmware

An 8-channel DVR security camera system was accessible with common default credentials. Full access to live feeds, recordings, alarm settings, and system configuration. Firmware dated 2021 with update available but not installed.

### C-03: WiFi Extenders — No Authentication Required

Three WiFi range extenders had admin panels accessible without any password. Running embedded web server with known vulnerabilities. Firmware outdated.

## Impact

Any guest connected to the hostel WiFi could:

- View all 8 live security camera feeds
- Access and delete camera recordings
- Change the WiFi password for all guests
- Modify DNS settings to redirect guest traffic
- Disable the firewall

## Tools Used

- Nmap 7.95 (network discovery, service detection)
- Custom Python tools (IR Toolkit, Web Scanner, Network Monitor)
- Firefox DevTools (web interface analysis)

## Recommendations Delivered

**Immediate:** Change all default passwords, enable guest network isolation

**Short-term:** Update all firmware, disable UPnP, disable/update SSH

**Long-term:** Implement network monitoring, restrict admin access, quarterly reviews

## Full Report

See [Portfolio version (redacted)](../reports/Security_Audit_Report_Portfolio.pdf)