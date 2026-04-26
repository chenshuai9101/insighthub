# 💼 InsightHub — Enterprise Insight Management Dashboard

> **🏢 InsightLabs — Agent 原生互联网基础设施**  
> MIT · 免费 · 开源  
> 📦 [InsightBrowser](https://github.com/chenshuai9101/insightbrowser) · [InsightLens](https://github.com/chenshuai9101/insightlens) · [InsightSee](https://github.com/chenshuai9101/insightsee) · [InsightHub](https://github.com/chenshuai9101/insighthub)  
> ☕ 如果对你有帮助，欢迎捐赠 → assets/ 有收款码

---

SaaS management dashboard for enterprise users. Configure data sources, run analysis workflows, view insight reports. Also includes the **Agent Discovery** view for end users to browse and compare Agent-registered merchants.

## Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Launch (make sure upstream services are running first)
python3 main.py
# → http://localhost:8080      Admin dashboard
# → http://localhost:8080/agent-discover   C-end discovery view
```

## Features

| Feature | Endpoint | Description |
|:--------|:---------|:------------|
| 🏠 Dashboard | `/` | Admin home with stats overview |
| 🔧 Config Wizard | `/config` | 4-step data-source setup |
| 📊 Reports | `/reports` | Visualized insight charts |
| 🏪 Agent Discover | `/agent-discover` | C-end view for real users to browse Agent merchants |
| 💰 Pricing | `/pricing` | Free / ¥29 / ¥99 / ¥499 tiers |

## Integration

InsightHub pulls live data from:
- **Registry** (port 7000) — merchant listings
- **Reliability** (port 7003) — trust ratings

## Architecture

```
User Browser → InsightHub (8080)
                   ├── Registry API (7000) — merchant catalog
                   ├── Reliability API (7003) — trust scores
                   └── SQLite — local session/cache
```

## License

MIT — see LICENSE for details.
