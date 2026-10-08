# Notes: Nuru Solutions — Head of Engineering & Data

source: portal
ats_optimize: true

## Positioning

Apply because the mandate is broader than the title: technology, data, product, architecture, team and CEO partnership.

Lead with:
- hands-on CTO / architect
- Product + Engineering + IT leadership at Peach
- mixed engineering/data organisation at Living Goods
- data-ingestion and distributed systems at Radio Africa
- national-scale data integrity/adjudication at GenKey
- field-data systems at MFieldwork

Do not claim:
- direct GIS or satellite-imagery delivery
- geospatial ML expertise
- model-building ownership
- AWS-specific production ownership unless separately sourced

Current ventures remain brief so they do not imply unavailability.


## Application question evidence

For questions about the most complex system taken from prototype to production, production failures, scaling, reliability or technical leadership, prefer the Radio Africa music-streaming / ingestion case study in `profile/case_studies/radio-africa-music-streaming-platform.md`.

Key arc: heterogeneous multi-provider catalogues → custom normalization / DRM / reporting requirements → first large Sony catalogue dump broke the single mainline pipeline → RabbitMQ + Kotlin/Akka asynchronous fan-out + idempotent retries + Lambda elastic capacity → team upskilling.
