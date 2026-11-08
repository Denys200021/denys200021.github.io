#!/usr/bin/env python3
"""Real-browser checks for recruiter mode, routing, mobile fit, and accessibility basics."""
from __future__ import annotations
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:4174/'


def wait_for_server(process: subprocess.Popen) -> None:
    deadline = time.time() + 35
    last_error = None
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f'Vite preview exited early with status {process.returncode}')
        try:
            with urllib.request.urlopen(BASE, timeout=2) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
        time.sleep(.25)
    raise RuntimeError(f'Vite preview did not become available: {last_error}')


def main() -> None:
    npm = shutil.which('npm') or 'npm'
    server = subprocess.Popen(
        [npm, 'run', 'preview', '--', '--host', '127.0.0.1', '--port', '4174', '--strictPort'],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
    )
    results: list[tuple[bool, str]] = []
    errors: list[str] = []

    def check(condition: bool, label: str) -> None:
        results.append((bool(condition), label))
        print(f"{'PASS' if condition else 'FAIL'} {label}")

    try:
        wait_for_server(server)
        with sync_playwright() as p:
            launch = {'headless': True, 'args': ['--no-sandbox', '--disable-dev-shm-usage']}
            if os.environ.get('CHROMIUM_PATH'):
                launch['executable_path'] = os.environ['CHROMIUM_PATH']
            browser = p.chromium.launch(**launch)
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            page.on('pageerror', lambda error: errors.append(str(error)))
            response = page.goto(BASE + '?view=recruiter', wait_until='domcontentloaded', timeout=30000)
            page.get_by_role('heading', name='King Art D. Pacumberto.', level=1).wait_for(timeout=15000)
            check(response is not None and response.status == 200, 'Recruiter view loads directly from a shareable query URL')
            check('Recruiter Profile' in page.title(), 'Recruiter view receives a focused browser title')
            check(page.get_by_role('navigation', name='Recruiter profile sections').count() == 1, 'Recruiter navigation has an accessible name')
            check(page.get_by_role('heading', name='Projects that show how I build.').is_visible(), 'Selected project case studies are visible')
            check(page.locator('.recruiter-project-card').count() == 3, 'Exactly three featured technical projects are presented')
            check(page.locator('.recruiter-project-card a[href^="https://github.com/"]').count() >= 3, 'Each featured technical project has a repository link')
            check(page.get_by_role('link', name='Download CV · PDF').count() == 2, 'Public-safe PDF CV is accessible in profile header and contact area')
            check(page.locator('a[href*="Resume.pdf"]').count() == 0, 'Recruiter profile does not expose the original phone-bearing resume')
            check(page.locator('.recruiter-portrait img').evaluate('(img) => img.complete && img.naturalWidth > 0'), 'Recruiter profile portrait loads successfully from the optimized responsive asset set')

            access = page.evaluate("""() => {
              const named = (element) => Boolean((element.getAttribute('aria-label') || element.getAttribute('title') || element.innerText || '').trim());
              const unnamedButtons = [...document.querySelectorAll('button')].filter((el) => !named(el));
              const unnamedLinks = [...document.querySelectorAll('a')].filter((el) => !named(el));
              const missingImageAlt = [...document.querySelectorAll('img')].filter((el) => !el.hasAttribute('alt'));
              const badExternal = [...document.querySelectorAll('a[target="_blank"]')].filter((el) => !el.rel.includes('noopener'));
              const landmarks = {main: document.querySelectorAll('main').length, nav: document.querySelectorAll('nav[aria-label]').length};
              return {unnamedButtons: unnamedButtons.length, unnamedLinks: unnamedLinks.length, missingImageAlt: missingImageAlt.length, badExternal: badExternal.length, landmarks};
            }""")
            check(access['unnamedButtons'] == 0, f"Recruiter controls have accessible names ({access['unnamedButtons']} unnamed)")
            check(access['unnamedLinks'] == 0, f"Recruiter links have accessible names ({access['unnamedLinks']} unnamed)")
            check(access['missingImageAlt'] == 0, 'Recruiter view contains no images without alt attributes')
            check(access['badExternal'] == 0, 'All new-tab external links use opener isolation')
            check(access['landmarks']['main'] == 1 and access['landmarks']['nav'] >= 1, 'Recruiter page has a single main landmark and named navigation')

            page.get_by_role('button', name='Read case study').first.click()
            page.get_by_role('dialog').wait_for(timeout=5000)
            check('project=' in page.url and 'view=recruiter' not in page.url, 'Case study action switches into the full project dialog with a shareable URL')
            page.get_by_role('button', name='Back to portfolio').click()
            page.get_by_role('link', name='Recruiter view').click()
            page.get_by_role('heading', name='King Art D. Pacumberto.', level=1).wait_for(timeout=8000)
            page.get_by_role('button', name='Full portfolio').click()
            page.get_by_role('heading', name='From a question').wait_for(timeout=10000)
            page.locator('#main-content').wait_for(state='visible', timeout=10000)
            page.locator('.site-header').wait_for(state='visible', timeout=10000)
            check('view=recruiter' not in page.url, 'Full-portfolio control exits recruiter view and clears its URL mode')
            check(page.evaluate('window.scrollY <= 2'), 'Explicit view switching starts the newly mounted layout at the top of the document')
            check(page.locator('#main-content').is_visible() and page.locator('#projects').is_visible(), 'Returning to full portfolio remounts the main content and project sections without a refresh')
            check(page.locator('#lab').count() == 1 and page.locator('#skills-map').count() == 1 and page.locator('#network-lab').count() == 1, 'All major interactive lab sections return after recruiter-to-full switching')
            lifecycle = page.evaluate("""() => ({
              revealReady: document.documentElement.dataset.revealReady === 'true',
              motionOff: document.documentElement.dataset.motion === 'off',
              revealTargets: document.querySelectorAll('#main-content [data-reveal]').length,
              headerConnected: Boolean(document.querySelector('.site-header')?.isConnected),
              mastheadProgress: Boolean(document.querySelector('.scroll-progress'))
            })""")
            check(lifecycle['revealReady'] or lifecycle['motionOff'], 'Full-view reveal runtime is reinitialized or deliberately disabled by reduced motion')
            check(lifecycle['revealTargets'] >= 20 and lifecycle['headerConnected'] and lifecycle['mastheadProgress'], 'Full-view reveal, header, and progress targets are connected to the newly mounted DOM')
            page.evaluate("window.scrollTo(0, document.querySelector('#lab').offsetTop + 1200)")
            page.wait_for_timeout(120)
            check(page.locator('.quick-navigator').count() == 1, 'Quick navigator remounts and responds to scrolling after returning to full view')
            header_hidden = page.locator('.site-header').evaluate("el => el.classList.contains('header-hidden')")
            check(header_hidden, 'Rebound masthead controller hides the header on downward scroll')
            page.evaluate('window.scrollTo(0, 0)')
            page.wait_for_timeout(120)
            header_visible = not page.locator('.site-header').evaluate("el => el.classList.contains('header-hidden')")
            check(header_visible, 'Rebound masthead controller reveals the header on upward scroll')
            page.go_back()
            page.get_by_role('heading', name='King Art D. Pacumberto.', level=1).wait_for(timeout=10000)
            check('view=recruiter' in page.url and page.locator('.recruiter-view').is_visible(), 'Browser history restores the shareable recruiter view without stale full-view nodes')
            page.go_forward()
            page.get_by_role('heading', name='From a question').wait_for(timeout=10000)
            check('view=recruiter' not in page.url and page.locator('#main-content').is_visible(), 'Browser forward restores the full portfolio and its content runtime')
            # Repeat both transitions to catch duplicate observers or one-way cleanup.
            for iteration in range(2):
                page.get_by_role('link', name='Recruiter view').click()
                page.get_by_role('heading', name='King Art D. Pacumberto.', level=1).wait_for(timeout=8000)
                page.get_by_role('button', name='Full portfolio').click()
                page.get_by_role('heading', name='From a question').wait_for(timeout=10000)
                check(page.locator('#main-content').is_visible() and page.locator('.site-header').is_visible(), f'Repeated recruiter/full transition {iteration + 1} restores the complete portfolio')

            print_display = page.locator('.recruiter-actions').evaluate("el => getComputedStyle(el).display")
            page.emulate_media(media='print')
            print_hidden = page.locator('.recruiter-actions').evaluate("el => getComputedStyle(el).display") == 'none'
            page.emulate_media(media='screen')
            check(print_hidden and print_display != 'none', 'Print stylesheet removes on-screen navigation controls')

            for width in [320, 360, 390, 768, 1024, 1440]:
                page.set_viewport_size({'width': width, 'height': 900})
                page.wait_for_timeout(80)
                overflow = page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1')
                check(not overflow, f'{width}px viewport has no horizontal overflow')

            page.keyboard.press('Tab')
            focused = page.evaluate("document.activeElement && (document.activeElement.tagName === 'A' || document.activeElement.tagName === 'BUTTON')")
            check(focused, 'Keyboard navigation reaches a visible interactive control')
            check(not errors, 'Desktop recruiter route has no uncaught browser exceptions')

            mobile = browser.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
            mobile.on('pageerror', lambda error: errors.append(str(error)))
            mobile.goto(BASE + '?view=recruiter', wait_until='domcontentloaded', timeout=30000)
            mobile.get_by_role('heading', name='King Art D. Pacumberto.', level=1).wait_for(timeout=15000)
            check(mobile.get_by_role('link', name='Download CV · PDF').first.is_visible(), 'Touch layout keeps the PDF CV action visible')
            check(not mobile.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1'), '390px touch viewport has no horizontal overflow')
            mobile.get_by_role('link', name='Experience').tap()
            check(mobile.evaluate("location.hash === '#recruiter-experience'"), 'Touch section navigation reaches the experience record')
            check(not errors, 'Touch recruiter route has no uncaught browser exceptions')
            browser.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

    passed = sum(1 for ok, _ in results if ok)
    failed = [label for ok, label in results if not ok]
    print(f'\nRecruiter browser QA: {passed}/{len(results)} checks passed.')
    if failed:
        print('Failures:')
        for label in failed:
            print(f' - {label}')
        raise SystemExit(1)


if __name__ == '__main__':
    main()
