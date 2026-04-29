/**
 * Nav Enhancements — theme toggle, mobile menu, mermaid reinit on theme change.
 *
 * Coexists with course-enhancements.js (which handles Prism syntax highlighting,
 * progress bar, reading time, keyboard nav). Both files can be loaded together
 * without conflict.
 *
 * Required HTML (typically in the page's main nav block):
 *   <nav class="main-nav">
 *       <div class="nav-container">
 *           <a href="index.html" class="nav-logo">…</a>
 *           <button id="mobile-menu-toggle" class="mobile-menu-toggle" aria-expanded="false">☰</button>
 *           <div class="nav-links" id="nav-links">
 *               …links…
 *               <button id="theme-toggle" aria-label="Toggle dark/light mode">🌙</button>
 *           </div>
 *       </div>
 *   </nav>
 *
 * For Mermaid theme adaptation, the page's mermaid module script must expose
 * the imported library globally — i.e. `window.__mermaid = mermaid;` — so this
 * script can re-initialize it when the theme flips.
 */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        initThemeToggle();
        initMobileMenu();
        initAutoTOC();
    });

    /* -----------------------------------------------------------
     * Theme toggle (light/dark with localStorage persistence)
     * ----------------------------------------------------------- */

    function initThemeToggle() {
        const toggle = document.getElementById('theme-toggle');

        const saved = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = saved || (prefersDark ? 'dark' : 'light');

        applyTheme(theme);

        if (toggle) {
            toggle.addEventListener('click', function () {
                const current = document.documentElement.getAttribute('data-theme') || 'light';
                const next = current === 'light' ? 'dark' : 'light';
                applyTheme(next);
                localStorage.setItem('theme', next);
            });
        }
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);

        document.querySelectorAll('#theme-toggle').forEach(function (btn) {
            btn.textContent = theme === 'light' ? '🌙' : '☀️';
            btn.setAttribute(
                'aria-label',
                theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'
            );
        });

        reinitMermaid(theme);

        // Custom event so other scripts (or page-specific code) can react if needed
        document.dispatchEvent(new CustomEvent('themechange', { detail: { theme: theme } }));
    }

    /* -----------------------------------------------------------
     * Mermaid theme adaptation
     * ----------------------------------------------------------- */

    function reinitMermaid(theme) {
        const mermaid = window.__mermaid;
        if (!mermaid) return;  // page hasn't exposed mermaid — silently skip

        const isDark = theme === 'dark';
        const themeVariables = isDark
            ? {
                primaryColor: '#2d2d30',
                primaryTextColor: '#d4d4d4',
                primaryBorderColor: '#569cd6',
                lineColor: '#94a3b8',
                secondaryColor: '#1e1e1e',
                tertiaryColor: '#0f172a'
            }
            : {
                primaryColor: '#f0f8ff',
                primaryTextColor: '#1e293b',
                primaryBorderColor: '#3b82f6',
                lineColor: '#64748b',
                secondaryColor: '#f8fafc',
                tertiaryColor: '#f1f5f9'
            };

        try {
            mermaid.initialize({
                startOnLoad: false,
                theme: isDark ? 'dark' : 'default',
                themeVariables: themeVariables
            });

            // Reset and re-render existing diagrams
            document.querySelectorAll('.mermaid').forEach(function (el) {
                if (!el.dataset.src) {
                    el.dataset.src = el.textContent.trim();
                }
                el.removeAttribute('data-processed');
                el.innerHTML = el.dataset.src;
            });

            if (typeof mermaid.run === 'function') {
                mermaid.run();
            }
        } catch (e) {
            console.warn('Mermaid reinit failed:', e);
        }
    }

    /* -----------------------------------------------------------
     * Mobile menu (hamburger toggle)
     * ----------------------------------------------------------- */

    function initMobileMenu() {
        const btn = document.getElementById('mobile-menu-toggle');
        const navLinks = document.querySelector('.main-nav .nav-links');
        if (!btn || !navLinks) return;

        btn.addEventListener('click', function (e) {
            e.stopPropagation();
            const open = navLinks.classList.toggle('active');
            btn.setAttribute('aria-expanded', String(open));
            btn.textContent = open ? '✕' : '☰';
        });

        // Close menu when clicking outside
        document.addEventListener('click', function (e) {
            if (!btn.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
                btn.setAttribute('aria-expanded', 'false');
                btn.textContent = '☰';
            }
        });

        // Close menu on Escape
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                btn.setAttribute('aria-expanded', 'false');
                btn.textContent = '☰';
                btn.focus();
            }
        });
    }

    /* -----------------------------------------------------------
     * Auto-TOC — builds a sticky, FAB-collapsing table of contents
     *   from the page's <h2 id="…"> headings at runtime.
     *
     * Requires inject_section_ids.py to have run first so headings
     * have stable ids. Skips silently when fewer than 3 ids are
     * found (not worth a TOC for short pages).
     * ----------------------------------------------------------- */

    function initAutoTOC() {
        const main = document.querySelector('main#main-content') || document.querySelector('main') || document.body;
        if (!main) return;

        // Collect H2s with ids, in document order
        const headings = Array.from(main.querySelectorAll('h2[id]'));
        if (headings.length < 3) return;  // not enough sections to bother

        // Don't double-build (idempotent across re-inits)
        if (document.querySelector('.toc-card.auto-toc')) return;

        // ---- Build TOC structure ----
        const details = document.createElement('details');
        details.className = 'card toc-card auto-toc';
        details.open = true;

        const summary = document.createElement('summary');
        summary.setAttribute('aria-label', 'Toggle table of contents');
        summary.innerHTML =
            '<span class="toc-icon" aria-hidden="true">📑</span>' +
            '<span class="toc-label">In This Lesson</span>' +
            '<span class="toc-chevron" aria-hidden="true">▾</span>';
        details.appendChild(summary);

        const nav = document.createElement('nav');
        nav.setAttribute('aria-label', 'Table of Contents');
        const ol = document.createElement('ol');
        headings.forEach(function (h) {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#' + h.id;
            a.className = 'toc-link';
            // Use textContent to drop emoji-styled inner spans/code/etc.
            a.textContent = (h.textContent || '').trim();
            li.appendChild(a);
            ol.appendChild(li);
        });
        nav.appendChild(ol);
        details.appendChild(nav);

        // ---- Insert before the first H2 (so it appears under the lesson header) ----
        const firstH2 = main.querySelector('h2');
        if (firstH2 && firstH2.parentNode) {
            firstH2.parentNode.insertBefore(details, firstH2);
        } else {
            main.insertBefore(details, main.firstChild);
        }

        // ---- Active-section highlighting via IntersectionObserver ----
        if (!('IntersectionObserver' in window)) return;

        const links = details.querySelectorAll('.toc-link');
        const linkById = {};
        links.forEach(function (link) {
            const id = decodeURIComponent(link.getAttribute('href').slice(1));
            linkById[id] = link;
        });

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                const id = entry.target.id;
                links.forEach(function (l) { l.classList.remove('active'); });
                if (linkById[id]) linkById[id].classList.add('active');
            });
        }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });

        headings.forEach(function (h) { observer.observe(h); });

        // ---- Smooth-scroll on TOC click, accounting for sticky nav offset ----
        links.forEach(function (link) {
            link.addEventListener('click', function (e) {
                const id = decodeURIComponent(this.getAttribute('href').slice(1));
                const target = document.getElementById(id);
                if (!target) return;
                e.preventDefault();
                // Offset for sticky main-nav (~60px) + small breathing room
                const offset = 80;
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top: top, behavior: 'smooth' });
                history.pushState(null, '', '#' + id);
            });
        });
    }
})();
