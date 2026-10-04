/* ============================================================
   future.js — Comeiin Works interactive layer
   Catalogue routing, logistics carousel and WhatsApp widget.
   Scoped to avoid collisions with app.js and third-party scripts.
   ============================================================ */

(function () {
'use strict';

/* Catalogue base URL — set in base.html */
const FUTURE_CATALOGUE_URL = window.CW_CATALOGUE || '/products/';
const ABOUT_URL     = window.CW_ABOUT     || '/about/';
const PRIVACY_URL   = window.CW_PRIVACY   || '/privacy/';

/* Standard site navigation: responsive menu and accessible Industries dropdown. */
const siteHeader = document.querySelector('.site-header');
const siteNav = document.querySelector('.site-nav');
const navToggle = document.querySelector('.nav-toggle');
const industryToggle = document.querySelector('.industry-toggle');
const industryMenu = document.querySelector('.industry-menu');

function setIndustryMenu(open) {
  if (!industryToggle || !industryMenu) return;
  industryToggle.setAttribute('aria-expanded', String(open));
  industryMenu.hidden = !open;
}

function setMainNavigation(open) {
  if (!siteNav || !navToggle) return;
  siteNav.dataset.open = String(open);
  navToggle.setAttribute('aria-expanded', String(open));
  navToggle.classList.toggle('is-open', open);
  navToggle.querySelector('.sr-only').textContent = open ? 'Close navigation' : 'Open navigation';
  if (!open) setIndustryMenu(false);
}

navToggle?.addEventListener('click', () => {
  setMainNavigation(navToggle.getAttribute('aria-expanded') !== 'true');
});
industryToggle?.addEventListener('click', () => {
  setIndustryMenu(industryToggle.getAttribute('aria-expanded') !== 'true');
});
industryMenu?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    setIndustryMenu(false);
    setMainNavigation(false);
  });
});
siteNav?.querySelectorAll(':scope > a').forEach((link) => {
  link.addEventListener('click', () => setMainNavigation(false));
});
document.addEventListener('click', (event) => {
  if (siteHeader && !siteHeader.contains(event.target)) {
    setIndustryMenu(false);
    setMainNavigation(false);
  }
});
document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  setIndustryMenu(false);
  setMainNavigation(false);
});
matchMedia('(min-width: 1051px)').addEventListener?.('change', (event) => {
  if (event.matches) setMainNavigation(false);
});

/* Route the guided finder through the same catalogue filters. */
function findSupplies(term) {
  if (document.body.dataset.product || !document.getElementById('catalogue')) {
    location.href = `${FUTURE_CATALOGUE_URL}?q=${encodeURIComponent(term)}#catalogue`;
    return;
  }
  active = 'all';
  document.getElementById('search').value = term;
  document.getElementById('listing-type').value = 'all';
  document.getElementById('sort-order').value = 'review';
  render();
  document.getElementById('catalogue').scrollIntoView({
    behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
  });
  document.getElementById('search').focus({ preventScroll: true });
}

const finderForm = document.getElementById('finder-form');
if (finderForm) {
  finderForm.addEventListener('submit', (event) => {
    event.preventDefault();
    findSupplies(document.getElementById('finder-query').value.trim());
  });
}

document
  .querySelectorAll('[data-suggest]')
  .forEach((button) =>
    button.addEventListener('click', () => findSupplies(button.dataset.suggest)),
  );

/* Rotate the homepage logistics story with dots, keyboard controls and touch swipes. */
const heroCarousel = document.querySelector('[data-hero-carousel]');
if (heroCarousel) {
  const track = heroCarousel.querySelector('.hero-carousel-track');
  const slides = [...heroCarousel.querySelectorAll('.hero-carousel-slide')];
  const dots = [...heroCarousel.querySelectorAll('[data-carousel-dot]')];
  const caption = heroCarousel.querySelector('figcaption');
  const count = heroCarousel.querySelector('[data-carousel-count]');
  const title = heroCarousel.querySelector('[data-carousel-title]');
  const copy = heroCarousel.querySelector('[data-carousel-copy]');
  const content = [
    ['Prepared with care.', 'Laboratory orders packed with purpose.'],
    ['Coordinated delivery.', 'Responsive support from dispatch to receipt.'],
    ['Quality checked.', 'Requirements reviewed before the work begins.'],
    ['Ready for the work.', 'Essential equipment where it matters.'],
  ];
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let currentSlide = 0;
  let carouselTimer;
  let announcementTimer;
  let pointerStartX = null;

  function showSlide(index, announce = false) {
    currentSlide = (index + slides.length) % slides.length;
    if (announce) caption.setAttribute('aria-live', 'polite');
    slides.forEach((slide, slideIndex) => {
      const activeSlide = slideIndex === currentSlide;
      slide.classList.toggle('is-active', activeSlide);
      slide.toggleAttribute('aria-hidden', !activeSlide);
    });
    dots.forEach((dot, dotIndex) => {
      const activeDot = dotIndex === currentSlide;
      dot.classList.toggle('is-active', activeDot);
      activeDot ? dot.setAttribute('aria-current', 'true') : dot.removeAttribute('aria-current');
    });
    count.textContent = `${String(currentSlide + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
    [title.textContent, copy.textContent] = content[currentSlide];
    clearTimeout(announcementTimer);
    if (announce) {
      announcementTimer = setTimeout(() => caption.setAttribute('aria-live', 'off'), 1200);
    }
  }

  function stopCarousel() {
    clearInterval(carouselTimer);
  }

  function startCarousel() {
    stopCarousel();
    if (!reducedMotion.matches && !document.hidden) {
      carouselTimer = setInterval(() => showSlide(currentSlide + 1), 6500);
    }
  }

  dots.forEach((dot) =>
    dot.addEventListener('click', () => showSlide(Number(dot.dataset.carouselDot), true)),
  );
  heroCarousel.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') showSlide(currentSlide - 1, true);
    if (event.key === 'ArrowRight') showSlide(currentSlide + 1, true);
  });
  track.addEventListener('pointerdown', (event) => {
    if (event.isPrimary) pointerStartX = event.clientX;
  });
  track.addEventListener('pointerup', (event) => {
    if (pointerStartX === null || !event.isPrimary) return;
    const distance = event.clientX - pointerStartX;
    pointerStartX = null;
    if (Math.abs(distance) < 48) return;
    showSlide(currentSlide + (distance < 0 ? 1 : -1), true);
  });
  track.addEventListener('pointercancel', () => {
    pointerStartX = null;
  });
  heroCarousel.addEventListener('mouseenter', stopCarousel);
  heroCarousel.addEventListener('mouseleave', startCarousel);
  heroCarousel.addEventListener('focusin', stopCarousel);
  heroCarousel.addEventListener('focusout', () => {
    if (!heroCarousel.contains(document.activeElement)) startCarousel();
  });
  document.addEventListener('visibilitychange', startCarousel);
  reducedMotion.addEventListener?.('change', startCarousel);
  startCarousel();
}

/* Keep the orbit ring fixed and rotate a separate electron track inside it. */
const orbit = document.querySelector('.orbit');
if (orbit) {
  orbit.innerHTML = '<span class="electron-track"><span class="electron"></span></span>';
}

/* Keep telephone and WhatsApp roles consistent on every generated page. */
document.querySelectorAll('.topline a[href^="tel:"]').forEach((link) => {
  link.href = 'tel:+27112387334';
  link.innerHTML = 'Telephone &nbsp; 011 238 7334';
});
document.querySelectorAll('.contact-details a[href^="tel:"]').forEach((link) => {
  link.href = 'tel:+27112387334';
  link.textContent = 'Telephone: 011 238 7334';
});
document.querySelectorAll('.contact-details .whatsapp').forEach((link) => {
  link.href =
    'https://wa.me/27844106544?text=' +
    encodeURIComponent('Hello Comeiin Works, I would like help with a quotation.');
  link.textContent = 'WhatsApp: 084 410 6544 ↗︎';
});

/* Route "About" and "Privacy" links through Django URLs */
document
  .querySelectorAll('header nav a[href="#about"], header nav a[href="about.html"], header nav a[href="index.html#about"]')
  .forEach((link) => (link.href = ABOUT_URL));
document
  .querySelectorAll('footer a[href$="/privacy.html"], footer a[href="privacy.html"]')
  .forEach((link) => (link.href = PRIVACY_URL));

/* Lightweight WhatsApp concierge */
const whatsappMessage =
  'Hello Comeiin Works, I would like help with a laboratory supply quotation.';
const whatsappUrl = 'https://wa.me/27844106544?text=' + encodeURIComponent(whatsappMessage);

const whatsappWidget = document.createElement('aside');
whatsappWidget.className = 'whatsapp-widget';
whatsappWidget.setAttribute('aria-label', 'WhatsApp assistance');
whatsappWidget.innerHTML = `<div class="whatsapp-chat" id="whatsapp-chat"><button class="whatsapp-close" aria-label="Close WhatsApp message">×</button><div class="whatsapp-agent"><span>COMEIIN</span><i aria-hidden="true"></i></div><p><strong>How can we help?</strong>Tell us what your laboratory needs and continue the conversation with our team.</p><a href="${whatsappUrl}" target="_blank" rel="noopener">Continue in WhatsApp <span>↗︎</span></a></div><button class="whatsapp-launch" aria-expanded="true" aria-controls="whatsapp-chat" aria-label="Chat with Comeiin Works on WhatsApp"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 4.25A11.75 11.75 0 0 0 5.78 21.8L4.4 27.6l5.95-1.55A11.75 11.75 0 1 0 16 4.25Z"/><path d="M11.1 9.9c.35-.35.8-.3 1.08.12l1.55 2.34c.2.32.2.7-.06.98l-.82.9c-.25.28-.2.62-.03.91.9 1.56 2.27 2.86 3.9 3.7.3.16.63.18.88-.08l.94-.98c.26-.28.65-.33.98-.13l2.36 1.42c.42.25.5.7.17 1.08l-.78.9c-.68.78-1.75 1.1-2.74.83-4.34-1.18-7.9-4.56-9.31-8.83-.33-.98-.06-2.08.68-2.8l1.5-1.36Z"/></svg></button>`;
document.body.append(whatsappWidget);

const whatsappChat = whatsappWidget.querySelector('.whatsapp-chat');
const whatsappLaunch = whatsappWidget.querySelector('.whatsapp-launch');

function setWhatsAppOpen(open) {
  whatsappChat.hidden = !open;
  whatsappLaunch.setAttribute('aria-expanded', String(open));
}

whatsappWidget
  .querySelector('.whatsapp-close')
  .addEventListener('click', () => setWhatsAppOpen(false));
whatsappLaunch.addEventListener('click', () => setWhatsAppOpen(whatsappChat.hidden));
setWhatsAppOpen(false);

})();
