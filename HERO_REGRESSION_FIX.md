# Homepage hero regression guard

The live homepage regressed when the deploy source was rebuilt from a stale static-site generator/repository snapshot that still emitted the older `Deploy your AI sales fleet` hero and static `Fleet + Consulting` card. The approved homepage hero is the `A-Gent, always-on SDR.` version with the Book Demo lead form and looping AI SDR product-motion card.

The corrected artifact is now present in both `index.html` and `dashboard/index.html`, with the shared CSS, brand assets, Blog route, Platform route, and `/platform/signal-engine/` mirrored under both root and `dashboard/`. This is intentional compatibility hardening because the a-gent.co Netlify project has previously served from `dashboard/` despite root-publish deploys. If a future repository-triggered deploy or Platform update uses either publish root, it will still serve the approved homepage, animation stylesheet, Blog, and Signal Engine pages.
