#!/usr/bin/env bash

set -u

root="${1:-src}"
if [ ! -d "$root" ]; then
  printf 'Motion policy: ERROR: path not found: %s\n' "$root" >&2
  exit 2
fi

violations=0
warnings=0

scan() {
  local pattern="$1"
  local message="$2"
  local matches
  matches="$(grep -RInE \
    --exclude-dir=node_modules \
    --exclude-dir=dist \
    --exclude-dir=build \
    --exclude='*.map' \
    "$pattern" "$root" 2>/dev/null || true)"
  if [ -n "$matches" ]; then
    printf 'ERROR: %s\n%s\n' "$message" "$matches"
    violations=$((violations + 1))
  fi
}

scan 'transition-all|transition:[[:space:]]*all' \
  'Use explicit transition properties; transition-all is not allowed.'
scan "from[[:space:]]+['\"](gsap|react-spring|@react-spring|lottie-react|react-transition-group)" \
  'Unapproved animation library import; record a UI Spec exception first.'
scan 'animate-(bounce|ping|wiggle)' \
  'Decorative or strong bounce animation requires an explicit exception.'

motion_sources="$(grep -RIlE \
  --exclude-dir=node_modules \
  --exclude-dir=dist \
  --exclude-dir=build \
  --exclude='*.map' \
  'transition|data-state|prefers-reduced-motion|useReducedMotion|<motion\\.|keyframes|animate-' \
  "$root" 2>/dev/null || true)"
if [ -n "$motion_sources" ]; then
  reduced_motion="$(grep -RIlE \
    --exclude-dir=node_modules \
    --exclude-dir=dist \
    --exclude-dir=build \
    --exclude='*.map' \
    'prefers-reduced-motion|useReducedMotion|reducedMotion' \
    "$root" 2>/dev/null || true)"
  if [ -z "$reduced_motion" ]; then
    printf 'WARNING: motion sources found but no reduced-motion guard was detected under %s.\n' "$root"
    warnings=$((warnings + 1))
  fi
fi

if [ "$violations" -gt 0 ]; then
  printf 'Motion policy: FAIL (%s violation group(s), %s warning(s))\n' "$violations" "$warnings"
  exit 1
fi

printf 'Motion policy: PASS (%s warning(s))\n' "$warnings"
