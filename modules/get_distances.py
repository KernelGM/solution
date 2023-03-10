import pandas as pd
from loguru import logger

from modules.folders import data, output


class Distances:
    def __init__(self) -> None:
        self.sheet_distances()

    def sheet_distances(self):
        def fix_columns(row, flag, column, back):
            if row[column] == flag:
                return back
            else:
                return row[column]

        self.dist = pd.read_csv(
            f"{data}/distancias.csv",
            sep=",",
            skiprows=1,
            header=None,
            on_bad_lines="skip",
            low_memory=False,
            names=[
                "org",  # código do município de origem
                "dest",  # código do município de destino
                "km_linear",  # km do arco na superfície da terra, ligando os municípios # noqa: E501
                "km_rota",  # km da rota terrestre ligando os municípios
            ],
        )

        # Fix on column "km_linear" when display the specifc flag
        self.dist["km_linear"] = self.dist.apply(
            lambda row: fix_columns(row, "mesma cidade", "km_linear", 10.0),
            axis=1,
        )

        # Fix on column "km_rota" when display the specifc flag
        self.dist["km_rota"] = self.dist.apply(
            lambda row: fix_columns(row, "mesma cidade", "km_rota", 10.0),
            axis=1,
        )

        # Fix on column "km_rota" when display the specifc flag
        self.dist["km_rota"] = self.dist.apply(
            lambda row: fix_columns(
                row, "nao existe caminho entre os dois locais", "km_rota", 0.0
            ),
            axis=1,
        )

        # Convert "km_linear" and "km_rota" to float64 and "org" and "dest" to int64
        self.dist["km_linear"] = pd.to_numeric(self.dist["km_linear"], errors="coerce")
        self.dist["km_rota"] = pd.to_numeric(self.dist["km_rota"], errors="coerce")
        self.dist["org"] = pd.to_numeric(self.dist["org"], errors="coerce")
        self.dist["dest"] = pd.to_numeric(self.dist["dest"], errors="coerce")

        # Swap if rows "km_linear" > "km_rota"
        self.dist[["km_linear", "km_rota"]] = self.dist[["km_rota", "km_linear"]].where(
            self.dist["km_linear"] > self.dist["km_rota"],
            self.dist[["km_linear", "km_rota"]].values,
        )

        self.dist.to_csv(f"{output}/distance.csv", index=False, header=False)

        logger.debug("DataFrame 'distancia.csv' corrigido")
