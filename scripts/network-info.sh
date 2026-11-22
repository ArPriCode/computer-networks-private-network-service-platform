#!/bin/bash
set -euo pipefail

printf 'Interface: '
route get default 2>/dev/null | awk '/interface/{print $2}'

printf '\nIPv4 addresses:\n'
ifconfig | awk '/inet / && $2 != "127.0.0.1" {print $2}'

printf '\nSubnet masks:\n'
ifconfig | awk '/netmask/{print $4}'

printf '\nDefault gateway:\n'
route get default 2>/dev/null | awk '/gateway/{print $2}'

printf '\nListening project ports:\n'
netstat -anv | grep -E '\.(53|3001|3002|8443)[[:space:]]' | head -20 || true