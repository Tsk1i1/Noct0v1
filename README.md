# Dashboard Profissional — CP1 Data Science

Dashboard em Streamlit com portfólio profissional + estudo de mercado sobre
vagas de estágio em TI.

## Estrutura

```
dashboard-estagio-ti/
├── app.py                       # Aba "Quem sou eu" (página inicial)
├── pages/
│   ├── 1_Qualificacoes.py       # Aba "Minhas Qualificações"
│   ├── 2_Skills.py              # Aba "Skills"
│   └── 3_Estudo_de_Mercado.py   # Aba "Estudo de Mercado"
├── utils/
│   ├── data_loader.py           # Carregamento e limpeza da base de dados
│   └── theme.py                 # Alternância de tema claro/escuro
├── data/
│   └── vagas_estagio_ti.xlsx    # Base de dados (vagas de estágio em TI)
├── assets/
│   └── foto_perfil.jpg          # Minha foto de perfil escolhida
├── .streamlit/config.toml       # Configurações do Streamlit da página
└── requirements.txt
```

## Rodar localmente

```bash
python -m venv venv
source venv/bin/activate       
pip install -r requirements.txt
streamlit run app.py
```

## Tema claro/escuro

O tema é controlado pelo **alternador nativo do Streamlit**: clique no
menu **⋮** (canto superior direito) → **Settings** → **Theme** → escolha
"Dark". Isso reconfigura todos os componentes (sidebar, botões,
dropdowns, menus) de uma vez, sem precisar de CSS customizado.


