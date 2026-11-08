> **Historical release record.** This report documents an earlier incremental build and is retained for traceability. Its test results and file inventory are not the status of the current release. See [`FULL-SYSTEM-AUDIT-2026-11-09.md`](../../FULL-SYSTEM-AUDIT-2026-11-09.md) for the current audit.

---

# Adaptive Portfolio Update & QA — 2026-11-08

## What changed

### Adaptive behavior

- CSS remains the source of truth for layout; the site does not alter browser zoom.
- Fluid type and spacing, breakpoint rules, component container queries, orientation rules, `svh`/`dvh`, and safe-area viewport support adapt the page to the effective CSS viewport.
- `src/adaptive.ts` profiles the viewport, orientation, pointer type, visual viewport scale, DPR, reduced-motion preference, Save-Data, device-memory, and CPU hints.
- Optional Canvas quality moves among economy, balanced, and full profiles. It is capped at 42 desktop particles / 18 coarse-pointer particles, with a 24 FPS ceiling and bounded DPR. Save-Data and reduced-motion disable the particle workload.
- Adaptive profile notifications are keyed only to meaningful visual-effect changes. One-pixel resize events are handled by CSS/ResizeObserver without rescheduling the full optional effect workload.
- If browser hints or observers are unavailable, the profiler falls back to `maxTouchPoints`, window events, and conservative defaults.

### Fallbacks and resilience

- The Canvas field hides itself if 2D context creation fails; the CSS-built background remains.
- Motion-heavy zones pause when off-screen and when the document is hidden.
- The operating system's reduced-motion preference takes priority over a previously saved site preference.
- Native `details` / `summary` keeps expandable content usable without custom animation JavaScript and remains keyboard-operable.
- Remote font loading uses `display=swap` and system font stacks.
- The initial HTML includes a boot state and a no-JavaScript fallback. A React error boundary retains GitHub, email, and public CV routes if the main app fails.
- Optional interface sounds use Web Audio only, require visitor opt-in, and ship no audio files.

### Maintenance and backups

- `npm run check`: source/content/config preflight.
- `npm run test:adaptive`: dependency-free adaptive-profile tests.
- `npm run backup`: local source/resource snapshot with a SHA-256 manifest and immediate verification.
- `npm run backup:verify`: verifies the most recent snapshot.
- `npm run verify`: runs the preflight, adaptive tests, strict project typecheck, and production build when dependencies are installed.
- Backup retention is limited to the five newest snapshots under `.portfolio-backups/`; the directory is ignored by Git and is not a cloud backup.

## Visual and responsive QA

### Browser fixture checks passed

The Chromium fixture used the current portfolio stylesheet and representative page markup. It is a CSS/interaction fixture, not the complete React application.

- Viewports: 320×700, 360×800, 390×844, 430×932, 667×375 landscape, 768×1024, 900×900, 1024×768, 1365×900, and 1920×1080.
- At every tested size, `documentElement.scrollWidth` and `body.scrollWidth` matched the viewport width; no horizontal overflow was detected.
- Native disclosure controls opened and closed with both Space and Enter. The tested responsive widths also represent narrow effective CSS viewports produced by browser zoom; the code does not override zoom.
- With reduced motion emulated, project-card opacity was `1`, transform was `none`, and transition/animation durations resolved to `0s`.
- Theme tokens and primary colors were read from computed Chromium styles.
- No browser page errors were observed in the fixture.
- Desktop dark and mobile light screenshots were captured and reviewed.

### Contrast samples

Ratios are computed from the actual final theme tokens (rounded to two decimals):

| Pair | Contrast |
|---|---:|
| Dark primary text `#e8eee8` on `#101619` | 15.49:1 |
| Dark accent `#ff765e` on `#101619` | 6.96:1 |
| Dark button text `#13190b` on `#ff765e` | 6.83:1 |
| Light primary text `#39443f` on `#f3efe5` | 8.82:1 |
| Light muted text `#5e6a64` on `#f3efe5` | 4.91:1 |
| Light secondary muted `#626e67` on `#f3efe5` | 4.64:1 |
| Light accent `#a34b36` on `#f3efe5` | 5.06:1 |
| Light button text `#fffaf0` on `#a34b36` | 5.58:1 |

## Source and automated checks passed

- Static portfolio preflight: passed, including required files, JSON, content claims, unique project IDs, recognized project-illustration fallbacks, public CV path, GitHub Pages workflow version, private-CV exclusion, and port isolation.
- Adaptive unit/smoke tests: passed for desktop, touch, Save-Data, reduced-motion, zoomed visual viewport, DPR cap, invalid browser hints, and resize-work coalescing.
- Strict source-level TypeScript check: passed with the environment's global TypeScript 5.8.3 compiler and temporary React/Vite ambient declarations, including `noUnusedLocals`, `noUnusedParameters`, and `noFallthroughCasesInSwitch`. This is not a substitute for the project's declared dependency-backed TypeScript 7 check.
- CSS: 108,753 bytes; 718 top-level rules; zero tinycss2 stylesheet/declaration parse errors after the final palette and adaptive updates. The application source footprint is 184.1 KB across seven core files, before production minification.
- HTML structure, inline bootstrap JavaScript syntax, package JSON, GitHub Actions YAML, SVG XML, and local TypeScript/TSX import-path checks: passed.
- Local backup: most recent snapshot contained 29 files (about 325.4 KB) and all file lengths/SHA-256 checksums verified. The final package includes the backup tooling, not the ignored local backup directory.
- CVs: both two-page DOCX files rendered to PNG and visually inspected page by page; both PDFs rendered and inspected. The public CV omits the phone number; private CV retains it. The portfolio package includes only the public PDF.

## Not verified / not deployed

- `node_modules` and `package-lock.json` are not present in this working copy. Dependency installation previously failed with `EAI_AGAIN` while reaching `registry.npmjs.org`; an offline lockfile attempt also failed because the package metadata was not cached (`ENOTCACHED`).
- Therefore, the full dependency-backed `npm run typecheck`, Vite production build, and complete live React browser test remain unverified. The included GitHub Actions workflow runs these checks after dependencies can be installed.
- The package has not been pushed to GitHub and GitHub Pages has not been deployed. Vite's development/preview ports remain 5174/4174, and the Pages base remains `/` for the root `Legioniz.github.io` repository.
- Permanent visitor analytics, inquiry storage, comments, moderation, and owner-only admin controls are not enabled. GitHub Pages is static hosting; those features still require the configured secure backend described in `BACKEND-SETUP.md`.

## Content accuracy notes

- Education and six work entries follow the latest uploaded resume. No unconfirmed honors or dates are added.
- PUP QC Hackathon is listed once. Its date, category, and exact individual role remain unspecified.
- SSG/SSLG, Glee Club bass guitar/Gala Night, Technology Club/Technical Team leadership and livestream operations, Maths/Science Club officer roles, badminton, and CASAP QC volunteer photography responsibilities are from the owner's direct descriptions; dates were not invented.
- Java and SQL reflect previously supplied skill updates. TypeScript/React are shown as LensLab project technologies, not as self-rated core-skill proficiency. The skills summary was narrowed to avoid treating project-only technologies as verified proficiency.
- Smart Electrical Monitoring is explicitly a local synthetic-data demonstration, not a live utility or smart-meter connection.


## 2026-11-08 / Direction-aware header and bidirectional reveal refinement

- Implemented a smart floating masthead: downward scroll hides it after 18 CSS pixels of accumulated direction travel; upward scroll reveals it after 8 CSS pixels. It always shows near the top of the document, remains present when mobile navigation is open, and recovers on keyboard focus. Scroll handling is passive and coalesced through `requestAnimationFrame`.
- Replaced one-time reveal behavior with bidirectional `IntersectionObserver` state toggling. Elements now ease in as they enter the reading region, ease out as they leave, and repeat the entrance when the visitor scrolls upward. The observer uses a central reading area (`rootMargin: -6% 0px -7% 0px`) to reduce edge flicker.
- Added restrained reveal variants for major content groups and adaptive distances/durations for full, balanced, economy, and coarse-pointer profiles. Reduced-motion and manual motion-off settings keep all content visible and disable transitions.
- Rebuilt the header monogram markup as one unbreakable inline-flex `KA` unit; the letters now share a visible foreground color against the accent tile. Added `aria-expanded` and `aria-controls` to the mobile menu button.
- Chromium/Playwright fixture checks passed: masthead visible at top, hidden after downward scroll, shown after upward scroll, keyboard focus recovery, mobile menu pinning, `KA` one-line lockup and no page overflow at 320/360/390/430/768/1024/1440 px, reveal enter/exit/re-enter, and reduced-motion fallback.
- TypeScript source check passed using a temporary React ambient declaration because dependencies are not installed. Adaptive smoke tests passed. CSS parser found zero syntax errors across 827 top-level rules.
- Full React/Vite production build remains unverified because package dependencies are not installed in this environment.
