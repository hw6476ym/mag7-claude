# Global Supply Chain Explorer — Top 100 Companies

> **An interactive map showing where everything actually comes from.**
> 110 of the world's largest companies → their products → factories → components →
> specialty fabs → refined materials → refineries → mines, oilfields, farms, and
> the electric grid that powers them.

[**▶ Open the live demo**](https://hw6476ym.github.io/top100companies_supplychainFull/)

---

## What it does

Click any node — a company, a product, a chip fab, a refinery, a mine, a power
plant — and trace its full supply chain in either direction. Search by name,
location, or owner. Filter by sector. **🔒 markers flag single-source
chokepoints**, each annotated with how the world routes around the dependency
in practice (sanctions evasion, alternate suppliers, ramp timelines).

```
Company → Product → Assembly Plant → Component → Specialty Fab →
Refined Material → Refinery → Mine / Well / Farm
                ↘ Electricity → Power Plant → Fuel Mine
```

## Coverage

**~110 companies across 12 sectors** (Forbes / S&P 500 / market-cap leaders as of 2025):

| Sector | Examples |
|---|---|
| Big Tech | Apple, Microsoft, Alphabet, Amazon, Meta, Nvidia, Samsung, Sony, Oracle, SAP, Tencent, IBM, Cisco |
| Semiconductor | TSMC, ASML, Broadcom, AMD, Intel, Qualcomm, SK Hynix, Micron, TI, MediaTek, AMAT, Lam, KLA |
| Pharma & Health | Eli Lilly, Novo Nordisk, J&J, Pfizer, Merck, Roche, AstraZeneca, Novartis, AbbVie, UNH, Thermo Fisher, Danaher |
| Oil & Energy | Saudi Aramco, ExxonMobil, Chevron, Shell, TotalEnergies, BP, ConocoPhillips, PetroChina, Equinor |
| Defense / Aerospace | Lockheed Martin, RTX, Northrop Grumman, General Dynamics, BAE, L3Harris, Airbus |
| Automotive | Tesla, Toyota, VW, BYD, GM, Ford, Stellantis, Mercedes, BMW, Honda, Hyundai |
| Finance | Berkshire Hathaway, JPMorgan, Visa, Mastercard, BlackRock, BoA, Wells Fargo, Goldman, Morgan Stanley |
| Consumer & Retail | Walmart, Costco, Home Depot, Target, P&G, Coca-Cola, PepsiCo, Nestlé, LVMH, Hermès, L'Oréal, Unilever, McDonald's |
| Industrial | Boeing, GE Aerospace, Siemens, Caterpillar, Honeywell, ABB, Schneider Electric, 3M |
| Mining & Materials | BHP, Rio Tinto, Glencore |
| Media & Telecom | Disney, Netflix, Comcast, Verizon, AT&T, T-Mobile |
| E-commerce | Alibaba, JD.com, Pinduoduo, MercadoLibre |

Every node is a **named real-world entity** — not a category. Examples:
*TSMC Fab 18 (Tainan)*, *ASML Veldhoven*, *Foxconn Zhengzhou ("iPhone City")*,
*SK Hynix M16*, *Lockheed Fort Worth*, *GD Electric Boat*, *American Pacific
Henderson NV*, *Salar de Atacama*, *Kolwezi DRC*, *Bayan Obo*, *Spruce Pine
quartz*, *Aramco Ghawar*, *Pilbara iron ore*. ~700 nodes, ~1,500 edges.

## Highlights

- **🔒 No-viable-alternative chokepoints** with workaround analysis — ASML EUV,
  TSMC 3nm + CoWoS packaging, SK Hynix HBM3e, Sony micro-OLED, Spruce Pine
  quartz, Bayan Obo rare earths, Foxconn Zhengzhou, Aerojet ammonium-perchlorate,
  BWXT naval reactors, Holston RDX, Lockheed Fort Worth, GD Electric Boat,
  Pantex, Aramco Ghawar, VSMPO Russian titanium, Toray carbon fiber, Novo
  Kalundborg, and more.
- **Defense supply chain end-to-end** — F-35 to titanium sponge to power plants;
  Patriot to ammonium perchlorate; submarines to BWXT naval-reactor fuel.
- **Energy chain** — every fab traces through electricity → nine power-plant
  types → coal/uranium/sun/wind/water. (TSMC alone consumed ~9% of all Taiwan
  power in 2024 — visible directly in the Taipower node.)
- **Retailer "stocks from" feature** — Walmart, Costco, Home Depot, Target detail
  panels list the upstream brands they distribute.
- **Sanctions / disruption analysis** — every chokepoint has a workaround note:
  how Boeing replaced Russian titanium post-2022, why heavy REEs remain ~98%
  Chinese, what India is doing to backstop US 155mm shell production, etc.

## Tech

| Layer | What it is |
|---|---|
| Visualization | [D3.js v7](https://d3js.org/) force-directed graph with custom horizontal-tier layout, arc-curved links, and adjacency-walk chain highlighting |
| Hosting | GitHub Pages (single static HTML, ~160 KB, no build step) |
| Data | Hand-curated from USGS, IEA, BloombergNEF, S&P Commodity Insights, company 10-Ks, and trade press through 2025 |
| Auto-deploy | Claude Code `PostToolUse` hook auto-commits and pushes on save |

No frameworks, no bundler, no backend. The entire app — UI, data model, ~700
nodes, sector colors, force simulation, search, filtering, detail-panel
rendering — lives in **one self-contained HTML file**. View source: it's
intentionally readable.

## How to read the map

- **Left → right flow.** Companies on the left, products → factories → mines
  on the right. Power chain runs parallel.
- **Color = sector** (for tier-1 company nodes) or tier (for everything else).
  See the legend in the left sidebar.
- **Click a node** → the node's full chain lights up; the right sidebar shows
  capacity, owner, location, sector, monopoly notes, and clickable lists of
  upstream / downstream / company / mine connections.
- **🔒** = single-source / no-viable-alternative dependency; click to read the
  *why* and the *how the world routes around it*.
- **⚠** = geopolitical / concentration / ESG flag.
- **Search** matches name, location, or owner. **Sector dropdown** collapses the
  view to one industry's full subgraph.

## Data sources

Public-domain figures compiled from:

- **USGS** Mineral Commodity Summaries (mining + refining capacity)
- **IEA** + **BloombergNEF** (energy mix, EV / battery / grid data)
- **S&P Commodity Insights** + **Wood Mackenzie** (commodity flows)
- **Company filings** — 10-K, annual reports, investor decks
- **Trade press** — Reuters, FT, Nikkei Asia, SemiAnalysis, FactSet through 2025

Capacities shift quarterly — treat as a teaching map, not a procurement document.

## Run locally

```bash
git clone https://github.com/hw6476ym/top100companies_supplychainFull.git
cd top100companies_supplychainFull
# Open index.html directly in a browser, or:
python -m http.server 8000
# then visit http://localhost:8000
```

## License

[MIT](LICENSE) — free to fork, remix, embed, redistribute. Attribution
appreciated but not required.
