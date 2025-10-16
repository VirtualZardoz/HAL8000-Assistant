---
title: Rate Limiting Patterns
date_ingested: 2025-10-16
source: direct input (test)
category: library
subcategory: patterns
tags: rate-limiting, api-design, system-stability, scalability, patterns
---

# Rate Limiting Patterns

Rate limiting is a technique to control the rate of requests to a system or API. Common patterns include:

## Token Bucket
- Tokens added at fixed rate
- Each request consumes a token
- Requests blocked when bucket empty

## Leaky Bucket
- Requests processed at constant rate
- Excess requests queued
- Queue overflow results in rejection

## Fixed Window
- Count requests in fixed time windows
- Simple but has boundary issues

## Sliding Window
- More accurate than fixed window
- Tracks requests in rolling time period

These patterns are essential for API design and system stability.

---

**Metadata:**
- Ingested: 2025-10-16
- Source: direct input (test)
- Classification: library/patterns (confidence: high)
- Related: None found (new content)
