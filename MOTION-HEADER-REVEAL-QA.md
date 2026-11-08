# Motion, Masthead & Disclosure Runtime — QA

Date: 2026-11-08

## Root causes fixed

1. The play-shaped motion toggle had been disabled when the operating system requested reduced motion. That prevented a visitor from explicitly opting into site animation. The control is now always operable; by default the site follows the OS preference, but a deliberate click can enable or pause motion for this site.
2. Earlier local-storage motion preference keys could preserve stale pause state across releases. The current release reads/writes `legion-portfolio-motion-v4`; v1-v3 keys are ignored. `system` means follow the OS, `on` means explicit site-level opt-in, and `off` means manual pause.
3. Section reveals were previously too coupled to the masthead scroll pipeline. The reveal controller now uses its own `IntersectionObserver`; the masthead has a separate, frame-batched controller.
4. The disclosure panel used a plain `0fr` grid track. Grid's automatic minimum can retain the min-content size, leaving the panel apparently partly open. It now animates between `minmax(0, 0fr)` and `minmax(0, 1fr)` so the closed track can truly reach zero.
5. `.achievement-row div` was too broad and could override the disclosure panel's grid layout. The rule now targets `.achievement-detail` only.

## Runtime behavior

- `src/reveal.ts` uses one `IntersectionObserver` for `[data-reveal]` targets. Entering the reading area adds `.is-visible`; leaving removes it; re-entry animates again.
- A `MutationObserver` registers newly filtered project cards and removes detached elements from tracking.
- The reveal script has a bounded timeout fallback. If observer callbacks fail, content is restored to its visible state rather than remaining hidden.
- `src/masthead.ts` hides the header after a small accumulated downward movement and shows it after upward movement. It protects the header at the top, while mobile navigation is open, while keyboard focus is inside the header, and whenever motion is paused.
- The motion control in `src/App.tsx` is not disabled under system reduced-motion. With the OS preference active, it displays the play icon and explains that clicking enables motion for this site.
- The early `index.html` bootstrap applies theme and motion preferences before React mounts.
- Skills, work history, extracurricular activities, education history, achievements, and project notes use native disclosure semantics. The shared panel is keyboard-operable through `<summary>` and animates height and opacity using zero-minimum grid tracks.

## Automated verification

Commands executed:

- `npm run test:adaptive` — passed.
- `npm run check` — passed; source/content/configuration preflight and required assets verified.
- `npm run test:motion` — passed; exact production reveal/masthead modules and the actual project CSS were exercised in Chromium.
- `npm run test:interactions` — passed; 29/29 interaction assertions.
- Standalone TypeScript compilation of `adaptive.ts`, `reveal.ts`, `masthead.ts`, `sound.ts`, `config.ts`, and `data.ts` — passed.
- `tinycss2` parse of the main stylesheet — passed with no parse errors.
- `npm run typecheck` — blocked because React, React DOM, their type declarations, Vite, and the React Vite plugin are not installed in this runtime. The npm registry previously returned DNS error `EAI_AGAIN`; the full dependency-backed React typecheck and production build are therefore not claimed as passed.

### Browser assertions

- Section reveal starts hidden, enters, exits, and re-enters with 720ms opacity/transform transitions.
- Newly inserted project cards are registered.
- Skill, academic-history, and achievement disclosure rows each open, finish expanding, close with Enter, and reach a fully collapsed zero-height/zero-opacity state.
- System reduced motion starts the site static; explicit v4 site opt-in re-enables transitions without changing the OS setting.
- The header's computed transform moves above the viewport on downward scroll and returns on upward scroll.
- Header top guard, open-menu guard, motion-off guard, and mobile horizontal centering pass.
- `KA` remains one line without document overflow at 320, 360, 390, 430, 768, 1024, and 1440 CSS pixels.
- No browser page errors were emitted by the motion test.

## Documents

- `public/King-Art-Pacumberto-Resume.pdf`: exact owner-supplied original PDF; it contains the phone number and is public when deployed.
- `public/King-Art-Pacumberto-CV.pdf`: redesigned public-safe PDF.

## Not verified

The full React/Vite production build could not run without the missing dependencies. Browser QA loads the exact production reveal/masthead TypeScript modules and CSS into Chromium with representative markup; it does not claim that a complete React runtime or deployed GitHub Pages site has been built. The update has not been pushed to GitHub or deployed.
