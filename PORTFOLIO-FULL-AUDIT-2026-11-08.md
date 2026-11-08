> **Historical snapshot:** This November 8 audit records the earlier package state. The editable DOCX was removed in the November 9 PDF-only release; the current public package ships only the original resume PDF and public-safe CV PDF. See `PDF-ONLY-DOCUMENTS-QA-2026-11-09.md`.

# Legioniz Portfolio — Full Source, Resource & Motion Audit

**Audit date:** 2026-11-08  
**Source package:** `Legioniz_Portfolio_With_Original_Resume_2026-11-08.zip`  
**Updated release:** `Legioniz_Portfolio_Full_Code_Animation_Verified_2026-11-08.zip`

## Summary

The earlier releases had two motion-preference storage generations and a reveal controller coupled to the masthead scroll pipeline. The previous browser QA did not assert the actual masthead transform, so the header behavior was not truly being verified. This release:

- moves saved motion preference to `legion-portfolio-motion-v4`; stale v1-v3 values are ignored;
- keeps the OS `prefers-reduced-motion` choice as the highest-priority accessibility setting;
- uses `IntersectionObserver` for bidirectional section entry, exit, and re-entry;
- registers dynamically filtered project cards through `MutationObserver`;
- separates the masthead scroll behavior into `src/masthead.ts`, with a single passive listener batched through `requestAnimationFrame`;
- adds reveal targets to the expandable skill, timeline, education, award, and extracurricular records;
- preserves visible content when motion is disabled, observer APIs are missing, or the observer's initial callback is not delivered;
- updates the public CV PDF to the current public-safe export and verifies the original resume and both public CV downloads by SHA-256.

## Root causes addressed

1. **Stale saved motion state:** previous builds could retain an `off` value under older localStorage keys. The current build uses a new v3 key so an old pause setting cannot silently disable the latest animation system.
2. **Coupled reveal and header logic:** section visibility previously depended on the header scroll loop. It now has its own observer and is independent of header direction handling.
3. **Insufficient masthead verification:** previous testing only asserted that the header class changed. The new browser test verifies the computed off-screen transform on desktop and mobile.
4. **Incomplete element coverage:** the latest app adds individual reveal targets to the repeated content rows in Skills and Experience, not only the larger section cards.
5. **Stale public CV asset:** the previously bundled public CV PDF was replaced with the newest exported PDF. DOCX and original resume match their current source files.

## Validation results

| Validation | Result | Notes |
|---|---|---|
| Source/content preflight | PASS | `node scripts/portfolio.mjs check`; all required app, document, and deployment files found |
| Adaptive profile smoke tests | PASS | Desktop, touch, data-saver, reduced motion, zoomed viewport, DPR cap, invalid-input fallback, resize coalescing |
| Chromium reveal test | PASS | Real `src/reveal.ts` + stylesheet; initial off-screen state, enter, exit, re-enter, dynamic insertion, disabled-motion fallback, missing observer APIs, timeout recovery |
| Chromium masthead test | PASS | Real `src/masthead.ts`; down-scroll hides, up-scroll reveals, top guard, open-menu guard, motion-off guard, mobile-centering transform |
| Responsive KA mark | PASS | 320, 360, 390, 430, 768, 1024, 1440 CSS px; no page overflow |
| TypeScript source pass | PASS WITH STUBS | Global TypeScript 5.8.3 with temporary ambient React declarations; not a substitute for dependency-backed project typecheck |
| CSS parse | PASS | 828 top-level rules; zero top-level or nested declaration parse errors |
| SVG validation | PASS | `favicon.svg` and `og-card.svg` parse as XML |
| Relative import scan | PASS | 11 local imports resolved; zero missing paths |
| Document hashes | PASS | Exact hashes match current resume PDF and public-safe CV PDF/DOCX sources |
| Full Vite production build | NOT VERIFIED | `node_modules` is absent; npm install in this environment timed out with registry DNS error `EAI_AGAIN` |
| GitHub Pages deployment | NOT DEPLOYED | No remote push or deployment was performed |

### Browser motion results

The Chromium test measured the actual style state:

- Off-screen section: opacity 0, translated and scaled to its resting state.
- Entering the reading area: opacity transitions to 1 and transform returns to neutral.
- Leaving the area: opacity transitions back to 0.
- Scrolling back: opacity returns to 1.
- Dynamic project card insertion: registered and revealed.
- Desktop masthead: transforms vertically off-screen after deliberate downward movement, then returns after upward movement.
- Mobile masthead: hides vertically while retaining horizontal centering.
- Disabled or reduced motion: content stays visible and the masthead remains available.
- Browser page errors in the motion fixture: zero.

Run the browser check locally with Python Playwright, Chromium, and global TypeScript installed:

```bash
python tests/portfolio-motion-qa.py
```

## Public document manifest

| File in `public/` | Bytes | SHA-256 |
|---|---:|---|
| `King-Art-Pacumberto-Resume.pdf` | 358,350 | `99950a214cfa96e400802d3d2266250322ea7ded6c9cfe3ead046259913fc383` |
| `King-Art-Pacumberto-CV.pdf` | 108,420 | `dccd1565dbbc570c58533e06030474b319af3825b53bfd4b96c535f7f3c305e6` |
| `King-Art-Pacumberto-CV.docx` | 41,590 | `7797143f48627178dedd47429f4ebcee0fd9d688d2d03f248012569849570c24` |

The original resume contains the phone number printed on the supplied PDF. The public-safe PDF and Word CV omit it. The original resume remains in the `public/` directory only because the owner explicitly requested that exact PDF be downloadable.

## Dependency and build status

The package declares exact direct versions of React/React DOM 19.3.1, TypeScript 7.0.2, Vite 8.3.6, `@vitejs/plugin-react` 6.2.1, and React type packages 19.3.0. These versions are published on npm as of the audit date. The environment cannot currently resolve the npm registry, so dependencies could not be installed and the full Vite production build remains unverified.

After extracting the package on a machine with registry access:

```bash
npm install
npm run verify
```

Development server remains on `http://localhost:5174/`; preview remains on `http://localhost:4174/`. Port 5173 is untouched.

## Deployment status

This ZIP is a source update, not a live deployment. The current GitHub account listing showed six repositories and did not include a portfolio repository. The assumed repository URL `https://github.com/Legioniz/Legioniz.github.io` returned 404 during inspection. If the existing site is published from a differently named repository, that repository URL must be identified before its source can be compared or updated. Until the new source is committed and the Pages workflow completes successfully, an already-open website may continue serving an older release.

## Most useful checks if a browser still shows no movement

1. Confirm the browser is serving the updated source, not an older folder or deployed build.
2. Check the browser/OS accessibility setting for **Reduce motion**. When enabled, this site intentionally disables reveal and masthead animations and keeps content fully visible.
3. The latest build ignores stale v1/v2 site motion values. The current saved preference is `legion-portfolio-motion-v4`; system reduced motion is honored by default, while the enabled header play control lets a visitor explicitly opt into motion for this site.
4. In the site header, the motion control should show the pause symbol when decorative motion is enabled. A play symbol indicates motion is paused; under system reduced motion, the control is disabled and its tooltip explains why.
