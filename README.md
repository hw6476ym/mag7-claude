# TOP 100 COMPANIES Supply Chain Explorer

Interactive 8-tier supply-chain map of the top companies of the world all the
way down to **mines, wells, farms — and the electric grid**.

Coverage: **~110 companies across 12 sectors** — Big Tech, Semiconductor,
Pharma & Health, Oil & Energy, Finance, Automotive, Consumer Goods, Retail,
Industrial, **Defense / Aerospace**, Media / Telecom, E-commerce, and
**Mining & Materials**.

**Company → Product → Assembly Plant → Component → Specialty Fab → Refined Material → Refinery → Mine / Well / Farm**

Plus a parallel **energy chain** — every fab traces through electricity → power
plants (gas, nuclear, coal, hydro, solar, wind, geothermal, Taiwan grid, Korea
grid) → fuel mines / wells / sun / wind.

Every node is a real, named entity — e.g. *TSMC Fab 18 (Tainan)*,
*ASML Veldhoven*, *SK Hynix M16*, *Foxconn Zhengzhou*, *Lockheed Fort Worth*,
*GD Electric Boat*, *American Pacific Henderson NV*, *Salar de Atacama*,
*Kolwezi DRC*, *Bayan Obo*, *Spruce Pine quartz*, *Aramco Ghawar* — with
location, owner, capacity, sector, and chokepoint flags.

Click any node to trace its full chain in either direction. Search by name,
location, or owner. Filter by sector. **🔒 marks single-source / no-viable-
alternative dependencies** — each comes with a workaround note explaining
how the world routes around the chokepoint in practice (Boeing's titanium
post-VSMPO, Lynas + MP for non-Chinese rare earths, Catalent for Novo's
GLP-1 capacity, etc.).

## Live demo

**https://hw6476ym.github.io/Top100_completesupplychain/**

(Or open `index.html` directly in any modern browser.)

## Built with

Single-file HTML + [D3.js](https://d3js.org/) (loaded from CDN). ~700 nodes,
~1,500 edges. No build step. ~160 KB.

## Data sources

Public-domain figures compiled from USGS, IEA, BloombergNEF, S&amp;P
Commodity Insights, company filings (10-K / annual reports), and trade press
through 2025. Capacities and ownership reflect the most recent disclosed
figures available. Supply networks shift quarterly — treat as a teaching
map, not a procurement document.
