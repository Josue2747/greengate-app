# 🌿 GreenGate

**Universal Geo-Compliance API** — Validate land parcels against environmental and regulatory datasets in seconds.

[![API Status](https://img.shields.io/badge/API-Live-brightgreen)]()
[![License](https://img.shields.io/badge/License-Proprietary-blue)]()

---

## What is GreenGate?

GreenGate is a geospatial validation engine that checks if land parcels overlap with protected areas, deforestation alerts, indigenous territories, and other regulatory layers.

**Use cases:**
- 🌱 Agricultural supply chain compliance
- 🏦 ESG due diligence for land-based investments
- 📋 Regulatory reporting automation
- 🛰️ Real-time deforestation monitoring integration

---

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Your App   │────▶│  GreenGate  │────▶│   Result    │
│  (GeoJSON)  │     │     API     │     │  (JSON/PDF) │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │  Reference  │
                    │   Layers    │
                    │  (PostGIS)  │
                    └─────────────┘
```

1. **Send** a polygon (farm, plot, concession)
2. **Receive** compliance status + risk score + detailed report

---

## Quick Start

### Validate a Parcel

```bash
curl -X POST https://api.greengate.app/v1/validations/quick \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "type": "Polygon",
    "coordinates": [[[-46.5,-23.5],[-46.5,-23.51],[-46.49,-23.51],[-46.49,-23.5],[-46.5,-23.5]]]
  }'
```

### Response

```json
{
  "status": "approved",
  "risk_score": 100,
  "checks": [
    {"type": "deforestation", "status": "pass"},
    {"type": "indigenous_territory", "status": "pass"},
    {"type": "protected_areas", "status": "pass"}
  ]
}
```

---

## Features

| Feature | Description |
|---------|-------------|
| ⚡ Fast | ~150ms average response time |
| 🔒 Secure | API key authentication, rate limiting |
| 📊 Auditable | Full audit trail with cryptographic hashes |
| 📄 Reports | PDF generation for due diligence |
| 🌍 Scalable | Cloud-native, PostgreSQL + PostGIS |

---

## Supported Reference Layers

- Deforestation alerts (satellite-based)
- Indigenous territories
- Conservation units
- Water protection areas (APP)
- Environmental embargoes
- Rural property boundaries

*Custom layers available on request.*

---

## API Documentation

📚 Full API docs available at `/docs` endpoint.

---

## Self-Hosted Deployment

See [`docs/deploy.md`](docs/deploy.md) for deployment instructions.

**Requirements:**
- Docker + Docker Compose
- PostgreSQL 14+ with PostGIS

---

## License

Proprietary. Contact for licensing information.

---

<p align="center">
  <sub>Built with 🌱 for a sustainable future</sub>
</p>
