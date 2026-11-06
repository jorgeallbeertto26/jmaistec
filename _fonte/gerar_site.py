#!/usr/bin/env python3
"""Gerador do site J+ TEC Tecnologia.

Monta todas as páginas estáticas com o mesmo cabeçalho, rodapé e SEO.
Uso (na raiz do repositório):  python3 _fonte/gerar_site.py
Depois, envie os arquivos gerados ao GitHub. A pasta _fonte não é publicada pelo GitHub Pages.
"""
import json, os, re, datetime
from html import escape

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://jmaistec.com.br"
HOJE = datetime.date.today().isoformat()

EMPRESA = "J+ TEC Tecnologia"
EMAIL = "jorge@jmaistec.com.br"
WA_NUM = "5521966810304"
WA_TXT = "(21) 96681-0304"
OUTROS_TEL = "(22) 98849-2137 · (21) 98854-5380"
INSTAGRAM = "https://www.instagram.com/jmaistec/"

# ---------------------------------------------------------------- ícones
SPRITE = """<svg class="sr-only" width="0" height="0" aria-hidden="true" focusable="false">
<symbol id="i-infra" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M7 7h.01M7 17h.01M11 7h6M11 17h6"/></g></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.2 7.7-8 9-4.8-1.3-8-4.5-8-9V6l8-3z"/><path d="M9 12l2.2 2.2L15.5 10"/></g></symbol>
<symbol id="i-code" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9.5 10l-2.5 2 2.5 2M14.5 10l2.5 2-2.5 2"/></g></symbol>
<symbol id="i-wa" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" d="M12 3.2a8.8 8.8 0 0 0-7.6 13.2L3.2 20.8l4.5-1.2A8.8 8.8 0 1 0 12 3.2z"/><path fill="currentColor" d="M9.2 8.2c-.3.5-.3 1.3.2 2.3a9.8 9.8 0 0 0 4.1 3.9c1 .5 1.8.5 2.3.2l.7-.7c.3-.3.3-.7 0-1l-1.2-.9a.8.8 0 0 0-1 0l-.4.4c-.9-.4-1.8-1.3-2.2-2.2l.4-.4a.8.8 0 0 0 0-1l-.9-1.2c-.3-.3-.7-.3-1 0z"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.8"/></g></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/></g></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M6.6 3.5h2.6l1.4 4-2 1.3a11 11 0 0 0 6.6 6.6l1.3-2 4 1.4v2.6a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z"/></symbol>
<symbol id="i-insta" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".6" fill="currentColor"/></g></symbol>
<symbol id="i-layers" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/></g></symbol>
<symbol id="i-user" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/></g></symbol>
<symbol id="i-pulse" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M3 12h4l2.5-6 5 12L17 12h4"/></symbol>
<symbol id="i-chat" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M4 5h16v11H9l-5 4z"/></symbol>
</svg>"""

def ico(name, cls="ico"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'

ARROW = '<span class="arrow" aria-hidden="true">→</span>'
NOVA_ABA = '<span class="sr-only"> (abre em nova aba)</span>'

# ---------------------------------------------------------------- serviços
SERVICOS = [
    {
        "slug": "infraestrutura-de-ti", "nome": "Infraestrutura de TI", "icone": "infra",
        "title": "Infraestrutura de TI para empresas | Redes, servidores e nuvem | J+ TEC",
        "desc": "Planejamento, implantação e administração de redes, servidores, Active Directory, virtualização, nuvem, VoIP e CFTV. Solicite um orçamento à J+ TEC Tecnologia.",
        "resumo": "Planejamento, implantação, administração e otimização de ambientes de TI para manter sua operação conectada, estável e eficiente.",
        "lead": "Ambientes de TI planejados, organizados e monitorados para que a sua operação fique conectada, estável e pronta para crescer.",
        "itens": [
            ("Redes corporativas e conectividade", "Projeto, cabeamento, Wi-Fi e organização da rede para conexões estáveis entre pessoas, equipamentos e sistemas."),
            ("Servidores, Active Directory e ambientes Windows/Linux", "Implantação e administração de servidores, contas, permissões e serviços de rede."),
            ("Virtualização e ambientes em nuvem", "Uso mais eficiente de recursos com máquinas virtuais e serviços em nuvem adequados ao porte do negócio."),
            ("Monitoramento, disponibilidade e desempenho", "Acompanhamento do ambiente para identificar falhas e gargalos antes que afetem a rotina."),
            ("Telefonia IP (VoIP) e sistemas de CFTV", "Comunicação e segurança física integradas à rede da empresa."),
            ("Suporte técnico e melhoria da infraestrutura", "Atendimento a problemas do dia a dia e evolução contínua do ambiente."),
        ],
        "faq": [
            ("O que é avaliado antes de qualquer mudança na infraestrutura?", "O ponto de partida é entender o ambiente atual: rede, equipamentos, servidores, acessos e as necessidades da operação. A partir disso, as recomendações são alinhadas às prioridades e às possibilidades de cada cliente."),
            ("A J+ TEC trabalha com Windows e Linux?", "Sim. A atuação inclui servidores e ambientes Windows e Linux, além de Active Directory, virtualização e serviços em nuvem."),
            ("Infraestrutura e segurança podem ser tratadas juntas?", "Sim. Infraestrutura, cibersegurança e soluções digitais são pensadas de forma complementar, para que o ambiente seja ao mesmo tempo estável e protegido."),
        ],
    },
    {
        "slug": "ciberseguranca", "nome": "Cibersegurança", "icone": "shield",
        "title": "Cibersegurança para empresas | Riscos, acessos e backup | J+ TEC",
        "desc": "Avaliação de vulnerabilidades e riscos, proteção de identidades e acessos, segurança de endpoints, monitoramento, backup e continuidade. Fale com a J+ TEC Tecnologia.",
        "resumo": "Proteção de ambientes digitais com foco na redução de riscos, prevenção de ameaças e fortalecimento da segurança da informação.",
        "lead": "Redução de riscos, prevenção de ameaças e boas práticas de segurança da informação aplicadas à realidade da sua empresa.",
        "itens": [
            ("Avaliação de vulnerabilidades e riscos", "Identificação de pontos fracos no ambiente e priorização do que corrigir primeiro."),
            ("Proteção de identidades e controle de acessos", "Contas, senhas, permissões e autenticação reforçada para que cada pessoa acesse só o que precisa."),
            ("Segurança de endpoints e ambientes corporativos", "Proteção de computadores, servidores e dispositivos usados no dia a dia."),
            ("Monitoramento e análise de eventos", "Acompanhamento de registros e alertas para detectar comportamentos suspeitos."),
            ("Backup, continuidade de negócios e recuperação", "Cópias de segurança e planos para retomar a operação após incidentes."),
            ("Orientação em boas práticas e governança de segurança", "Políticas, processos e conscientização da equipe sobre segurança da informação."),
        ],
        "faq": [
            ("Por onde começar a melhorar a segurança da empresa?", "Pela avaliação de riscos: entender quais dados e sistemas são mais importantes, onde estão as vulnerabilidades e o que deve ser priorizado. Assim o investimento vai primeiro para o que reduz mais risco."),
            ("Backup também faz parte da cibersegurança?", "Sim. Backup, continuidade de negócios e recuperação são essenciais para retomar a operação após falhas, erros humanos ou ataques, como sequestro de dados (ransomware)."),
            ("A equipe da empresa também é orientada?", "Sim. A orientação em boas práticas e governança de segurança faz parte do trabalho, porque boa parte dos incidentes começa com ações do dia a dia, como cliques em mensagens falsas."),
        ],
    },
    {
        "slug": "desenvolvimento-web", "nome": "Desenvolvimento Web", "icone": "code",
        "title": "Desenvolvimento web | Sites, sistemas e automações | J+ TEC",
        "desc": "Criação de sites institucionais, landing pages, sistemas e aplicações web, formulários, integrações e automações, com SEO técnico e foco em celular. J+ TEC Tecnologia.",
        "resumo": "Criação de experiências digitais modernas, responsivas e funcionais para fortalecer a presença online e apoiar os objetivos do negócio.",
        "lead": "Sites, sistemas e automações modernos, rápidos e responsivos para fortalecer a presença online e apoiar os objetivos do seu negócio.",
        "itens": [
            ("Sites institucionais e landing pages", "Páginas claras, rápidas e responsivas que apresentam a empresa e geram contatos."),
            ("Sistemas e aplicações web", "Ferramentas sob medida, acessadas pelo navegador, para organizar processos do negócio."),
            ("Formulários e integrações", "Captura de contatos e pedidos ligada a e-mail, WhatsApp e outros serviços."),
            ("Automações de processos", "Tarefas repetitivas executadas de forma automática, com menos erros e mais agilidade."),
            ("Desempenho, SEO técnico e experiência mobile", "Carregamento rápido, estrutura otimizada para buscadores e boa navegação no celular."),
            ("Segurança desde o projeto", "Boas práticas de segurança da informação aplicadas ao código, à hospedagem e aos formulários."),
        ],
        "faq": [
            ("O site fica bom no celular?", "Sim. Os projetos são responsivos, ou seja, se adaptam a celulares, tablets e computadores, com atenção especial à experiência mobile."),
            ("O site já sai otimizado para o Google?", "Os projetos incluem SEO técnico: títulos e descrições por página, estrutura de cabeçalhos, dados estruturados, sitemap e bom desempenho de carregamento. O posicionamento nos resultados depende também de conteúdo e tempo."),
            ("Dá para ver exemplos de projetos?", "Sim. Na página de portfólio estão as marcas e iniciativas relacionadas à experiência da J+ TEC, como a Drogaria Show Popular e a Dani JM – Festas com Amor."),
        ],
    },
]

PROJETOS = [
    {"nome": "Drone Vision", "tag": "Imagens aéreas", "url": "https://dronevision.com.br/", "img": "/assets/projetos/drone-vision-logo.png", "w": 822, "h": 673, "tipo": "logo",
     "txt": "Projetos com drones e soluções de imagem aérea para o Rio de Janeiro e região, unindo tecnologia, planejamento e produção visual."},
    {"nome": "Maker Drone", "tag": "Tecnologia de drones", "url": "https://makerdrone.com.br/", "img": "/assets/projetos/maker-drone.jpg", "w": 1400, "h": 963, "tipo": "foto",
     "txt": "Iniciativa envolvendo tecnologia de drones, operação e recursos de imagem aérea."},
    {"nome": "Droga Show", "tag": "Varejo farmacêutico", "url": "https://drogariashowpopular.com.br/", "img": "/assets/projetos/droga-show-logo.png", "w": 600, "h": 572, "tipo": "logo-claro",
     "txt": "Presença online da Drogaria Show Popular, no Centro de Nova Iguaçu (RJ), com consulta de produtos e atendimento pelo WhatsApp."},
    {"nome": "Dani JM – Festas com Amor", "tag": "Decoração de festas", "url": "https://danifestascomamor.com.br/", "img": "/assets/projetos/dani-jm-logo.svg", "w": 600, "h": 300, "tipo": "logo-claro",
     "txt": "Página de decoração de festas e locação de peças, com galeria de temas, escolha de cores e pedido de orçamento pelo WhatsApp."},
]

ETAPAS = [
    ("Entendimento", "Conversamos sobre o desafio, o ambiente atual e os objetivos do negócio."),
    ("Proposta clara", "Escopo definido, explicações sem jargão e alinhamento de expectativas."),
    ("Implantação", "Execução organizada, com atenção à estabilidade e à segurança."),
    ("Acompanhamento", "Ajustes, orientação e evolução contínua depois da entrega."),
]

DIFERENCIAIS = [
    ("layers", "Visão integrada", "Infraestrutura, segurança e soluções digitais pensadas de forma complementar."),
    ("user", "Abordagem personalizada", "Recomendações alinhadas às necessidades, prioridades e possibilidades de cada cliente."),
    ("pulse", "Foco em confiabilidade", "Atenção à estabilidade, segurança, organização e continuidade das operações."),
    ("chat", "Comunicação transparente", "Explicações claras, escopo definido e alinhamento de expectativas durante o projeto."),
]

# ---------------------------------------------------------------- blocos comuns
ORG_ID = SITE + "/#organizacao"
ORG = {
    "@context": "https://schema.org", "@type": "Organization", "@id": ORG_ID,
    "name": EMPRESA, "alternateName": "J+ TEC", "url": SITE + "/",
    "logo": SITE + "/assets/logo-jmais.svg", "image": SITE + "/assets/og-image.jpg",
    "email": EMAIL, "telephone": "+55-21-96681-0304", "sameAs": [INSTAGRAM],
    "contactPoint": [{"@type": "ContactPoint", "telephone": "+55-21-96681-0304", "contactType": "sales", "availableLanguage": "Portuguese"}],
    "knowsAbout": ["Infraestrutura de TI", "Cibersegurança", "Segurança da informação", "Desenvolvimento web"],
}

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"

def breadcrumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)]}

def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

CSP = ("default-src 'self'; img-src 'self' data:; font-src 'self'; style-src 'self'; script-src 'self'; "
       "connect-src 'self' https://api.web3forms.com https://formspree.io; base-uri 'self'; object-src 'none'; form-action 'self'")

def head(title, desc, path, extra_ld=(), noindex=False):
    url = SITE + path
    blocos = "\n  ".join(ld(x) for x in extra_ld)
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  {robots}
  <meta name="theme-color" content="#0a1830">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="{EMPRESA}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Logo da J+ TEC Tecnologia">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/poppins-700.woff" as="font" type="font/woff" crossorigin>
  <link rel="stylesheet" href="/css/style.css">
  <script src="/js/config.js" defer></script>
  <script src="/js/main.js" defer></script>
  {blocos}
</head>"""

def cur(path, alvo):
    return ' aria-current="page"' if path == alvo else ""

def header(path):
    subs = "".join(f'<li><a href="/servicos/{s["slug"]}/"{cur(path, "/servicos/" + s["slug"] + "/")}>{s["nome"]}</a></li>' for s in SERVICOS)
    return f"""<body>
{SPRITE}
<a class="skip-link" href="#conteudo">Ir para o conteúdo</a>
<header class="site-header on-dark">
  <div class="wrap site-header__bar">
    <a class="brand" href="/" aria-label="J+ TEC Tecnologia, página inicial"><img src="/assets/logo-jmais.svg" alt="J+ TEC Tecnologia" width="131" height="42"></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu"><span class="menu-toggle__bars" aria-hidden="true"></span>Menu</button>
    <nav class="nav" id="menu" aria-label="Principal">
      <ul>
        <li><a href="/"{cur(path, "/")}>Início</a></li>
        <li class="has-sub"><a href="/servicos/"{cur(path, "/servicos/")}>Serviços</a><ul class="sub">{subs}</ul></li>
        <li><a href="/portfolio/"{cur(path, "/portfolio/")}>Portfólio</a></li>
        <li><a href="/sobre/"{cur(path, "/sobre/")}>Sobre</a></li>
        <li><a href="/contato/"{cur(path, "/contato/")}>Contato</a></li>
        <li><a class="btn btn--primary" href="/contato/">Solicitar orçamento</a></li>
      </ul>
    </nav>
  </div>
</header>"""

def footer():
    servs = "".join(f'<li><a href="/servicos/{s["slug"]}/">{s["nome"]}</a></li>' for s in SERVICOS)
    return f"""<footer class="site-footer on-dark">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="/assets/logo-jmais.svg" alt="J+ TEC Tecnologia" width="144" height="46" loading="lazy">
        <p>Infraestrutura, segurança e soluções digitais para empresas que precisam evoluir com confiança.</p>
      </div>
      <div><h2>Serviços</h2><ul>{servs}</ul></div>
      <div><h2>Navegação</h2><ul><li><a href="/portfolio/">Portfólio</a></li><li><a href="/sobre/">Sobre</a></li><li><a href="/contato/">Contato</a></li><li><a href="/privacidade/">Política de Privacidade</a></li></ul></div>
      <div><h2>Contato</h2><ul>
        <li><a href="https://wa.me/{WA_NUM}" target="_blank" rel="noopener noreferrer">WhatsApp {WA_TXT}{NOVA_ABA}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram @jmaistec{NOVA_ABA}</a></li>
      </ul></div>
    </div>
    <p class="footer__bottom">© <span id="ano">2026</span> {EMPRESA}. Todos os direitos reservados.</p>
  </div>
</footer>
<a class="wa-float" href="https://wa.me/{WA_NUM}" target="_blank" rel="noopener noreferrer" aria-label="Conversar pelo WhatsApp (abre em nova aba)">{ico("wa", "")}</a>
</body>
</html>
"""

def page_hero(trail, titulo, lead, icone=None):
    bc = "".join((f'<li><a href="{u}">{escape(n)}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{escape(n)}</li>') for i, (n, u) in enumerate(trail))
    ic = ico(icone, "ico-big") if icone else ""
    return f"""<section class="band page-hero on-dark">
  <canvas class="net" data-density="low" aria-hidden="true"></canvas>
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Você está em"><ol>{bc}</ol></nav>
    <div data-reveal>{ic}<h1>{titulo}</h1><p class="lead">{lead}</p></div>
  </div>
</section>"""

def cta(titulo="Vamos encontrar a solução certa para sua empresa?", texto="Conte seu desafio. Vamos entender sua necessidade e identificar como a tecnologia pode ajudar seu negócio a avançar.", servico=None, sid=None):
    href = "/contato/" + (f"?servico={servico}" if servico else "")
    idattr = f' id="{sid}"' if sid else ""
    return f"""<section class="band cta on-dark"{idattr}>
  <canvas class="net" data-density="low" aria-hidden="true"></canvas>
  <div class="wrap" data-reveal="zoom">
    <h2>{titulo}</h2>
    <p>{texto}</p>
    <div class="btn-row">
      <a class="btn btn--primary" href="{escape(href)}">Solicitar orçamento {ARROW}</a>
      <a class="btn btn--ghost" href="https://wa.me/{WA_NUM}" target="_blank" rel="noopener noreferrer">{ico("wa")}Conversar pelo WhatsApp{NOVA_ABA}</a>
    </div>
  </div>
</section>"""

def card_servico(s, i):
    lis = "".join(f"<li>{escape(t)}</li>" for t, _ in s["itens"][:5])
    nome_min = s["nome"][0].lower() + s["nome"][1:] if s["slug"] != "infraestrutura-de-ti" else s["nome"]
    return f"""<article class="card d{i+1}" data-reveal>
  {ico(s["icone"], "card__icon")}
  <h3>{s["nome"]}</h3>
  <p>{s["resumo"]}</p>
  <ul>{lis}</ul>
  <a class="more" href="/servicos/{s["slug"]}/">Ver {nome_min} {ARROW}<span class="sr-only"> em detalhes</span></a>
</article>"""

def card_projeto(p, i):
    if p["tipo"] == "foto":
        media_cls, alt = "project__media project__media--photo", f"Imagem do projeto {p['nome']}"
    elif p["tipo"] == "logo-claro":
        media_cls, alt = "project__media project__media--light", f"Logo da {p['nome']}"
    else:
        media_cls, alt = "project__media", f"Logo da {p['nome']}"
    return f"""<article class="card project d{(i % 2) + 1}" data-reveal>
  <div class="{media_cls}"><img src="{p["img"]}" alt="{escape(alt)}" width="{p["w"]}" height="{p["h"]}" loading="lazy" decoding="async"></div>
  <div class="project__body">
    <span class="tag">{p["tag"]}</span>
    <h3>{escape(p["nome"])}</h3>
    <p>{p["txt"]}</p>
    <a class="more" href="{p["url"]}" target="_blank" rel="noopener noreferrer">Visitar projeto {ARROW}<span class="sr-only"> {escape(p["nome"])} (abre em nova aba)</span></a>
  </div>
</article>"""

def etapas_html():
    lis = "".join(f'<li class="d{i+1}" data-reveal><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(ETAPAS))
    return f'<ol class="steps">{lis}</ol>'

def diferenciais_html():
    return '<div class="grid grid--2">' + "".join(
        f'<div class="card feature d{i+1}" data-reveal>{ico(ic, "card__icon")}<div><h3>{t}</h3><p>{d}</p></div></div>'
        for i, (ic, t, d) in enumerate(DIFERENCIAIS)) + "</div>"

def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details data-reveal><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in faq) + "</div>"

def relativizar(html, path):
    """Troca caminhos "/x" por relativos ("../x"), para o site abrir tanto no GitHub Pages
    quanto direto do disco (duplo clique no index.html). Links de pasta ganham "index.html"."""
    prof = path.strip("/").count("/") + 1 if path.endswith("/") and path != "/" else 0
    pre = "../" * prof
    def troca(m):
        attr, alvo = m.group(1), m.group(2)
        base, _, resto = alvo.partition("?")
        if base.endswith("/"):
            base += "index.html"
        novo = pre + base.lstrip("/")
        return f'{attr}="{novo}{"?" + resto if resto else ""}"'
    return re.sub(r'\b(href|src)="(/(?!/)[^"#]*)"', troca, html)

def escrever(path, html):
    destino = os.path.join(RAIZ, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(RAIZ, path.lstrip("/"))
    if path != "/404.html":   # a 404 é servida em qualquer endereço, então mantém caminhos absolutos
        html = relativizar(html, path)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    print("gerado:", os.path.relpath(destino, RAIZ))

# ---------------------------------------------------------------- páginas
def pagina_inicio():
    path = "/"
    website = {"@context": "https://schema.org", "@type": "WebSite", "name": EMPRESA, "url": SITE + "/", "inLanguage": "pt-BR", "publisher": {"@id": ORG_ID}}
    chips = "".join(f'<li>{ico(s["icone"])}{s["nome"]}</li>' for s in SERVICOS)
    cards = "".join(card_servico(s, i) for i, s in enumerate(SERVICOS))
    projetos = "".join(card_projeto(p, i) for i, p in enumerate(PROJETOS))
    html = head("J+ TEC Tecnologia | Infraestrutura de TI, Cibersegurança e Desenvolvimento Web",
                "Infraestrutura de TI, cibersegurança e desenvolvimento web para empresas que buscam mais segurança, eficiência e presença digital. Solicite um orçamento à J+ TEC Tecnologia.",
                path, [ORG, website]) + header(path) + f"""
<main id="conteudo">
<section class="band hero on-dark">
  <canvas class="net" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="hero__inner">
      <p class="eyebrow" data-reveal>Infraestrutura · Segurança · Web</p>
      <h1 data-reveal class="d1"><span class="sr-only">Tecnologia confiável para proteger, conectar e impulsionar seu negócio.</span><span aria-hidden="true">Tecnologia confiável para <span class="typed" data-typed="proteger|conectar|impulsionar">proteger</span><span class="caret"></span><br>seu negócio.</span></h1>
      <p class="hero__text d2" data-reveal>Infraestrutura de TI, cibersegurança e desenvolvimento web para empresas que buscam mais segurança, eficiência e presença digital.</p>
      <div class="btn-row d3" data-reveal>
        <a class="btn btn--primary" href="/servicos/">Conheça nossas soluções {ARROW}</a>
        <a class="btn btn--ghost" href="/contato/">Fale com um especialista</a>
      </div>
      <ul class="hero__chips d4" data-reveal>{chips}</ul>
    </div>
  </div>
  <span class="scroll-cue" aria-hidden="true"></span>
</section>

<section class="section" id="servicos">
  <div class="wrap">
    <div class="section__head" data-reveal>
      <span class="kicker">Serviços</span>
      <h2>Soluções de tecnologia para o seu negócio.</h2>
      <p>Três áreas que se complementam, com recomendações alinhadas à realidade de cada cliente.</p>
    </div>
    <div class="grid grid--3">{cards}</div>
  </div>
</section>

<section class="section section--gray" id="como-trabalhamos">
  <div class="wrap">
    <div class="section__head" data-reveal>
      <span class="kicker">Como trabalhamos</span>
      <h2>Do primeiro contato à evolução contínua.</h2>
      <p>Um caminho simples e transparente, com escopo definido e alinhamento de expectativas em cada etapa.</p>
    </div>
    {etapas_html()}
  </div>
</section>

<section class="section" id="diferenciais">
  <div class="wrap">
    <div class="section__head" data-reveal>
      <span class="kicker">Diferenciais</span>
      <h2>Tecnologia com visão prática de negócio.</h2>
    </div>
    {diferenciais_html()}
  </div>
</section>

<section class="section section--gray" id="portfolio">
  <div class="wrap">
    <div class="section__head" data-reveal>
      <span class="kicker">Portfólio</span>
      <h2>Projetos e iniciativas que demonstram nossa versatilidade.</h2>
      <p>Marcas e iniciativas relacionadas à nossa experiência em tecnologia, soluções digitais e produção de conteúdo aéreo.</p>
    </div>
    <div class="grid grid--2">{projetos}</div>
    <p class="note" data-reveal><a class="btn btn--outline" href="/portfolio/">Ver portfólio completo {ARROW}</a></p>
  </div>
</section>

<section class="section" id="sobre">
  <div class="wrap split">
    <div data-reveal="left">
      <span class="kicker">Sobre a J+ TEC</span>
      <h2>Tecnologia com experiência e visão estratégica.</h2>
      <p>A J+ TEC Tecnologia reúne conhecimentos em infraestrutura de TI, segurança da informação e desenvolvimento de soluções digitais para ajudar empresas a utilizar a tecnologia de maneira mais segura, eficiente e estratégica.</p>
      <p><a class="more" href="/sobre/">Conheça a J+ TEC {ARROW}</a></p>
    </div>
    <div class="band panel on-dark" data-reveal="right">
      <ul class="pillars">{"".join(f'<li>{ico(s["icone"])}{s["nome"]}</li>' for s in SERVICOS)}</ul>
    </div>
  </div>
</section>

{cta(sid="contato")}
</main>
""" + footer()
    escrever(path, html)

def pagina_servicos():
    path = "/servicos/"
    trail = [("Início", "/"), ("Serviços", path)]
    cards = "".join(card_servico(s, i) for i, s in enumerate(SERVICOS))
    html = head("Serviços de TI para empresas | Infraestrutura, Cibersegurança e Web | J+ TEC",
                "Conheça os serviços da J+ TEC Tecnologia: infraestrutura de TI, cibersegurança e desenvolvimento web, pensados de forma integrada para a realidade de cada empresa.",
                path, [ORG, breadcrumbs_ld(trail)]) + header(path) + f"""
<main id="conteudo">
{page_hero(trail, "Soluções de tecnologia para o seu negócio", "Três áreas que se complementam: a infraestrutura mantém a operação funcionando, a segurança protege o que é importante e a web leva o negócio mais longe.")}
<section class="section">
  <div class="wrap"><div class="grid grid--3">{cards}</div></div>
</section>
<section class="section section--gray">
  <div class="wrap">
    <div class="section__head" data-reveal><span class="kicker">Como trabalhamos</span><h2>Um processo claro do início ao fim.</h2></div>
    {etapas_html()}
  </div>
</section>
{cta()}
</main>
""" + footer()
    escrever(path, html)

def pagina_servico(s):
    path = f"/servicos/{s['slug']}/"
    trail = [("Início", "/"), ("Serviços", "/servicos/"), (s["nome"], path)]
    serv_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["nome"], "serviceType": s["nome"],
               "description": s["resumo"], "url": SITE + path, "provider": {"@id": ORG_ID},
               "hasOfferCatalog": {"@type": "OfferCatalog", "name": s["nome"], "itemListElement": [
                   {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}} for t, d in s["itens"]]}}
    itens = "".join(f'<li class="d{(i % 3) + 1}" data-reveal>{ico("check")}<div><strong>{escape(t)}</strong><span>{escape(d)}</span></div></li>' for i, (t, d) in enumerate(s["itens"]))
    outros = "".join(card_servico(o, i) for i, o in enumerate(x for x in SERVICOS if x is not s))
    html = head(s["title"], s["desc"], path, [ORG, serv_ld, breadcrumbs_ld(trail), faq_ld(s["faq"])]) + header(path) + f"""
<main id="conteudo">
{page_hero(trail, s["nome"], s["lead"], s["icone"])}
<section class="section">
  <div class="wrap">
    <div class="section__head" data-reveal><span class="kicker">O que fazemos</span><h2>{s["nome"]} sob medida para a sua empresa.</h2><p>{s["resumo"]}</p></div>
    <ul class="checks">{itens}</ul>
  </div>
</section>
<section class="section section--gray">
  <div class="wrap">
    <div class="section__head" data-reveal><span class="kicker">Como trabalhamos</span><h2>Do diagnóstico à evolução contínua.</h2></div>
    {etapas_html()}
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section__head" data-reveal><span class="kicker">Perguntas frequentes</span><h2>Dúvidas sobre {s["nome"].lower() if s["slug"] != "infraestrutura-de-ti" else "infraestrutura de TI"}</h2></div>
    {faq_html(s["faq"])}
  </div>
</section>
{cta(titulo="Vamos conversar sobre " + ("a sua infraestrutura de TI?" if s["slug"] == "infraestrutura-de-ti" else ("a segurança da sua empresa?" if s["slug"] == "ciberseguranca" else "o seu projeto web?")), servico=s["nome"])}
<section class="section section--gray">
  <div class="wrap">
    <div class="section__head" data-reveal><span class="kicker">Soluções integradas</span><h2>Conheça também</h2></div>
    <div class="grid grid--2">{outros}</div>
  </div>
</section>
</main>
""" + footer()
    escrever(path, html)

def pagina_portfolio():
    path = "/portfolio/"
    trail = [("Início", "/"), ("Portfólio", path)]
    lista = {"@context": "https://schema.org", "@type": "ItemList", "name": "Portfólio J+ TEC", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": p["nome"], "url": p["url"]} for i, p in enumerate(PROJETOS)]}
    projetos = "".join(card_projeto(p, i) for i, p in enumerate(PROJETOS))
    html = head("Portfólio | Projetos e iniciativas | J+ TEC Tecnologia",
                "Conheça projetos e iniciativas relacionados à experiência da J+ TEC Tecnologia: Drone Vision, Maker Drone, Drogaria Show Popular e Dani JM – Festas com Amor.",
                path, [ORG, breadcrumbs_ld(trail), lista]) + header(path) + f"""
<main id="conteudo">
{page_hero(trail, "Portfólio", "Projetos e iniciativas que demonstram nossa versatilidade em tecnologia, soluções digitais e produção de conteúdo aéreo.")}
<section class="section">
  <div class="wrap">
    <div class="grid grid--2">{projetos}</div>
    <p class="note" data-reveal>São marcas e iniciativas distintas, relacionadas à experiência da J+ TEC. Os serviços centrais da empresa continuam sendo infraestrutura de TI, cibersegurança e desenvolvimento web.</p>
  </div>
</section>
{cta(titulo="Quer um projeto como esses?", texto="Sites, páginas e soluções digitais com desempenho, segurança e boa experiência no celular.", servico="Desenvolvimento Web")}
</main>
""" + footer()
    escrever(path, html)

def pagina_sobre():
    path = "/sobre/"
    trail = [("Início", "/"), ("Sobre", path)]
    about = {"@context": "https://schema.org", "@type": "AboutPage", "name": "Sobre a J+ TEC Tecnologia", "url": SITE + path, "about": {"@id": ORG_ID}}
    html = head("Sobre a J+ TEC Tecnologia | Tecnologia com visão estratégica",
                "A J+ TEC Tecnologia reúne conhecimentos em infraestrutura de TI, segurança da informação e desenvolvimento de soluções digitais para empresas.",
                path, [ORG, breadcrumbs_ld(trail), about]) + header(path) + f"""
<main id="conteudo">
{page_hero(trail, "Tecnologia com experiência e visão estratégica", "Conhecimento técnico e visão de negócio para usar a tecnologia de maneira mais segura, eficiente e estratégica.")}
<section class="section">
  <div class="wrap split">
    <div data-reveal="left">
      <span class="kicker">Quem somos</span>
      <h2>Infraestrutura, segurança e soluções digitais em um só lugar.</h2>
      <p>A J+ TEC Tecnologia reúne conhecimentos em infraestrutura de TI, segurança da informação e desenvolvimento de soluções digitais para ajudar empresas a utilizar a tecnologia de maneira mais segura, eficiente e estratégica.</p>
      <p>Nossa abordagem combina conhecimento técnico, visão de negócio e soluções adequadas aos desafios de cada projeto, buscando simplificar operações, fortalecer ambientes tecnológicos e criar experiências digitais de qualidade.</p>
    </div>
    <div class="band panel on-dark" data-reveal="right">
      <ul class="pillars">{"".join(f'<li>{ico(s["icone"])}<a href="/servicos/{s["slug"]}/">{s["nome"]}</a></li>' for s in SERVICOS)}</ul>
    </div>
  </div>
</section>
<section class="section section--gray">
  <div class="wrap">
    <div class="section__head" data-reveal><span class="kicker">Diferenciais</span><h2>Tecnologia com visão prática de negócio.</h2></div>
    {diferenciais_html()}
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section__head" data-reveal><span class="kicker">Como trabalhamos</span><h2>Transparência em cada etapa.</h2></div>
    {etapas_html()}
  </div>
</section>
{cta()}
</main>
""" + footer()
    escrever(path, html)

def pagina_contato():
    path = "/contato/"
    trail = [("Início", "/"), ("Contato", path)]
    contato = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contato J+ TEC Tecnologia", "url": SITE + path, "about": {"@id": ORG_ID}}
    opts = "".join(f'<option value="{s["nome"]}">{s["nome"]}</option>' for s in SERVICOS)
    html = head("Contato e orçamento | J+ TEC Tecnologia",
                f"Fale com a J+ TEC Tecnologia pelo WhatsApp {WA_TXT}, por e-mail ou pelo formulário e solicite um orçamento de infraestrutura de TI, cibersegurança ou desenvolvimento web.",
                path, [ORG, breadcrumbs_ld(trail), contato]) + header(path) + f"""
<main id="conteudo">
{page_hero(trail, "Solicite seu orçamento", "Descreva sua necessidade. Respondemos pelo canal que você preferir.")}
<section class="section section--gray">
  <div class="wrap contact">
    <div data-reveal="left">
      <h2>Fale com a J+ TEC</h2>
      <ul class="contact__list">
        <li>{ico("wa")}<div><strong>WhatsApp</strong><a href="https://wa.me/{WA_NUM}" target="_blank" rel="noopener noreferrer">{WA_TXT}{NOVA_ABA}</a></div></li>
        <li>{ico("phone")}<div><strong>Outros telefones</strong>{OUTROS_TEL}</div></li>
        <li>{ico("mail")}<div><strong>E-mail</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
        <li>{ico("insta")}<div><strong>Instagram</strong><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">@jmaistec{NOVA_ABA}</a></div></li>
      </ul>
    </div>
    <form class="form" id="form-contato" novalidate data-reveal="right">
      <div class="field"><label for="f-nome">Nome</label><input id="f-nome" name="name" type="text" autocomplete="name" required maxlength="120"><span class="err" id="e-nome" aria-live="polite"></span></div>
      <div class="field"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="160"><span class="err" id="e-email" aria-live="polite"></span></div>
      <div class="field"><label for="f-empresa">Empresa (opcional)</label><input id="f-empresa" name="company" type="text" autocomplete="organization" maxlength="120"></div>
      <div class="field"><label for="f-servico">Serviço de interesse</label><select id="f-servico" name="service" required><option value="">Selecione…</option>{opts}<option value="Ainda não sei / outro assunto">Ainda não sei / outro assunto</option></select><span class="err" id="e-servico" aria-live="polite"></span></div>
      <div class="field"><label for="f-msg">Mensagem</label><textarea id="f-msg" name="message" required maxlength="3000"></textarea><span class="err" id="e-msg" aria-live="polite"></span></div>
      <div class="hp" aria-hidden="true"><label for="f-bot">Não preencha este campo</label><input id="f-bot" name="botcheck" type="text" tabindex="-1" autocomplete="off"></div>
      <button class="btn btn--primary" id="f-enviar" type="submit">Enviar mensagem</button>
      <div id="f-status" role="status" aria-live="polite" hidden></div>
      <small>Usamos seus dados apenas para responder a este contato. Saiba mais na <a href="/privacidade/">Política de Privacidade</a>.</small>
    </form>
  </div>
</section>
</main>
""" + footer()
    escrever(path, html)

def pagina_privacidade():
    path = "/privacidade/"
    trail = [("Início", "/"), ("Política de Privacidade", path)]
    with open(os.path.join(RAIZ, "_fonte", "privacidade-corpo.html"), encoding="utf-8") as f:
        corpo = f.read()
    html = head("Política de Privacidade | J+ TEC Tecnologia",
                "Como a J+ TEC Tecnologia trata os dados pessoais recebidos pelo site e pelos canais de contato, nos termos da LGPD.",
                path, [breadcrumbs_ld(trail)]) + header(path) + f"""
<main id="conteudo">
{page_hero(trail, "Política de Privacidade", "Transparência sobre como tratamos seus dados, nos termos da LGPD.")}
<div class="doc"><div class="wrap doc__inner">{corpo}</div></div>
</main>
""" + footer()
    escrever(path, html)
    # endereço antigo continua funcionando
    escrever("/privacidade.html", f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Política de Privacidade | J+ TEC</title><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/privacidade/"><meta http-equiv="refresh" content="0; url=/privacidade/"></head><body><p><a href="/privacidade/">A Política de Privacidade mudou de endereço. Clique aqui.</a></p></body></html>
""")

def pagina_404():
    html = head("Página não encontrada | J+ TEC Tecnologia", "A página procurada não existe ou mudou de endereço.", "/404.html", noindex=True) + header("/404") + f"""
<main id="conteudo" class="band notfound on-dark">
  <canvas class="net" data-density="low" aria-hidden="true"></canvas>
  <div class="wrap"><p class="code">404</p><h1>Página não encontrada</h1><p>O endereço pode estar incorreto ou a página mudou de lugar.</p>
  <div class="btn-row" style-free><a class="btn btn--primary" href="/">Voltar ao início</a><a class="btn btn--ghost" href="/servicos/">Ver serviços</a></div></div>
</main>
""".replace(" style-free", "") + footer()
    escrever("/404.html", html)

def sitemap():
    urls = ["/", "/servicos/"] + [f"/servicos/{s['slug']}/" for s in SERVICOS] + ["/portfolio/", "/sobre/", "/contato/", "/privacidade/"]
    pri = {"/": "1.0", "/contato/": "0.8", "/privacidade/": "0.3"}
    corpo = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{HOJE}</lastmod><priority>{pri.get(u, '0.9' if u.startswith('/servicos/') else '0.7')}</priority></url>\n" for u in urls)
    with open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{corpo}</urlset>\n')
    print("gerado: sitemap.xml")

if __name__ == "__main__":
    pagina_inicio(); pagina_servicos()
    for s in SERVICOS: pagina_servico(s)
    pagina_portfolio(); pagina_sobre(); pagina_contato(); pagina_privacidade(); pagina_404(); sitemap()
