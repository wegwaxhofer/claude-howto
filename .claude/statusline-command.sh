#!/bin/bash
input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')
model=$(echo "$input" | jq -r '.model.display_name // empty')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
five_hour=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
seven_day=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

# PS1-style: user@host:cwd (bold green user@host, bold blue cwd)
ps1_part=$(printf "\033[01;32m%s@%s\033[00m:\033[01;34m%s\033[00m" "$(whoami)" "$(hostname -s)" "${cwd:-$(pwd)}")

# Claude context suffix
suffix=""
[ -n "$model" ] && suffix="$model"
[ -n "$used" ] && suffix="$suffix | ctx:$(printf '%.0f' "$used")%"

# Rate limit info (Claude.ai subscription only)
rate_parts=""
[ -n "$five_hour" ] && rate_parts="5h:$(printf '%.0f' "$five_hour")%"
[ -n "$seven_day" ] && rate_parts="${rate_parts:+$rate_parts }7d:$(printf '%.0f' "$seven_day")%"
[ -n "$rate_parts" ] && suffix="${suffix:+$suffix | }limits:$rate_parts"

# Cached API credit balance (written by /root/.claude/fetch-anthropic-credits.sh via cron)
credit_cache="/root/.claude/anthropic-credits.cache"
if [ -f "$credit_cache" ]; then
  max_age=3600  # 1 hour
  file_age=$(( $(date +%s) - $(stat -c %Y "$credit_cache") ))
  if [ "$file_age" -lt "$max_age" ]; then
    credit_val=$(cat "$credit_cache" 2>/dev/null)
    [ -n "$credit_val" ] && suffix="${suffix:+$suffix | }credits:$credit_val"
  fi
fi

if [ -n "$suffix" ]; then
  printf "%s  [%s]" "$ps1_part" "$suffix"
else
  printf "%s" "$ps1_part"
fi
