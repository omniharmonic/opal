---
id: pattern-quadratic-funding
type: pattern
title: Quadratic Funding
status: staged
confidence: 0.95
source: _inbox/transcripts/sample-podcast-commons.md
extracted_at: 2026-02-02T12:00:00Z
sectors:
  - economic-and-resource-sharing-systems
  - civic-engagement-and-participation-systems
scales:
  - municipal
  - planetary
---

# Quadratic Funding

## Summary

A matching mechanism where small donations from many people are matched more than large donations from few people, helping surface broadly supported public goods.

## Problem

Traditional funding models favor large donors, leading to outcomes that may not reflect broad community preferences. Public goods that many people care about but can't individually fund much get underfunded.

## Solution

The matching formula prioritizes breadth of support:
- 100 people giving $1 each receives MORE matching than 1 person giving $100
- The square root of individual contributions is summed, then squared
- This means many small contributions get amplified through matching

## Context

- Developed from mechanism design and public goods theory
- Implemented at scale by Gitcoin for open source funding
- Can be applied to any public goods funding scenario

## Related Patterns

- [[patterns/participatory-budgeting|Participatory Budgeting]] - alternative allocation method
- [[protocols/dao|Decentralized Autonomous Organization]] - often used together

## Related Organizations

- [[organizations/gitcoin|Gitcoin]] - primary implementer

## Sources

- The Commons Podcast Episode 42 (Dr. Elinor Blake)
