# Recruiter View

The portfolio includes a focused, shareable recruiter experience at:

`https://legioniz.github.io/?view=recruiter`

It is intentionally a concise reading mode, not a second manually maintained CV. Project summaries, skills, employment history, education, achievements, and extracurricular information are sourced from `src/data.ts` and `src/config.ts` so the normal portfolio and recruiter experience remain aligned.

## What it includes

- Professional introduction, optimized responsive portrait, current PUP BSIT study, location, and availability note.
- A single public-safe PDF CV download. The original resume PDF—which contains the phone number printed in the supplied file—is not exposed in this mode.
- Three featured technical projects with repository links and hand-off into the full project case-study dialog.
- Evidence-led skills grouped by practice area, without invented proficiency percentages.
- Relevant technical support and teaching experience first, with remaining employment history disclosed below.
- Education, selected recognition, leadership, and collaboration experience.
- Email, GitHub, and LinkedIn contact destinations.
- Responsive layout, keyboard skip link, focusable page heading, native disclosures, and a print stylesheet.

The mode is controlled by the `view=recruiter` query parameter. It supports direct entry, refresh, browser history, and return to the full portfolio. The app updates browser title, description, Open Graph, and Twitter card metadata when switching between the two reading modes. The page component is dynamically imported so the recruiter-only markup and code are not required in the initial full-portfolio bundle.

## Content maintenance

Edit the underlying arrays in `src/data.ts` and the public profile fields in `src/config.ts`. Do not add unverified dates, metrics, responsibilities, qualifications, or claims. The TIMO result links to a public result where available; other achievements remain owner-supplied unless a source is provided.

The public-safe CV is `public/King-Art-Pacumberto-CV.pdf`. Keep phone-bearing or otherwise private versions out of `public/`.


## Presentation and motion refinement

Recruiter View shares the full portfolio's charcoal / warm-ivory / coral tokens and its typography roles, while using a tighter editorial layout, clearer section labels, more prominent project artwork, balanced content widths, and stronger contact / PDF action hierarchy. Experience is arranged as a compact timeline with an in-view progress rail. Experience cards, education entries, award records, and leadership items use short staged reveals, with the first viewport visible before the observer initializes. Reduced-motion and observer fallbacks keep every item readable. Project links continue to open the shared full case-study dialog, rather than a duplicate recruiter-only detail page.
