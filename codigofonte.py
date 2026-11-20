from __future__ import annotations

import csv
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


TAXA_CONTRATUAL_TOTAL = 2000.00
MAX_PARCELAS_CONTRATO = 5


def ler_inteiro_intervalo(mensagem: str, minimo: int, maximo: int) -> int:
    """Lê e valida um número inteiro dentro de um intervalo fechado."""
    while True:
        valor_str = input(mensagem).strip()
        try:
            valor = int(valor_str)
            if minimo <= valor <= maximo:
                return valor
            print(f"Erro: informe um número inteiro entre {minimo} e {maximo}.")
        except ValueError:
            print("Erro: entrada inválida. Digite apenas números inteiros.")


def ler_sim_nao(mensagem: str) -> bool:
    """Lê resposta sim/não (s/n) e retorna True para sim, False para não."""
    while True:
        resp = input(mensagem).strip().lower()
        if resp in ("s", "sim"):
            return True
        if resp in ("n", "nao", "não"):
            return False
        print("Erro: responda com 's' (sim) ou 'n' (não).")


@dataclass
class Imovel(ABC):
    """Classe base que representa um imóvel da R.M Imóveis."""

    categoria: str
    aluguel_base: float
    quartos: int

    @abstractmethod
    def calcular_adicional_quartos(self) -> float:
        """Retorna o valor adicional referente à quantidade de quartos."""

    @abstractmethod
    def calcular_adicional_estacionamento(self) -> float:
        """Retorna o valor adicional referente a garagem ou estacionamento."""

    @abstractmethod
    def descricao_estacionamento(self) -> str:
        """Retorna a descrição legível da regra de estacionamento aplicada."""

    def valor_bruto_aluguel(self) -> float:
        """Soma aluguel base, adicional de quartos e estacionamento."""
        return (
            self.aluguel_base
            + self.calcular_adicional_quartos()
            + self.calcular_adicional_estacionamento()
        )


@dataclass
class Apartamento(Imovel):
    """Representa um apartamento (1 ou 2 quartos e opcionalmente 1 vaga)."""

    possui_garagem: bool = False
    ADICIONAL_2_QUARTOS = 200.00
    VALOR_GARAGEM = 300.00

    def calcular_adicional_quartos(self) -> float:
        return self.ADICIONAL_2_QUARTOS if self.quartos == 2 else 0.0

    def calcular_adicional_estacionamento(self) -> float:
        return self.VALOR_GARAGEM if self.possui_garagem else 0.0

    def descricao_estacionamento(self) -> str:
        if self.possui_garagem:
            return f"1 vaga de garagem (R$ {self.VALOR_GARAGEM:.2f})"
        return "Sem vaga de garagem (R$ 0,00)"


@dataclass
class Casa(Imovel):
    """Representa uma casa (1 ou 2 quartos e opcionalmente 1 vaga)."""

    possui_garagem: bool = False
    ADICIONAL_2_QUARTOS = 250.00
    VALOR_GARAGEM = 300.00

    def calcular_adicional_quartos(self) -> float:
        return self.ADICIONAL_2_QUARTOS if self.quartos == 2 else 0.0

    def calcular_adicional_estacionamento(self) -> float:
        return self.VALOR_GARAGEM if self.possui_garagem else 0.0

    def descricao_estacionamento(self) -> str:
        if self.possui_garagem:
            return f"1 vaga de garagem (R$ {self.VALOR_GARAGEM:.2f})"
        return "Sem vaga de garagem (R$ 0,00)"


@dataclass
class Estudio(Imovel):
    """Representa um estúdio com pacote de 2 vagas e vagas adicionais."""

    total_vagas: int = 0
    PACOTE_2_VAGAS = 250.00
    VAGA_ADICIONAL = 60.00

    def calcular_adicional_quartos(self) -> float:
        return 0.0

    def calcular_adicional_estacionamento(self) -> float:
        if self.total_vagas <= 0:
            return 0.0
        if self.total_vagas <= 2:
            return self.PACOTE_2_VAGAS
        extras = self.total_vagas - 2
        return self.PACOTE_2_VAGAS + (extras * self.VAGA_ADICIONAL)

    def descricao_estacionamento(self) -> str:
        if self.total_vagas <= 0:
            return "Sem vagas de estacionamento (R$ 0,00)"
        if self.total_vagas <= 2:
            return (
                f"Pacote inicial de até 2 vagas ({self.total_vagas} vaga(s)) - "
                f"R$ {self.PACOTE_2_VAGAS:.2f}"
            )
        extras = self.total_vagas - 2
        return (
            f"Pacote 2 vagas (R$ {self.PACOTE_2_VAGAS:.2f}) + "
            f"{extras} vaga(s) adicional(is) x R$ {self.VAGA_ADICIONAL:.2f}"
        )


class OrcamentoLocacao:
    """Consolida regras comerciais, resumo do orçamento e projeção de 12 meses."""

    DESCONTO_APARTAMENTO_SEM_CRIANCA = 0.05

    def __init__(
        self,
        imovel: Imovel,
        possui_criancas: bool,
        parcelas_contrato: int,
    ) -> None:
        if not (1 <= parcelas_contrato <= MAX_PARCELAS_CONTRATO):
            raise ValueError("Parcelas do contrato devem estar entre 1 e 5.")
        self.imovel = imovel
        self.possui_criancas = possui_criancas
        self.parcelas_contrato = parcelas_contrato

    def elegivel_desconto_apartamento(self) -> bool:
        return isinstance(self.imovel, Apartamento) and not self.possui_criancas

    def valor_desconto_mensal(self) -> float:
        if self.elegivel_desconto_apartamento():
            return round(
                self.imovel.valor_bruto_aluguel() * self.DESCONTO_APARTAMENTO_SEM_CRIANCA,
                2,
            )
        return 0.0

    def aluguel_mensal_final(self) -> float:
        return round(
            self.imovel.valor_bruto_aluguel() - self.valor_desconto_mensal(),
            2,
        )

    def valor_parcela_contrato(self) -> float:
        return round(TAXA_CONTRATUAL_TOTAL / self.parcelas_contrato, 2)

    def gerar_projecao_12_meses(self) -> list[dict[str, str | int | float]]:
        """Retorna lista de dicionários com a projeção mensal para 12 meses."""
        aluguel = self.aluguel_mensal_final()
        parcela_taxa = self.valor_parcela_contrato()
        linhas: list[dict[str, str | int | float]] = []

        for mes in range(1, 13):
            taxa_no_mes = parcela_taxa if mes <= self.parcelas_contrato else 0.0
            total_previsto = round(aluguel + taxa_no_mes, 2)
            linhas.append(
                {
                    "mes": mes,
                    "aluguel_mensal": f"{aluguel:.2f}",
                    "parcela_taxa_contratual": f"{taxa_no_mes:.2f}",
                    "total_previsto_mes": f"{total_previsto:.2f}",
                }
            )
        return linhas

    def exportar_csv(self, caminho_arquivo: str) -> Path:
        """Grava a projeção dos 12 meses em um arquivo CSV."""
        caminho = Path(caminho_arquivo)
        if caminho.suffix.lower() != ".csv":
            caminho = caminho.with_suffix(".csv")

        campos = [
            "mes",
            "aluguel_mensal",
            "parcela_taxa_contratual",
            "total_previsto_mes",
        ]
        dados = self.gerar_projecao_12_meses()

        with caminho.open(mode="w", newline="", encoding="utf-8") as arquivo_csv:
            escritor = csv.DictWriter(arquivo_csv, fieldnames=campos, delimiter=";")
            escritor.writeheader()
            escritor.writerows(dados)

        return caminho.resolve()

    def exibir_resumo(self) -> None:
        """Exibe o detalhamento completo do orçamento e da taxa contratual."""
        add_quartos = self.imovel.calcular_adicional_quartos()
        add_estac = self.imovel.calcular_adicional_estacionamento()
        desconto = self.valor_desconto_mensal()
        aluguel_final = self.aluguel_mensal_final()
        parcela_taxa = self.valor_parcela_contrato()

        print("\n" + "=" * 54)
        print("RENTSMART — RESUMO DO ORÇAMENTO (R.M IMÓVEIS)")
        print("=" * 54)
        print(f"Categoria do imóvel : {self.imovel.categoria}")
        if isinstance(self.imovel, (Apartamento, Casa)):
            print(f"Quantidade de quartos: {self.imovel.quartos}")
        print(f"Aluguel-base        : R$ {self.imovel.aluguel_base:.2f}")
        print(f"Adicional quartos   : R$ {add_quartos:.2f}")
        print(f"Estacionamento      : {self.imovel.descricao_estacionamento()}")
        print(f"Desconto (5% apto)  : - R$ {desconto:.2f}")
        print("-" * 54)
        print(f"ALUGUEL MENSAL FINAL: R$ {aluguel_final:.2f}")
        print("-" * 54)
        print("TAXA CONTRATUAL (CUSTO SEPARADO DO ALUGUEL MENSAL)")
        print(f"Valor total da taxa : R$ {TAXA_CONTRATUAL_TOTAL:.2f}")
        print(
            f"Parcelamento        : {self.parcelas_contrato}x de R$ {parcela_taxa:.2f}"
        )
        print("=" * 54)


def coletar_imovel() -> Imovel:
    """Solicita ao usuário os dados do imóvel e instancia a classe adequada."""
    print("\nEscolha a categoria do imóvel:")
    print("1 - Apartamento (base R$ 700,00)")
    print("2 - Casa (base R$ 900,00)")
    print("3 - Estúdio (base R$ 1.200,00)")
    opcao = ler_inteiro_intervalo("Opção (1 a 3): ", 1, 3)

    if opcao == 1:
        quartos = ler_inteiro_intervalo("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja incluir 1 vaga de garagem (+R$ 300,00)? (s/n): ")
        return Apartamento(
            categoria="Apartamento",
            aluguel_base=700.00,
            quartos=quartos,
            possui_garagem=garagem,
        )

    if opcao == 2:
        quartos = ler_inteiro_intervalo("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja incluir 1 vaga de garagem (+R$ 300,00)? (s/n): ")
        return Casa(
            categoria="Casa",
            aluguel_base=900.00,
            quartos=quartos,
            possui_garagem=garagem,
        )

    vagas = ler_inteiro_intervalo(
        "Quantidade total de vagas de estacionamento (0 a 10): ", 0, 10
    )
    return Estudio(
        categoria="Estúdio",
        aluguel_base=1200.00,
        quartos=1,
        total_vagas=vagas,
    )


def main() -> None:
    print("=== RentSmart — Sistema de Orçamento de Locação (R.M Imóveis) ===")
    imovel = coletar_imovel()

    possui_criancas = ler_sim_nao("O cliente possui crianças? (s/n): ")
    parcelas = ler_inteiro_intervalo(
        f"Em quantas parcelas deseja pagar a taxa contratual de R$ {TAXA_CONTRATUAL_TOTAL:.2f} "
        f"(1 a {MAX_PARCELAS_CONTRATO})? ",
        1,
        MAX_PARCELAS_CONTRATO,
    )

    orcamento = OrcamentoLocacao(
        imovel=imovel,
        possui_criancas=possui_criancas,
        parcelas_contrato=parcelas,
    )
    orcamento.exibir_resumo()

    nome_csv = input(
        "\nNome do arquivo CSV para projeção de 12 meses [projecao_12_meses.csv]: "
    ).strip()
    if not nome_csv:
        nome_csv = "projecao_12_meses.csv"

    caminho_gerado = orcamento.exportar_csv(nome_csv)
    print(f"Arquivo CSV gerado com sucesso em: {caminho_gerado}")


if __name__ == "__main__":
    main()
