# Day 28 — Multi-Step AI Workflows with State Management

## Overview

This project implements a multi-step AI research workflow with state
management, checkpointing, error handling, and resume functionality.

The workflow breaks a research task into four independent stages:

1. Search Sources
2. Extract Key Points
3. Synthesise Findings
4. Format Report

The workflow state is persisted after each completed stage so that the
system can resume from the latest successful checkpoint after a failure.

---

## Architecture

```text
User Topic
    |
    v
+----------------------+
|  Search Sources      |
+----------------------+
    |
    v
[Checkpoint]
    |
    v
+----------------------+
| Extract Key Points   |
+----------------------+
    |
    v
[Checkpoint]
    |
    v
+----------------------+
| Synthesise Findings  |
+----------------------+
    |
    v
[Checkpoint]
    |
    v
+----------------------+
| Format Report        |
+----------------------+
    |
    v
[Final Report]