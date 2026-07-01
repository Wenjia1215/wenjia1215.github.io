(() => {
  'use strict';

  const SITE = {
    name: 'Wenjia Wang',
    tagline: 'Research & Teaching',
    email: 'wenjiabusiness@gmail.com',
    location: 'Miami, FL',
    modes: [
      { page: 'teaching', label: 'Teaching', href: 'index.html', activeClass: 'teaching' },
      { page: 'research', label: 'Research', href: 'research.html', activeClass: 'research' },
    ],
    nav: [
      { page: 'publications', label: 'Publications', href: 'publications.html' },
      { label: 'CV', href: 'assets/files/wenjia-wang-cv.pdf' },
    ],
    socials: [
      { label: 'GitHub', badge: 'GH', href: 'https://github.com/Wenjia1215' },
      { label: 'LinkedIn', badge: 'in', href: 'https://www.linkedin.com/in/wenjiawang-page/' },
      { label: 'Scholar', badge: 'GS', href: 'https://scholar.google.com/citations?user=Zl-yM-kAAAAJ&hl=en&oi=ao' },
      { label: 'YouTube', badge: 'YT', href: 'https://www.youtube.com/@WenjiaCybersecurity' },
    ],
  };

  function el(tag, options = {}, children = []) {
    const node = document.createElement(tag);
    Object.entries(options).forEach(([key, value]) => {
      if (key === 'className') node.className = value;
      else if (key === 'text') node.textContent = value;
      else node.setAttribute(key, value);
    });
    children.forEach((child) => node.append(child));
    return node;
  }

  function currentPage() {
    return document.body.dataset.page || 'teaching';
  }

  function markActive(link, isActive, extraClass = '') {
    if (!isActive) return;
    link.className = ['active', extraClass].filter(Boolean).join(' ');
    link.setAttribute('aria-current', 'page');
  }

  function makeModeLink(item, page) {
    const link = el('a', { href: item.href, text: item.label });
    markActive(link, item.page === page, item.activeClass);
    return link;
  }

  function makeNavLink(item, page) {
    const link = el('a', { href: item.href, text: item.label });
    markActive(link, item.page === page);
    return link;
  }

  function makeSocialLink(item) {
    const badge = el('span', { className: 'social-badge', text: item.badge });
    const label = el('span', { className: 'social-label', text: item.label });
    return el('a', {
      className: 'header-social',
      href: item.href,
      target: '_blank',
      rel: 'noopener noreferrer',
      'aria-label': item.label,
    }, [badge, label]);
  }

  function makeHeader(page) {
    const skipLink = el('a', { className: 'skip-link', href: '#main-content', text: 'Skip to content' });

    const tagline = el('span', { text: SITE.tagline });
    const brand = el('a', { className: 'brand', href: 'index.html' }, [SITE.name, tagline]);

    const modeNav = el('nav', { className: 'mode-pills', 'aria-label': 'Primary pages' },
      SITE.modes.map((item) => makeModeLink(item, page)));

    const pageNav = el('nav', { className: 'nav-links', 'aria-label': 'Secondary pages' },
      SITE.nav.map((item) => makeNavLink(item, page)));

    const socialNav = el('nav', { className: 'header-socials', 'aria-label': 'Profile links' },
      SITE.socials.map(makeSocialLink));

    const header = el('header', { className: 'site-header mode-header' }, [brand, modeNav, pageNav, socialNav]);
    return [skipLink, header];
  }

  function makeFooter() {
    const year = new Date().getFullYear();
    const text = el('span', { text: `© ${year} ${SITE.name} · ${SITE.location}` });
    const icon = el('img', { src: 'assets/icons/email.svg', alt: '', 'aria-hidden': 'true' });
    const email = el('a', { className: 'footer-link email-button', href: `mailto:${SITE.email}` }, [icon, 'Send Email']);
    const inner = el('div', { className: 'footer-inner footer-compact' }, [text, email]);
    return el('footer', { className: 'footer' }, [inner]);
  }

  function mountSiteChrome() {
    document.body.prepend(...makeHeader(currentPage()));
    document.body.append(makeFooter());
  }

  mountSiteChrome();
})();
