# SONiC-Alpine OpenTelemetry (OTel) Integration Plan

## Purpose
This plan is intentionally split into **three** documents to keep the file map simple and reduce navigation overhead.

## File Map (Simplified)
1) **`OTEL_MVP_PLAN.md`**
   - The minimal, step-by-step MVP with justifications and exit criteria.
2) **`OTEL_IMPLEMENTATION_PLAN.md`**
   - Full implementation plan including architecture, phases, backend integration, validation, telemetry matrix, alternatives, and risks.
3) **`OTEL_INTEGRATION_PLAN.md`** (this file)
   - The index/landing page that explains how to use the other two documents.

## How to Use
- Start with **`OTEL_MVP_PLAN.md`** to get a working gNMI → Collector → Backend pipeline.
- Only after MVP succeeds, use **`OTEL_IMPLEMENTATION_PLAN.md`** to expand coverage, add backends, and harden reliability.

## Minimum Viable Path (One-Paragraph Summary)
Validate gNMI responses, configure a minimal collector with a gNMI receiver and one exporter, and confirm metrics land in a backend. Everything else (Redis polling, logs, dashboards, TLS, stress tests) is deferred until the MVP data path is proven.
