/* J+ TEC — JavaScript puro, sem dependências e sem rastreamento.
   Animações: rede no topo (canvas), texto digitando, revelar ao rolar e holofote nos cards.
   Tudo é desligado quando o visitante pede "reduzir movimento" no sistema. */
(function () {
  "use strict";
  var cfg = window.JMAIS_CONFIG || {};
  var t0 = Date.now();
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.documentElement.classList.add("js");

  try { var ano = document.getElementById("ano"); if (ano) ano.textContent = String(new Date().getFullYear()); } catch (e) {}

  /* Cabeçalho com sombra ao rolar */
  try {
    var header = document.querySelector(".site-header");
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    if (header) { onScroll(); window.addEventListener("scroll", onScroll, { passive: true }); }
  } catch (e) {}

  /* Menu móvel */
  try {
    var toggle = document.querySelector(".menu-toggle"), menu = document.getElementById("menu");
    if (toggle && menu) {
      var mq = window.matchMedia("(min-width: 1000px)");
      var setOpen = function (open, back) {
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        menu.classList.toggle("is-open", open);
        if (!open && back) toggle.focus();
      };
      toggle.addEventListener("click", function () { setOpen(toggle.getAttribute("aria-expanded") !== "true"); });
      menu.addEventListener("click", function (ev) { if (ev.target.closest("a")) setOpen(false); });
      document.addEventListener("keydown", function (ev) { if (ev.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") setOpen(false, true); });
      mq.addEventListener("change", function () { if (mq.matches) setOpen(false); });
    }
  } catch (e) { var m = document.getElementById("menu"); if (m) m.classList.add("is-open"); }

  /* Revelar ao rolar */
  try {
    var items = document.querySelectorAll("[data-reveal]");
    if (reduce || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("is-visible"); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); } });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
      items.forEach(function (el) { io.observe(el); });
    }
  } catch (e) { document.documentElement.classList.remove("js"); }

  /* Holofote que segue o mouse dentro dos cards */
  try {
    if (!reduce && window.matchMedia("(hover: hover)").matches) {
      document.querySelectorAll(".card").forEach(function (c) {
        c.addEventListener("pointermove", function (ev) {
          var r = c.getBoundingClientRect();
          c.style.setProperty("--mx", (ev.clientX - r.left) + "px");
          c.style.setProperty("--my", (ev.clientY - r.top) + "px");
        });
      });
    }
  } catch (e) {}

  /* Texto digitando no título principal */
  try {
    var typed = document.querySelector("[data-typed]");
    if (typed) {
      var words = typed.getAttribute("data-typed").split("|");
      if (reduce) { typed.textContent = words[0]; }
      else {
        var wi = 0, ci = words[0].length, del = true;
        typed.textContent = words[0];
        var tick = function () {
          var w = words[wi], delay;
          if (del) { ci--; typed.textContent = w.slice(0, ci); delay = 45; if (ci <= 0) { del = false; wi = (wi + 1) % words.length; delay = 320; } }
          else { ci++; typed.textContent = words[wi].slice(0, ci); delay = 85; if (ci >= words[wi].length) { del = true; delay = 2200; } }
          setTimeout(tick, delay);
        };
        setTimeout(tick, 2400);
      }
    }
  } catch (e) {}

  /* Rede animada (nós e conexões) nas faixas escuras */
  try {
    document.querySelectorAll("canvas.net").forEach(function (cv) {
      var ctx = cv.getContext("2d"); if (!ctx) return;
      var host = cv.parentElement, dpr = Math.min(window.devicePixelRatio || 1, 2);
      var W = 0, H = 0, pts = [], mouse = { x: -9999, y: -9999 }, running = false, raf = 0, visible = true;
      var dense = cv.getAttribute("data-density") === "low" ? 26000 : 15000;
      var LINK = 140;
      function size() {
        var r = host.getBoundingClientRect(); W = r.width; H = r.height;
        cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        var n = Math.max(18, Math.min(110, Math.round(W * H / dense)));
        pts = [];
        for (var i = 0; i < n; i++) pts.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35, r: Math.random() * 1.6 + .8, g: Math.random() < .08 });
      }
      function draw() {
        ctx.clearRect(0, 0, W, H);
        for (var i = 0; i < pts.length; i++) {
          var p = pts[i];
          if (running) {
            p.x += p.vx; p.y += p.vy;
            if (p.x < 0 || p.x > W) p.vx *= -1; if (p.y < 0 || p.y > H) p.vy *= -1;
            var mdx = mouse.x - p.x, mdy = mouse.y - p.y, md = mdx * mdx + mdy * mdy;
            if (md < 22000) { p.x -= mdx * .006; p.y -= mdy * .006; }
          }
          for (var j = i + 1; j < pts.length; j++) {
            var q = pts[j], dx = p.x - q.x, dy = p.y - q.y, d = Math.sqrt(dx * dx + dy * dy);
            if (d < LINK) { ctx.strokeStyle = "rgba(125,178,255," + (0.28 * (1 - d / LINK)).toFixed(3) + ")"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke(); }
          }
        }
        for (var k = 0; k < pts.length; k++) {
          var s = pts[k];
          ctx.fillStyle = s.g ? "rgba(217,169,59,.95)" : "rgba(160,205,255,.85)";
          ctx.beginPath(); ctx.arc(s.x, s.y, s.g ? s.r + .8 : s.r, 0, Math.PI * 2); ctx.fill();
        }
      }
      function loop() { draw(); if (running) raf = requestAnimationFrame(loop); }
      function start() { if (!running && !reduce && visible && !document.hidden) { running = true; raf = requestAnimationFrame(loop); } }
      function stop() { running = false; cancelAnimationFrame(raf); }
      size(); draw();
      var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { size(); draw(); }, 150); });
      host.addEventListener("pointermove", function (ev) { var r = host.getBoundingClientRect(); mouse.x = ev.clientX - r.left; mouse.y = ev.clientY - r.top; });
      host.addEventListener("pointerleave", function () { mouse.x = mouse.y = -9999; });
      document.addEventListener("visibilitychange", function () { document.hidden ? stop() : start(); });
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (en) { visible = en[0].isIntersecting; visible ? start() : stop(); }).observe(host);
      } else start();
    });
  } catch (e) {}

  /* Formulário de contato */
  var form = document.getElementById("form-contato");
  if (!form) return;
  var status = document.getElementById("f-status"), btn = document.getElementById("f-enviar");
  var sel = document.getElementById("f-servico");
  try {
    var q = new URLSearchParams(window.location.search).get("servico");
    if (q && sel) Array.prototype.forEach.call(sel.options, function (o) { if (o.value === q) sel.value = q; });
  } catch (e) {}
  var fields = {
    name: ["f-nome", "e-nome", "Informe seu nome."],
    email: ["f-email", "e-email", "Informe um e-mail válido."],
    service: ["f-servico", "e-servico", "Escolha um serviço de interesse."],
    message: ["f-msg", "e-msg", "Escreva uma mensagem com pelo menos 10 caracteres."]
  };
  var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function showStatus(kind, html) { status.hidden = false; status.className = "status status--" + kind; status.innerHTML = html; }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function validate(data) {
    var first = null;
    Object.keys(fields).forEach(function (k) {
      var el = document.getElementById(fields[k][0]), err = document.getElementById(fields[k][1]), v = (data[k] || "").trim(), bad;
      if (k === "email") bad = !emailRe.test(v); else if (k === "message") bad = v.length < 10; else bad = v.length === 0;
      el.setAttribute("aria-invalid", bad ? "true" : "false");
      if (bad) el.setAttribute("aria-describedby", fields[k][1]); else el.removeAttribute("aria-describedby");
      err.textContent = bad ? fields[k][2] : "";
      if (bad && !first) first = el;
    });
    return first;
  }
  function whatsappLink(d) {
    var txt = "Olá! Meu nome é " + d.name + (d.company ? " (" + d.company + ")" : "") + ". Serviço de interesse: " + d.service + ". " + d.message;
    return "https://wa.me/" + (cfg.whatsapp || "") + "?text=" + encodeURIComponent(txt.slice(0, 1200));
  }
  function fallbackHtml(d) {
    return '<br><a class="btn btn--wa" href="' + esc(whatsappLink(d)) + '" target="_blank" rel="noopener noreferrer">Enviar pelo WhatsApp</a> ' +
           '<a class="btn btn--outline" href="mailto:' + esc(cfg.email || "") + '">Escrever por e-mail</a>';
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var fd = new FormData(form), d = {};
    ["name", "email", "company", "service", "message"].forEach(function (k) { d[k] = String(fd.get(k) || "").trim(); });
    var bad = validate(d);
    if (bad) { bad.focus(); showStatus("err", "Revise os campos destacados e tente novamente."); return; }
    if (fd.get("botcheck")) return;                                   // isca anti-spam preenchida
    if (Date.now() - t0 < 3000) { showStatus("err", "Aguarde um instante e envie novamente."); return; }
    if (!cfg.formEndpoint) {                                          // sem serviço configurado: nada de sucesso falso
      showStatus("err", "O envio por formulário ainda não está ativo. Para não perder seu contato, use um dos canais abaixo:" + fallbackHtml(d));
      return;
    }
    btn.disabled = true; btn.textContent = "Enviando…"; showStatus("ok", "Enviando sua mensagem…");
    var ctl = new AbortController(), timer = setTimeout(function () { ctl.abort(); }, 15000);
    var payload = Object.assign({}, cfg.formExtraFields || {}, {
      name: d.name, email: d.email, company: d.company, service: d.service, message: d.message,
      subject: "Contato pelo site J+ TEC — " + d.service
    });
    fetch(cfg.formEndpoint, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(payload), signal: ctl.signal })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok && j.success !== false }; }); })
      .then(function (res) { if (!res.ok) throw new Error("falha"); showStatus("ok", "Mensagem enviada. Obrigado! Retornaremos em breve."); form.reset(); })
      .catch(function () { showStatus("err", "Não foi possível enviar agora. Tente novamente ou use outro canal:" + fallbackHtml(d)); })
      .then(function () { clearTimeout(timer); btn.disabled = false; btn.textContent = "Enviar mensagem"; });
  });
})();
