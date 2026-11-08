# Hero Visibility Fix — November 9, 2026

## Issue

With motion enabled, the main-page introduction could disappear while the same text appeared when motion was paused. The hero headline was registered with the global scroll-reveal controller and also had a separate clip-mask rule tied to `.is-visible`. When an observer entry was missed or delayed, the global `[data-reveal]` rule hid the text and the hero-specific clip mask kept the title lines clipped. The motion-off CSS explicitly restored opacity and clipping, which explains why disabling motion appeared to fix it.

## Changes

- Removed first-screen hero content from the global `IntersectionObserver` reveal system.
- Added a dedicated `data-hero-sequence` entrance sequence for the eyebrow, description, actions, and footnote.
- Added `data-hero-line` to the three headline lines, with a separate `hero-line-enter` keyframe.
- Set visible baseline styles for all hero content. The motion sequence is enhancement only; it never starts from fully hidden or fully clipped text.
- Preserved the full headline as the accessible heading label: **“From a question to working systems.”** The visual line fragments are hidden from assistive technology to prevent concatenated words.
- Added a semantic group label to the location and discipline metadata so it is not announced as one concatenated string.
- Kept the hero illustration visible independently; only its decorative motion remains viewport-observed.
- Removed obsolete reveal-dependent hero clip-mask and transition rules, and consolidated adaptive timing so Full, Balanced, and Economy profiles use the correct animation duration.
- Advanced the service-worker shell cache to `legion-portfolio-shell-v7`.
- Updated static preflight, production-source checks, and Chromium browser tests to enforce the fail-open hero behavior.

## Verification

| Check | Result |
|---|---:|
| Static source preflight | Passed |
| Feature and security checks | 59/59 |
| Production-source checks | 68/68 |
| Cross-file integrity | 24/24 |
| Chromium design and motion checks | 22/22 |
| Chromium interaction checks | 29/29 |
| Adaptive profile smoke tests | Passed |
| Python QA syntax compilation | Passed |
| TypeScript/TSX syntax transpilation | 14 files, 0 syntax diagnostics |
| CSS parser | Passed; 2,156 qualified rules |
| Manual Chromium hero preview | All three lines visible at full opacity after animation |

The Chromium design fixture explicitly leaves the global reveal-ready gate active while verifying that the hero headline and support copy remain visible. It also checks readability during animation, after animation, when motion is paused, under Economy timing, and with the operating-system reduced-motion preference.

The independent desktop/touch interaction fixture passed without JavaScript errors or failed checks.

## Scope and limitation

The browser tests used the production stylesheet and targeted browser fixtures. The complete React/Vite build and compiled-app end-to-end test were not run because `node_modules` is not present in this release workspace. The fix has not been deployed. No Lighthouse result is claimed.
