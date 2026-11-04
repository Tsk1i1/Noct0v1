# Noct0v1 — portfólio de Nicolas

## Stack e comandos
- Python, Streamlit, pandas, Plotly, SciPy; base Excel local com openpyxl.
- Rodar na raiz: `python -m streamlit run app.py`.
- Verificar: `python -m unittest discover -s tests -v` e `python -m compileall -q app.py pages utils`.

## Convenções e limites
- Manter `app.py` e os caminhos em `pages/` para preservar URLs existentes.
- Interface e textos em português. Preservar fatos pessoais; não inventar qualificações ou resultados.
- Usar `utils/ui.py` para identidade visual, cabeçalhos e navegação; componentes nativos para controles.
- Preservar a planilha original; evitar novas dependências de produção sem necessidade.
- Gráficos e conclusões devem respeitar o recorte selecionado, incluindo filtros sem resultados.
- Nenhum segredo, ambiente virtual, captura ou arquivo temporário no Git.
- Trabalhar em branch de feature; não publicar, fazer push ou alterar o site online sem solicitação.

## Direção visual
- Identidade editorial: branco e azul, azul profundo nos destaques, tipografia legível, bordas discretas, sem emojis decorativos.
- Tema claro e escuro legíveis, navegação por teclado e layout utilizável em celular.
- A apresentação profissional destaca projetos e evidências, sem percentuais subjetivos de domínio.

## Mapa
- `app.py`: apresentação e projeto em destaque.
- `pages/1_Qualificacoes.py`, `pages/2_Skills.py`: formação e competências.
- `pages/3_Estudo_de_Mercado.py`: dashboard e filtros.
- `utils/data_loader.py`: normalização e agregações; `utils/theme.py`: cores dos gráficos.
- `docs/visual-refresh.md`: escopo e verificação desta renovação.
