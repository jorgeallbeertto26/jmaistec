/* J+ TEC — JavaScript puro, sem dependências e sem rastreamento. */
(function () {
  "use strict";
  var cfg = window.JMAIS_CONFIG || {};
  var t0 = Date.now();

  try { var ano = document.getElementById("ano"); if (ano) ano.textContent = String(new Date().getFullYear()); } catch (e) {}

  /* Menu móvel */
  try {
    var toggle = document.querySelector(".menu-toggle"), menu = document.getElementById("menu");
    if (toggle && menu) {
      var mq = window.matchMedia("(min-width: 960px)");
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

  /* Botões "Conhecer solução" pré-selecionam o serviço no formulário */
  try {
    var sel = document.getElementById("f-servico");
    document.querySelectorAll("[data-servico]").forEach(function (a) {
      a.addEventListener("click", function () { if (sel) sel.value = a.getAttribute("data-servico"); });
    });
  } catch (e) {}

  /* Formulário */
  var form = document.getElementById("form-contato");
  if (!form) return;
  var status = document.getElementById("f-status"), btn = document.getElementById("f-enviar");
  var fields = {
    name: ["f-nome", "e-nome", "Informe seu nome."],
    email: ["f-email", "e-email", "Informe um e-mail válido."],
    service: ["f-servico", "e-servico", "Escolha um serviço de interesse."],
    message: ["f-msg", "e-msg", "Escreva uma mensagem com pelo menos 10 caracteres."]
  };
  var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function showStatus(kind, html) {
    status.hidden = false; status.className = "status status--" + kind; status.innerHTML = html;
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function validate(data) {
    var first = null;
    Object.keys(fields).forEach(function (k) {
      var el = document.getElementById(fields[k][0]), err = document.getElementById(fields[k][1]), v = (data[k] || "").trim(), bad = false;
      if (k === "email") bad = !emailRe.test(v);
      else if (k === "message") bad = v.length < 10;
      else bad = v.length === 0;
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
    return '<br><a class="btn btn--outline" href="' + whatsappLink(d) + '" target="_blank" rel="noopener noreferrer">Enviar pelo WhatsApp</a> ' +
           '<a class="btn btn--outline" href="mailto:' + esc(cfg.email || "") + '">Escrever por e-mail</a>';
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var fd = new FormData(form), d = {};
    ["name", "email", "company", "service", "message"].forEach(function (k) { d[k] = String(fd.get(k) || "").trim(); });

    var bad = validate(d);
    if (bad) { bad.focus(); showStatus("err", "Revise os campos destacados e tente novamente."); return; }

    if (fd.get("botcheck")) return;                       // isca anti-spam preenchida: descarta em silêncio
    if (Date.now() - t0 < 3000) { showStatus("err", "Aguarde um instante e envie novamente."); return; }

    if (!cfg.formEndpoint) {                              // sem serviço configurado: nada de sucesso falso
      showStatus("err", "O envio por formulário ainda não está ativo neste site. Para não perder seu contato, use um dos canais abaixo:" + fallbackHtml(d));
      return;
    }

    btn.disabled = true; btn.textContent = "Enviando…"; showStatus("ok", "Enviando sua mensagem…");
    var ctl = new AbortController(), timer = setTimeout(function () { ctl.abort(); }, 15000);
    var payload = Object.assign({}, cfg.formExtraFields || {}, {
      name: d.name, email: d.email, company: d.company, service: d.service, message: d.message,
      subject: "Contato pelo site J+ TEC — " + d.service
    });
    fetch(cfg.formEndpoint, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(payload), signal: ctl.signal })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok && j.success !== false, j: j }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error("falha");
        showStatus("ok", "Mensagem enviada. Obrigado! Retornaremos em breve.");
        form.reset();
      })
      .catch(function () { showStatus("err", "Não foi possível enviar agora. Tente novamente ou use outro canal:" + fallbackHtml(d)); })
      .then(function () { clearTimeout(timer); btn.disabled = false; btn.textContent = "Enviar mensagem"; });
  });
})();
