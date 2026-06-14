# Homepage hero regression guard

The live homepage regressed when the static deploy artifact was rebuilt from a generator/source snapshot that still emitted the older `Deploy your AI sales fleet` hero and static `Fleet + Consulting` card. The approved homepage hero is the `A-Gent, always-on SDR.` version with the Book Demo lead form and looping AI SDR product-motion card.

This repository now mirrors the corrected deploy artifact in both `index.html` and `dashboard/index.html`, with Netlify publishing from the repository root (`publish = "."`). This prevents future repository-triggered deploys or Platform updates from silently reverting the homepage to the stale hero or serving the dashboard mirror instead of the root homepage. Blog and Platform routes, including `/platform/signal-engine/`, were preserved additively.
