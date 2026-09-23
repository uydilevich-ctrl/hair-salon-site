(() => {
  const fmt = (n) => n.toLocaleString('ru-RU').replace(/ /g, ' ');
  const tgLink = (text) =>
    `https://t.me/${CONFIG.telegram}` + (text ? `?text=${encodeURIComponent(text)}` : '');

  const priceHtml = (p) => {
    if (typeof p === 'string') return `<span class="price">${p}</span>`;
    if (Array.isArray(p)) {
      return `<span class="price tiers"><small>от</small>${p
        .map((v) => `<span>${fmt(v)}</span>`)
        .join('<b>/</b>')} ₽</span>`;
    }
    return `<span class="price"><small>от</small>${fmt(p)} ₽</span>`;
  };

  // Карточки услуг
  document.getElementById('cards').innerHTML = SERVICES.map((c, i) => {
    const from = Math.min(
      ...c.items.map(([, p]) => (Array.isArray(p) ? p[0] : typeof p === 'number' ? p : Infinity))
    );
    return `<a class="card" href="#prices" data-cat="${c.id}">
      <span class="card-num">0${i + 1}</span>
      <h3>${c.title}</h3>
      <p>${c.short}</p>
      <span class="card-from">от ${fmt(from)} ₽ <i>→</i></span>
    </a>`;
  }).join('');

  // Прайс с вкладками
  const tabs = document.getElementById('tabs');
  const list = document.getElementById('price-list');
  tabs.innerHTML = SERVICES.map(
    (c) => `<button role="tab" data-cat="${c.id}">${c.title}</button>`
  ).join('');

  const show = (id) => {
    const c = SERVICES.find((x) => x.id === id);
    tabs.querySelectorAll('button').forEach((b) =>
      b.setAttribute('aria-selected', String(b.dataset.cat === id))
    );
    const tiered = c.items.some(([, p]) => Array.isArray(p));
    list.innerHTML =
      (tiered ? '<p class="tiers-note">короткие / средние / длинные волосы</p>' : '') +
      c.items
        .map(
          ([name, p]) => `<div class="row">
          <span class="name">${name}</span>
          <span class="leader"></span>
          ${priceHtml(p)}
          <a class="book" target="_blank" rel="noopener"
             href="${tgLink(`Здравствуйте! Хочу записаться: ${name}.`)}">Записаться</a>
        </div>`
        )
        .join('');
    list.classList.remove('fade');
    void list.offsetWidth;
    list.classList.add('fade');
  };

  tabs.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (b) show(b.dataset.cat);
  });
  document.getElementById('cards').addEventListener('click', (e) => {
    const a = e.target.closest('.card');
    if (a) show(a.dataset.cat);
  });
  show(SERVICES[0].id);

  // Если фото нет — img удаляется, остаётся заглушка-градиент
  const photo = (src, alt = '') =>
    `<img src="${src}" alt="${alt}" loading="lazy"
      onload="this.parentNode.classList.add('loaded')" onerror="this.remove()">`;

  // До / после
  document.getElementById('works-list').innerHTML = WORKS.map(
    (w) => `<figure class="work">
      <div class="compare" style="--pos: 50%">
        <div class="layer after">${photo(w.after, `${w.title} — после`)}</div>
        <div class="layer before">${photo(w.before, `${w.title} — до`)}</div>
        <span class="tag tag-before">До</span><span class="tag tag-after">После</span>
        <span class="handle" aria-hidden="true"><i>‹ ›</i></span>
        <input type="range" min="0" max="100" value="50" aria-label="Сравнить до и после: ${w.title}">
      </div>
      <figcaption><h3>${w.title}</h3><span>${w.note}</span></figcaption>
    </figure>`
  ).join('');
  document.querySelectorAll('.compare input').forEach((r) =>
    r.addEventListener('input', () => r.parentNode.style.setProperty('--pos', `${r.value}%`))
  );

  // Фото салона + просмотр крупно
  const gallery = document.getElementById('gallery');
  gallery.innerHTML = SALON_PHOTOS.map(
    (p, i) => `<figure class="shot s${i + 1}" data-i="${i}">
      ${photo(p.src, p.caption)}
      <figcaption>${p.caption}</figcaption>
    </figure>`
  ).join('');
  const lb = document.getElementById('lightbox');
  gallery.addEventListener('click', (e) => {
    const f = e.target.closest('.shot.loaded');
    if (!f) return;
    const p = SALON_PHOTOS[f.dataset.i];
    lb.querySelector('img').src = p.src;
    lb.querySelector('img').alt = p.caption;
    lb.querySelector('.lb-caption').textContent = p.caption;
    lb.showModal();
  });
  lb.addEventListener('click', (e) => {
    if (e.target === lb || e.target.closest('.lb-close')) lb.close();
  });

  // Контакты
  document.querySelectorAll('.js-tg').forEach((a) => {
    a.href = tgLink(a.dataset.text);
    a.target = '_blank';
    a.rel = 'noopener';
  });
  document.querySelectorAll('.js-wa').forEach((a) => {
    a.href = `https://wa.me/${CONFIG.whatsapp}`;
    a.target = '_blank';
    a.rel = 'noopener';
  });
  document.querySelectorAll('.js-phone').forEach((a) => {
    a.href = `tel:${CONFIG.phone.replace(/[^\d+]/g, '')}`;
  });
  document.querySelector('.js-address').textContent = CONFIG.address;
  document.querySelector('.js-hours').textContent = CONFIG.hours;
  document.querySelector('.js-phone-text').textContent = CONFIG.phone;
  document.getElementById('year').textContent = new Date().getFullYear();

  // Мобильное меню
  const nav = document.querySelector('.nav');
  const burger = document.querySelector('.burger');
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('.menu a').forEach((a) =>
    a.addEventListener('click', () => nav.classList.remove('open'))
  );

  // Появление секций при прокрутке
  const io = new IntersectionObserver(
    (entries) =>
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      }),
    { threshold: 0.12 }
  );
  document.querySelectorAll('.section-head, .card, .point, .work, .shot, .contacts-inner').forEach((el) => {
    el.classList.add('rise');
    io.observe(el);
  });
})();
