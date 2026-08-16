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

Cada página tem um seletor "🎨 Tema" no topo da sidebar. A escolha fica salva
em `st.session_state` e vale para todas as abas durante a sessão do usuário
(assim que ele muda de página, o tema é mantido). A implementação está toda
centralizada em `utils/theme.py` — para ajustar as cores, edite os dicionários
`CORES_CLARO` e `CORES_ESCURO` nesse arquivo.

## Próximos passos de conteúdo

- [ ] Adicionar foto real em `assets/foto_perfil.jpg`
- [ ] Preencher minibio em `app.py`
- [ ] Listar GS's, hackathons, nanocursos e challenges em `pages/1_🎓_Qualificacoes.py`
- [ ] Ajustar skills, idiomas e ferramentas em `pages/2_🛠️_Skills.py`
- [ ] Escrever os insights reais (textos em itálico "edite") na página de
      Estudo de Mercado, depois de olhar os gráficos gerados
- [ ] Substituir/completar `data/vagas_estagio_ti.xlsx` com os dados finais
      do professor quando forem liberados
