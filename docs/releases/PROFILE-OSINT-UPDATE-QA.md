> **Historical release record.** This report documents an earlier incremental build and is retained for traceability. Its test results and file inventory are not the status of the current release. See [`FULL-SYSTEM-AUDIT-2026-11-09.md`](../../FULL-SYSTEM-AUDIT-2026-11-09.md) for the current audit.

---

# Portfolio Profile & OSINT Update — QA Report

**Date:** 8 November 2026  
**Project:** Legioniz Professional Portfolio  
**Deployment target:** `Legioniz.github.io` (GitHub Pages)

## Delivered changes

- Added the supplied graduation portrait to the profile/about section. The image is a still editorial portrait, not a moving hero background, so it gives the page a human focal point without competing with the portfolio's geometric diagrams or project visuals.
- Generated responsive WebP variants (480, 800, and 1023 px) and JPEG fallbacks at the same widths. The original 2.6 MB PNG is not included in the website package.
- Added `<picture>`, `srcset`, `sizes`, intrinsic dimensions, lazy loading, async decoding, descriptive alt text, and an initials fallback if the image cannot load.
- Added a distinct OSINT and defensive-network-practice field note to the About section.
- Added owner-reported public-source research, official-source cross-checking, preliminary legitimacy/compliance checks, Linux/Kali Linux foundations, Nmap local host/port discovery, local firewall configuration, traffic review, Medusa authorized login-audit labs, and isolated dummy-machine concepts to the skills and supporting content.
- Described data/traffic-spoofing and IP-manipulation only as concepts explored in isolated labs. The site explicitly limits practice to systems owned by the user or explicitly authorized for testing.
- Did not claim legal authority, professional penetration-testing experience, or an investigative/cybersecurity certification.
- Omitted the ambiguous tool name “Kraken” until the owner provides the exact product/project identity.
- Updated the private and public CV versions. Both remain two pages and use the portfolio's coral/ink accent palette. The public version omits the phone number; the private version retains it.
- Updated the bundled public CV PDF in `public/`.

## Image optimization

| Variant | Approximate size |
|---|---:|
| WebP 480 | 14.8 KB |
| WebP 800 | 34.1 KB |
| WebP 1023 | 51.8 KB |
| JPEG 480 | 37.9 KB |
| JPEG 800 | 95 KB |
| JPEG 1023 | 148 KB |

The browser selects the appropriate source using responsive image metadata and can fall back to JPEG if WebP is unsupported. See MDN responsive image guidance in `SOURCES.md`.

## Verification performed

- `node scripts/portfolio.mjs check`: passed; required resources, resume claims, security scope, unique project IDs, image fallbacks, public CV path, GitHub Pages workflow, and port isolation checked.
- `node --experimental-strip-types tests/adaptive-smoke.ts`: passed; desktop, touch, data-saver, reduced-motion, zoomed viewport, DPR cap, invalid-input fallback, and resize coalescing.
- CSS parsed with `tinycss2`: 795 top-level rules, 0 parse errors.
- Strict source TypeScript check using global `tsc` and temporary ambient React declarations: passed. This is a source-level check only, not a dependency-backed project typecheck.
- Chromium layout fixture using the actual portfolio stylesheet checked at 13 viewport sizes (320, 360, 390, 430, 600, 700, 701, 768, 820, 900, 1024, 1365, and 1920 px): no horizontal overflow; portrait stayed inside the viewport; the image decoded at 800 × 1203; no page errors in the fixture.
- Private and public CV DOCX files rendered through `render_docx.py`; all four page images were visually reviewed. Both CVs are 2 pages.
- PDF text checks confirmed the updated OSINT/security content. Public PDF was scanned and does not contain `+63 994 550 1424`; private PDF retains it.
- Local backup snapshot created and checksum-verified: 35 files, approximately 719.5 KB; retention cap is five snapshots.
- Release archive is separately checked with `unzip -t` before delivery.

## Not verified / limitations

- A full dependency-backed `npm run typecheck` and Vite production build could not run because `npm install` failed to resolve `registry.npmjs.org` (`EAI_AGAIN`, DNS/network error). Do not treat the successful static/source checks as a full production build.
- The site has not been pushed or deployed to GitHub Pages in this update.
- Permanent inquiries, visitor records, owner authentication, and comment moderation still require the configured Supabase backend described in `BACKEND-SETUP.md`; GitHub Pages alone cannot provide secure persistent records or an owner-only admin system.

## Outstanding owner confirmation

“Kraken” can refer to multiple unrelated tools. Provide the exact repository/product link or full name before adding it as a skill or tool to the public CV/portfolio.
