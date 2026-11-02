# Site J+ TEC Tecnologia

Página única em HTML, CSS e JavaScript puros. Sem cookies, sem rastreadores e sem fontes externas.

## Arquivos
- `index.html`, `privacidade.html`, `404.html`: páginas.
- `css/style.css`: visual (cores em `:root`). `js/main.js`: menu e formulário. `js/config.js`: **configuração do formulário**.
- `assets/logo-jmais.svg` (para fundo escuro) e `assets/logo-jmais-claro.svg` (para fundo claro): logo J+ TEC refeita em vetor.
- `assets/projetos/`: logos do portfólio. `robots.txt`, `sitemap.xml`, `_headers`.

## Ativar o formulário (obrigatório antes de divulgar)
O site é estático e não tem servidor. Enquanto `formEndpoint` estiver vazio em `js/config.js`, o formulário **não finge envio**: mostra um aviso e oferece WhatsApp e e-mail.
Para ativar, use um serviço de formulários com plano gratuito, por exemplo:
1. **Web3Forms**: crie uma chave de acesso com o e-mail que vai receber as mensagens e preencha
   `formEndpoint: "https://api.web3forms.com/submit"` e `formExtraFields: { access_key: "SUA_CHAVE" }`.
2. **Formspree**: crie um formulário e use a URL dele em `formEndpoint`.
Confira o limite mensal do plano gratuito no site do provedor. Depois, teste um envio real e informe o nome do provedor no item 5 de `privacidade.html`.

## Publicar sem perder o domínio
1. **Faça backup** do site atual (baixe todos os arquivos da hospedagem de `jmaistec.com.br`).
2. Envie estes arquivos para a mesma hospedagem, mantendo `index.html` na raiz. Não altere DNS nem domínio.
3. Para voltar à versão anterior, restaure o backup.
Se a hospedagem atual for o GitHub Pages, basta enviar os arquivos ao repositório (com as pastas) e manter o arquivo `CNAME`.

## Pendências
- Logo da **Drone Vision**: o arquivo não foi recebido. Siga o comentário em `index.html` (cartão "Drone Vision").
- Logo da **Droga Show** foi ampliada de 160 px para 600 px (suavização, não recuperação de detalhe). Para qualidade perfeita, use o arquivo original (SVG/AI/PNG grande).
- Redes sociais: só adicionar depois de confirmar os endereços.
