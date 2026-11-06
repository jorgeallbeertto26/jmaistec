# Site J+ TEC Tecnologia

Site multipágina em HTML, CSS e JavaScript puros, hospedado no GitHub Pages (domínio em `CNAME`). Sem cookies, sem rastreadores e sem fontes externas.

## Páginas
| Endereço | Conteúdo |
|---|---|
| `/` | Início (rede animada, título digitando, serviços, etapas, diferenciais, portfólio) |
| `/servicos/` | Visão geral dos serviços |
| `/servicos/infraestrutura-de-ti/` · `/servicos/ciberseguranca/` · `/servicos/desenvolvimento-web/` | Uma página por serviço, com perguntas frequentes |
| `/portfolio/` · `/sobre/` · `/contato/` · `/privacidade/` | Demais páginas |
| `privacidade.html` | Redireciona o endereço antigo para `/privacidade/` |

## Como editar
Os textos ficam em `_fonte/gerar_site.py`. Depois de editar, rode na raiz:
```
python3 _fonte/gerar_site.py
```
Ele regera todas as páginas e o `sitemap.xml`. A pasta `_fonte` não é publicada pelo GitHub Pages.

## Animações
- Rede de nós e conexões nas faixas escuras (`canvas.net`), pausada fora da tela e com a aba oculta.
- Título digitando na página inicial (`data-typed`), com texto completo para leitores de tela e buscadores.
- Revelar ao rolar (`data-reveal`, `left`, `right`, `zoom`; atrasos `d1` a `d5`).
- Cards com elevação, borda animada e holofote que segue o mouse.
Todas são desligadas quando o sistema do visitante pede para reduzir movimento.

## SEO
Título e descrição únicos por página, `canonical`, Open Graph, dados estruturados (Organization, WebSite, Service, FAQPage, BreadcrumbList), `sitemap.xml` e `robots.txt`.
Depois de publicar: cadastre o domínio no Google Search Console e envie `https://jmaistec.com.br/sitemap.xml`.

## Ativar o formulário (obrigatório antes de divulgar)
Enquanto `formEndpoint` estiver vazio em `js/config.js`, o formulário não finge envio: mostra um aviso e oferece WhatsApp e e-mail.
- **Web3Forms**: `formEndpoint: "https://api.web3forms.com/submit"` e `formExtraFields: { access_key: "SUA_CHAVE" }`.
- **Formspree**: use a URL do formulário em `formEndpoint`.
Depois, teste um envio real e informe o provedor no item 5 da política de privacidade (`_fonte/privacidade-corpo.html`).

## Segurança
A política de segurança de conteúdo (CSP) está em uma `<meta>` em cada página, porque o GitHub Pages não lê o arquivo `_headers`. Não use atributos `style="..."` nem scripts embutidos: a CSP bloqueia.

## Pendências
- Revisar as perguntas frequentes das páginas de serviço.
- Área de atendimento (cidades/região) não foi informada; quando confirmar, dá para reforçar o SEO local.
- Logo da **Droga Show** foi ampliada de 160 px para 600 px; para qualidade perfeita, use o arquivo original.
- A pasta `img/` (logos originais em PNG e uma imagem gerada por IA) não é usada pelo site.
