"""Verificação das páginas e dos recortes usando a base real do projeto."""

import os
from io import BytesIO
from pathlib import Path
import unittest
from unittest.mock import patch

import pandas as pd
import streamlit as st
from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = "pages/3_Estudo_de_Mercado.py"


class PortfolioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.previous_directory = Path.cwd()
        os.chdir(ROOT)
        from utils.data_loader import carregar_dados

        cls.base = carregar_dados()
        cls.base = cls.base[cls.base["Tipo da Vaga"].eq("Estágio")]

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.previous_directory)

    def run_page(self, path):
        page = AppTest.from_file(str(ROOT / "app.py"), default_timeout=45).run()
        if path != "app.py":
            page.switch_page(path).run()
        self.assertEqual([error.message for error in page.exception], [])
        return page

    def assert_metrics(self, page, expected):
        self.assertEqual([error.message for error in page.exception], [])
        metrics = {metric.label: metric.value for metric in page.metric}
        self.assertEqual(int(metrics["Vagas analisadas"]), len(expected))
        self.assertEqual(
            int(metrics["Empresas"]), expected["Nome da Empresa"].nunique()
        )
        self.assertEqual(
            int(metrics["Vagas de interesse"]), int(expected["Interessante"].sum())
        )

    def test_all_pages_render(self):
        for path in [
            "app.py",
            "pages/1_Qualificacoes.py",
            "pages/2_Skills.py",
            DASHBOARD,
        ]:
            with self.subTest(page=path):
                page = self.run_page(path)
                if path == DASHBOARD:
                    self.assert_metrics(page, self.base)

    def test_filters_update_counts_and_can_be_cleared(self):
        page = self.run_page(DASHBOARD)
        # Um recorte com dados testa a composição dos dois filtros.
        row = self.base.dropna(subset=["Nicho de Mercado", "Tipo de Trabalho"]).iloc[0]
        niche, work_type = row["Nicho de Mercado"], row["Tipo de Trabalho"]
        page.multiselect[0].select(niche).run()
        expected = self.base[self.base["Nicho de Mercado"].eq(niche)]
        self.assert_metrics(page, expected)

        page.multiselect[1].select(work_type).run()
        expected = expected[expected["Tipo de Trabalho"].eq(work_type)]
        self.assert_metrics(page, expected)

        page.checkbox[0].check().run()
        self.assert_metrics(page, expected)
        page.checkbox[0].uncheck().run()
        self.assert_metrics(page, expected)

        page.multiselect[0].set_value([])
        page.multiselect[1].set_value([]).run()
        self.assert_metrics(page, self.base)

    def test_empty_filter_combination_is_handled(self):
        page = self.run_page(DASHBOARD)
        pair = next(
            (
                (niche, work_type)
                for niche in self.base["Nicho de Mercado"].dropna().unique()
                for work_type in self.base["Tipo de Trabalho"].dropna().unique()
                if self.base[
                    self.base["Nicho de Mercado"].eq(niche)
                    & self.base["Tipo de Trabalho"].eq(work_type)
                ].empty
            ),
            None,
        )
        if pair is None:
            self.skipTest("A base contém dados em todas as combinações de filtros.")
        page.multiselect[0].select(pair[0])
        page.multiselect[1].select(pair[1]).run()
        self.assertEqual([error.message for error in page.exception], [])
        self.assertTrue(
            len(page.info) + len(page.warning) > 0,
            "O visitante precisa receber orientação quando o recorte não tem vagas.",
        )

    def test_export_contains_only_the_selected_rows(self):
        with patch("streamlit.download_button", wraps=st.download_button) as download:
            page = self.run_page(DASHBOARD)
            niche = self.base["Nicho de Mercado"].dropna().iloc[0]
            page.multiselect[0].select(niche).run()
            self.assertEqual([error.message for error in page.exception], [])
            self.assertTrue(download.called)
            exported = pd.read_csv(
                BytesIO(download.call_args.kwargs["data"]),
                encoding="utf-8-sig",
                sep=";",
            )
            expected = self.base[self.base["Nicho de Mercado"].eq(niche)]
            self.assertEqual(len(exported), len(expected))
            self.assertEqual(set(exported["Nicho de Mercado"]), {niche})
            self.assertEqual(
                exported["Nome da Vaga"].tolist(), expected["Nome da Vaga"].tolist()
            )
            self.assertNotIn("Tecnologias_Lista", exported.columns)
            self.assertNotIn("Beneficios_Lista", exported.columns)
            self.assertTrue(page.get("download_button"))


if __name__ == "__main__":
    unittest.main()
