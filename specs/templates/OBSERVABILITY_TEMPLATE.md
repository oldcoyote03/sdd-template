# Observability Specification Template

## Overview

This template defines what data to monitor, what signals matter, and how to alert when conditions arise.

## Structure

### Data Sources & Feeds

- **Source Name**: What data are we ingesting?
- **Data Type**: Prices, volumes, events, metrics?
- **Feed Specification**: Where does it come from? (API, file, stream, etc.)
- **Update Frequency**: Real-time, daily, on-demand?
- **Retention**: How long do we keep this data?

### Metrics & Signals

- **Metric Name**: What are we measuring?
- **Calculation**: How is it derived from raw data?
- **Baseline/Reference**: What's normal? What are we comparing against?
- **Relevance**: Why does this metric matter for decisions?

### Alert Conditions

- **Condition Name**: What pattern/threshold triggers an alert?
- **Condition Logic**: How is it evaluated? (threshold, pattern, anomaly, etc.)
- **Alert Urgency**: Critical, high, medium, low?
- **Alert Recipients**: Who gets notified and how?

### Dashboards & Visualizations

- **Dashboard Name**: What visualization is useful?
- **Metrics Included**: Which signals go on this dashboard?
- **Refresh Cadence**: How often is it updated?
- **Audience**: Who needs to see this?

## Usage

Observability Agents will read this spec to determine:
- "What data should I be monitoring?"
- "When should I alert?"
- "What's important to visualize?"

Be specific about thresholds, update frequencies, and alert recipients.
