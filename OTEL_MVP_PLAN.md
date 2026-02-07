# SONiC-Alpine OpenTelemetry MVP Plan (Painfully Detailed)

## Purpose
Establish the smallest end-to-end telemetry path that proves **gNMI → OTel Collector → Backend** is working in the SONiC-Alpine environment, with **explicit justifications** for every step. This is intentionally minimal and does **not** attempt full container coverage, log ingestion, Redis polling, dashboards, or TLS hardening.

## MVP Scope (Strict)
- **Signals:** Metrics only (no logs, no traces).
- **Sources:** gNMI (from sonic-gnmi) + optional hostmetrics (collector self/host basics).
- **Targets:** Prometheus remote_write **or** debug exporter (Prometheus preferred if available).
- **Paths:**
  - Interface counters (openconfig-interfaces) for one interface.
  - BGP global state (openconfig-network-instance) for basic control-plane telemetry.

## MVP Non-Goals (Explicitly Excluded)
- Redis direct polling.
- Filelog ingestion.
- Per-container coverage matrix.
- Centralized backend stack (Grafana/Jaeger).
- TLS/mTLS and auth.
- Persistent queues, retries tuning, or memory pressure testing.
- Stress testing or outage simulations.

---

## Step-by-Step Plan with Justification

### Step 0 — Confirm Environment Assumptions (No changes yet)
**Goal:** Avoid chasing false failures caused by missing binaries or disabled services.

**Actions (human-checked):**
1) **Confirm the sonic-gnmi service is enabled** in the SONiC container.
   - *Justification:* gNMI is the only telemetry source for MVP; if it is disabled, nothing downstream can work.
2) **Confirm the otelcol-contrib binary exists** in the OTel container.
   - *Justification:* Collector absence creates a total block; validate before touching configs.
3) **Confirm gNMI port reachability (9339)** from the collector sidecar or pod.
   - *Justification:* gNMI is a network service; if the port is blocked or binding is wrong, all gNMI subscriptions fail.

**Exit Criteria:**
- gNMI server is enabled and reachable.
- Collector binary exists and runs `--version`.

---

### Step 1 — Establish gNMI Data Truth (Read-only validation)
**Goal:** Prove gNMI can return at least one counter and one control-plane state.

**Actions (read-only):**
1) **Run gNMI capabilities**.
   - *Justification:* Confirms the target supports required YANG models. If capabilities don’t list openconfig modules, subscription paths below are invalid.
2) **Fetch interface counters for one interface** (e.g., Ethernet0).
   - *Justification:* Counter paths are the primary network telemetry; confirming basic GET is the simplest proof that gNMI is wired through translib/YANG.
3) **Fetch BGP global state**.
   - *Justification:* Provides a control-plane data point and prevents the MVP from being limited to L2/L3 interface stats only.

**Exit Criteria:**
- gNMI returns a valid payload for interface counters.
- gNMI returns a valid payload for BGP global state.

---

### Step 2 — Define the Minimal Collector Config (No code, plain structure)
**Goal:** Keep collector configuration as small as possible while still functional.

**Configuration Intent (structure, not code):**
- **Receiver:** gNMI only.
- **Processor:** batch (default behavior) only.
- **Exporter:** one backend (Prometheus remote_write preferred) or debug.
- **Pipeline:** a single metrics pipeline.

**Justification:**
- Removing extra receivers/processors reduces failure modes and isolates gNMI data path issues.
- Avoiding logs/traces reduces scope and keeps the configuration auditable.
- A single pipeline clarifies success/failure and avoids cross-signal confusion.

**Exit Criteria:**
- Collector configuration is minimal and human-auditable.
- No placeholders for future features (avoid adding TODOs that expand scope).

---

### Step 3 — Start Collector and Verify gNMI Subscription Sync
**Goal:** Validate that collector successfully subscribes to gNMI paths and receives data.

**Actions:**
1) **Start collector with the minimal config.**
   - *Justification:* If the collector can’t start cleanly, downstream verification is meaningless.
2) **Inspect collector logs for gNMI subscription sync.**
   - *Justification:* gNMI receivers typically log a “sync_response” or similar indicator; this confirms the subscription is active and data is flowing.

**Exit Criteria:**
- Collector starts without fatal errors.
- gNMI subscription reports a successful sync.

---

### Step 4 — Verify Telemetry Delivery to a Backend (Single Sink)
**Goal:** Prove end-to-end delivery from gNMI into a backend.

**Actions (choose one path):**
1) **Prometheus remote_write path**
   - Validate that time-series appear (interface counters and BGP global).
   - *Justification:* This is the most realistic MVP outcome and demonstrates the data path is production-viable.
2) **Debug exporter path** (if Prometheus is not available)
   - Validate metrics appear in collector logs.
   - *Justification:* Debug exporter is a low-friction fallback to show that the collector is receiving and processing data, even without a backend.

**Exit Criteria:**
- At least one interface counter time-series is visible in the backend.
- BGP global state shows up as metrics (if BGP is enabled in the environment).

---

### Step 5 — Document MVP Completion and Boundaries
**Goal:** Prevent scope creep and lock in what “done” means for MVP.

**Actions:**
1) **Record the exact gNMI paths used** and confirm they were successful.
   - *Justification:* Future expansion should build on verified paths, not assumptions.
2) **Record the backend target and expected series names**.
   - *Justification:* This is the minimal contract for later dashboard/alert work.
3) **Explicitly note excluded items** (Redis polling, logs, TLS, dashboards).
   - *Justification:* Avoids stakeholders assuming those features are done or in-progress.

**Exit Criteria:**
- MVP outcomes are documented and reproducible.
- Scope boundaries are explicit and agreed.

---

## MVP Success Checklist (Binary Outcomes)
- [ ] gNMI capabilities return required models.
- [ ] gNMI GET for interface counters works.
- [ ] gNMI GET for BGP global state works (if BGP enabled).
- [ ] Collector starts and shows subscription sync.
- [ ] Metrics appear in backend (Prometheus or debug).

## MVP Failure Triage (If Something Breaks)
- **No gNMI response:** Verify gNMI service and port 9339; confirm telemetry feature state.
- **Collector won’t start:** Validate config for minimal structure; remove all optional processors/exporters.
- **No metrics in backend:** Confirm exporter endpoint; fall back to debug exporter to isolate exporter issues.

## MVP Upgrade Path (What comes after MVP)
1) Add hostmetrics for basic process stats.
2) Add additional gNMI paths (LLDP, platform).
3) Add Prometheus/Grafana dashboards.
4) Add logs with filelog receiver.
5) Add reliability features (queues/retries).
6) Add TLS/mTLS and auth.
7) Add Redis polling for unmapped counters.

---

## Why this is the minimum viable path
- It proves **the core gNMI telemetry contract** before any infrastructure or complexity is layered on top.
- It keeps every step **observable and reversible**.
- It makes the smallest set of changes needed to claim “telemetry works end-to-end.”
