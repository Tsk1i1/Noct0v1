# Dashboard Profissional — CP1 Data Science

Dashboard em Streamlit com portfólio profissional + estudo de mercado sobre
vagas de estágio em TI.

## Estrutura

```
dashboard-estagio-ti/
├── app.py                       # Aba "Quem sou eu" (página inicial)
├── pages/
│   ├── 1_🎓_Qualificacoes.py    # Aba "Minhas Qualificações"
│   ├── 2_🛠️_Skills.py           # Aba "Skills"
│   └── 3_📊_Estudo_de_Mercado.py # Aba "Estudo de Mercado"
├── utils/
│   ├── data_loader.py           # Carregamento e limpeza da base de dados
│   └── theme.py                 # Alternância de tema claro/escuro
├── data/
│   └── vagas_estagio_ti.xlsx    # Base de dados (vagas de estágio em TI)
├── assets/
│   └── foto_perfil.jpg          # Coloque aqui sua foto (ainda não incluída)
├── .streamlit/config.toml       # Tema visual
└── requirements.txt
```

## Rodar localmente

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Publicar no Streamlit Community Cloud (gratuito)

1. Crie um repositório no GitHub e suba esta pasta inteira (`git init`, `git add .`,
   `git commit -m "primeira versão"`, `git push`).
2. Acesse https://share.streamlit.io e faça login com sua conta GitHub.
3. Clique em **"New app"**, selecione o repositório, a branch e o arquivo
   principal (`app.py`).
4. Clique em **Deploy**. Em poucos minutos você recebe um link público
   (ex: `https://seu-app.streamlit.app`) — esse é o link a entregar.
5. Qualquer novo `git push` para o repositório atualiza o app publicado
   automaticamente.

## Tema claro/escuro

O tema agora é controlado pelo **alternador nativo do Streamlit**: clique no
menu **⋮** (canto superior direito) → **Settings** → **Theme** → escolha
"Dark". Isso reconfigura corretamente todos os componentes (sidebar, botões,
dropdowns, menus) de uma vez, sem precisar de CSS customizado.

Uma versão anterior tentava forçar o tema escuro via CSS injetado por cima
de um app configurado como claro no `config.toml` — isso deixava alguns
componentes internos do Streamlit (o conteúdo de dropdowns/menus, que pegam
cor direto do tema interno, não do CSS da página) sem estilo correto. A
correção foi parar de travar `backgroundColor`/`textColor` no
`.streamlit/config.toml`, o que libera o alternador nativo — daí ele cuida
de tudo automaticamente, sem exceções.

`utils/theme.py` ainda existe, mas só pra detectar se o tema nativo ativo é
claro ou escuro (via `st.context.theme`) e colorir os gráficos Plotly da
aba "Estudo de Mercado" de forma compatível.

## Próximos passos de conteúdo

- [ ] Adicionar foto real em `assets/foto_perfil.jpg`
- [ ] Preencher minibio em `app.py`
- [ ] Listar GS's, hackathons, nanocursos e challenges em `pages/1_🎓_Qualificacoes.py`
- [ ] Ajustar skills, idiomas e ferramentas em `pages/2_🛠️_Skills.py`
- [ ] Escrever os insights reais (textos em itálico "edite") na página de
      Estudo de Mercado, depois de olhar os gráficos gerados
- [ ] Substituir/completar `data/vagas_estagio_ti.xlsx` com os dados finais
      do professor quando forem liberados
