# Nicolas Mendes — portfólio

Portfólio em Streamlit com apresentação pessoal, formação, competências e um estudo exploratório da busca por estágio em TI.

## Executar

Use Python 3.11 ou superior. Na pasta do projeto:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

Abra o endereço local informado pelo Streamlit. O ambiente validado nesta atualização usou Python 3.14.7, Streamlit 1.62.0, pandas 3.0.5, Plotly 6.9.0, SciPy 1.18.0 e openpyxl 3.1.5.

## Páginas

- **Apresentação:** perfil, contato e estudo de vagas em destaque.
- **Qualificações:** formação, projetos e cursos.
- **Competências:** tecnologias e exemplos de uso, ferramentas e idiomas.
- **Estudo de mercado:** sete análises, filtros por nicho e formato de trabalho, tabela e exportação CSV.

Os arquivos e os caminhos existentes em `pages/` foram mantidos. Assim, endereços como `/Qualificacoes`, `/Skills` e `/Estudo_de_Mercado` continuam disponíveis. O tema pode ser alterado no menu do canto superior do Streamlit.

## Atualizar conteúdo

- Apresentação: `app.py`.
- Formação e competências: os respectivos arquivos em `pages/`.
- Navegação e contatos: `utils/ui.py`.
- Estilos: `assets/styles.css`; paleta nativa: `.streamlit/config.toml`.
- Vagas: `data/vagas_estagio_ti.xlsx`. Preserve os nomes das colunas. A planilha original foi mantida nesta renovação.

A base é uma coleta pessoal, não sistemática. Os resultados descrevem as vagas registradas e não representam todo o mercado. O CSV exporta apenas o recorte visível, com separador `;` e codificação UTF-8 com BOM para leitura no Excel.

## Verificar

```powershell
python -m unittest discover -s tests -v
python -m compileall -q app.py pages utils
```

Os testes abrem as quatro páginas, comparam indicadores com a base, combinam e limpam filtros, verificam recortes vazios e o conteúdo exportado.

## Publicação

O aplicativo atual usa Streamlit Community Cloud. Para atualizar a versão online, envie a branch revisada ao GitHub e integre-a à branch configurada no Streamlit. Nenhuma publicação é feita pelos comandos de execução ou teste acima.
