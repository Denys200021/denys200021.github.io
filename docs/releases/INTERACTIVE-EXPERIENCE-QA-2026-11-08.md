> **Historical release record.** This report documents an earlier incremental build and is retained for traceability. Its test results and file inventory are not the status of the current release. See [`FULL-SYSTEM-AUDIT-2026-11-09.md`](../../FULL-SYSTEM-AUDIT-2026-11-09.md) for the current audit.

---

# LEGIONIZ Portfolio — Interactive Experience QA

**Release date:** 8 November 2026  
**Scope:** project hover previews and project introductions, delegated interface sounds, sound preference behavior, responsive/touch interaction, existing scroll-reveal and masthead motion.

## Implemented

### Project launch cards

- Fine-pointer desktop hover lifts each project card and slides a quick-view panel in from the right.
- The quick-view panel previews the project headline, contribution/role, and technology tags.
- Clicking anywhere on a card opens the full project introduction.
- Enter and Space also open the introduction when the card is keyboard-focused.
- Touch/coarse-pointer layouts omit the hover-only panel and open the same introduction on tap.
- The introduction includes project overview, role/contribution, status, highlights, technology, expandable scope notes, and the repository link when available.
- The modal supports Escape, backdrop close, focus containment, and focus restoration.

### Interaction sounds

A single delegated Web Audio manager handles dynamic and static controls. No sound files or audio framework are downloaded.

| Interaction | Sound identity |
|---|---|
| Header/footer navigation hover | Bright two-note ping |
| Content link hover | Soft descending pair |
| Project card hover | Warm two-note rising interval |
| Standard control hover | Short triangular tick |
| Disclosure hover | Soft paired note |
| Keyboard focus | Single focus marker |
| Text input change | Quiet low tick |
| Select change | Two-note selection cue |
| Form submit | Three-note confirmation |
| Button action | Context-aware click/toggle/navigation cue |
| Project open / close | Rising / descending three-note chord |
| Filter / download / copy | Dedicated action patterns |

Sound is enabled by default for new visitors. A real user action is required before browser audio can play. The first hover before any click, tap, or keyboard interaction may therefore be silent; after a trusted gesture, hover cues become available. The speaker control persists the visitor's preference. When muting, one final toggle cue can play; subsequent actions stay silent until re-enabled.

### Existing motion system retained

- Direction-aware masthead hide/reveal behavior.
- Bidirectional section reveal (enter, exit, re-enter).
- Adaptive quality levels and reduced-motion/data-saver fallbacks.
- Off-screen decorative motion pauses.
- Desktop right-side project peek, touch tap-to-open fallback.

## Verification

| Check | Result |
|---|---|
| Static source/content preflight | **126 checks passed** |
| Adaptive profile smoke tests | **Passed** |
| Chromium interaction browser tests | **29 / 29 passed** |
| Chromium section reveal and masthead motion tests | **Passed** |
| CSS syntax parse | **885 top-level rules, 0 parse errors** |
| Application TypeScript source check | **Passed with temporary React declarations** |
| Original resume PDF SHA-256 | **Matches uploaded source** |
| Public CV PDF link | **Resolves to bundled PDF** |
| Release ZIP integrity | **Passed** |

The browser interaction suite compiles and loads the actual `src/sound.ts` module and the shipped `src/styles.css`, then exercises project-card markup, modal behavior, links, buttons, disclosures, form controls, mute behavior, and touch fallback in Chromium. The motion suite compiles the actual reveal and masthead controllers and verifies computed visibility/transform behavior in its browser fixture.

The browser fixtures are targeted integration tests; they are not a full React/Vite production deployment. The full dependency-backed React typecheck and Vite build have **not** been verified in this environment because `node_modules` is absent and package-registry DNS has previously failed (`EAI_AGAIN`). Do not treat the ZIP as a deployed site.

## Runtime notes

- Development port: `5174`.
- Preview port: `4174`.
- `npm run test:interactions` runs the optional Chromium/Playwright interaction suite (requires Python Playwright, global `tsc`, and Chromium).
- `npm run check`, `npm run test:adaptive`, and `python tests/portfolio-motion-qa.py` run the static and motion checks.
- No `node_modules/`, `dist/`, private CV, or local backup snapshots are included in the release archive.
- The exact original resume PDF is bundled as requested. It contains the phone number printed on the original document; publishing it makes that number publicly downloadable. The redesigned public-safe CV PDF omits the phone number. The DOCX download was removed in the November 9 PDF-only update.

