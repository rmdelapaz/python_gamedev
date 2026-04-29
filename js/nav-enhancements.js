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
})();
