# RentSmart — Sistema de Orcamento de Locacão (R.M Imoveis)

<img width="1408" height="768" alt="Gemini_Generated_Image_fqymf8fqymf8fqym (1)" src="https://github.com/user-attachments/assets/7e7681bb-615a-48f8-bbac-89a4fd30267b" />


Aplicação desenvolvida em **Python** aplicando **Pensamento Algorítmico** e **Programação Orientada a Objetos (POO)** para automatizar o cálculo de orçamentos de locação da imobiliária **R.M Imóveis**.

## Sobre o Projeto

Com o crescimento da carteira de imóveis e do volume de atendimentos da **R.M Imóveis**, o cálculo manual de orçamentos passou a gerar lentidão e risco de erros na aplicação de adicionais, descontos e condições contratuais.

O **RentSmart** resolve esse problema permitindo que o atendente informe as características da locação via terminal, validando os dados inseridos, aplicando automaticamente todas as regras comerciais, exibindo um resumo detalhado do orçamento e exportando a projeção financeira dos **12 primeiros meses** em formato **CSV**.

## Regras de Negócio Implementadas

| Categoria | Aluguel-Base (1 quarto) | Adicional 2 Quartos | Estacionamento / Garagem | 
| ----- | ----- | ----- | ----- | 
| **Apartamento** | R\$ 700,00 | \+ R\$ 200,00 | \+ R\$ 300,00 (1 vaga) | 
| **Casa** | R\$ 900,00 | \+ R\$ 250,00 | \+ R\$ 300,00 (1 vaga) | 
| **Estúdio** | R\$ 1.200,00 | Não se aplica | Pacote até 2 vagas: R\$ 250,00  Vaga adicional: + R\$ 60,00 cada | 

### Condições Adicionais

* **Desconto Comercial (Apartamento):** clientes que optarem por **apartamento** e informarem **não possuir crianças** recebem **5% de desconto** sobre o valor mensal do aluguel (calculado após a soma dos adicionais).

* **Taxa Contratual:** valor fixo de **R\$ 2.000,00**, parcelável em **1x a 5x**, exibido separadamente do aluguel mensal para maior transparência ao cliente.

* **Projeção Anual (CSV):** geração automática de arquivo `.csv` detalhando mês a mês o valor do aluguel, a parcela da taxa contratual (nos meses vigentes) e o custo total previsto para o primeiro ano de contrato.

## Arquitetura e Orientação a Objetos

O sistema foi estruturado separando responsabilidades em classes coesas para evitar duplicação de lógica e facilitar futuras manutenções:

* **`Imovel` (Classe Abstrata Base):** define os atributos comuns (`categoria`, `aluguel_base`, `quartos`) e a interface para cálculo de adicionais e valor bruto do aluguel.

* **`Apartamento` e `Casa`:** herdam de `Imovel` e especializam as regras de adicional para 2 quartos e inclusão de 1 vaga de garagem.

* **`Estudio`:** herda de `Imovel` e implementa a regra específica de pacote de 2 vagas de estacionamento e cobrança por vagas extras.

* **`OrcamentoLocacao`:** orquestra as regras comerciais do cliente (elegibilidade ao desconto de 5%, parcelamento da taxa contratual de R\$ 2.000,00), exibe o resumo formatado e gera o arquivo `.csv` de 12 meses.

## Estrutura de Arquivos

```
rentsmart/
├── rentsmart.py           # Código-fonte principal da aplicação
├── projecao_12_meses.csv  # Arquivo gerado após a execução de um orçamento
└── README.md              # Documentação do projeto

```

## Como Executar o Projeto

### Pré-requisitos

* **Python 3.10** ou superior instalado.

* Não há necessidade de instalar pacotes externos (o projeto utiliza apenas módulos nativos da biblioteca padrão do Python: `abc`, `csv`, `dataclasses` e `pathlib`).

### Passo a Passo

1. Clone este repositório para sua máquina:

   
   git clone https://github.com/Kaaraujo27/RentSmart-Sistema-de-Or-amento-de-Loca-o-com-Python-e-Orienta-o-a-Objetos.git

   cd rentsmart
   
   

3. Execute o programa no terminal:

   ```
   python rentsmart.py
   
   ```

   *(No Linux ou macOS, caso necessário, utilize `python3 rentsmart.py`.)*

4. Preencha as informações solicitadas no menu interativo:

   * Categoria do imóvel (`1` Apartamento, `2` Casa ou `3` Estúdio);

   * Quantidade de quartos ou vagas de estacionamento;

   * Se o cliente possui crianças (`s` ou `n`);

   * Quantidade de parcelas da taxa contratual (`1` a `5`);

   * Nome desejado para o arquivo `.csv` de saída.

## Exemplo de Saída

### Resumo no Terminal

```
======================================================
RENTSMART — RESUMO DO ORÇAMENTO (R.M IMÓVEIS)
======================================================
Categoria do imóvel : Apartamento
Quantidade de quartos: 2
Aluguel-base        : R$ 700.00
Adicional quartos   : R$ 200.00
Estacionamento      : 1 vaga de garagem (R$ 300.00)
Desconto (5% apto)  : - R$ 60.00
------------------------------------------------------
ALUGUEL MENSAL FINAL: R$ 1140.00
------------------------------------------------------
TAXA CONTRATUAL (CUSTO SEPARADO DO ALUGUEL MENSAL)
Valor total da taxa : R$ 2000.00
Parcelamento        : 4x de R$ 500.00
======================================================

```

### Arquivo CSV Gerado (`projecao_12_meses.csv`)

| mes | aluguel_mensal | parcela_taxa_contratual | total_previsto_mes | 
| ----- | ----- | ----- | ----- | 
| 1 | 1140.00 | 500.00 | 1640.00 | 
| 2 | 1140.00 | 500.00 | 1640.00 | 
| 3 | 1140.00 | 500.00 | 1640.00 | 
| 4 | 1140.00 | 500.00 | 1640.00 | 
| 5 | 1140.00 | 0.00 | 1140.00 | 
| ... | ... | ... | ... | 
| 12 | 1140.00 | 0.00 | 1140.00 | 

## Autor

Desenvolvido como projeto da disciplina **Algorithmic Thinking & Introduction to Object-Oriented Programming**.

Kayque Araujo Rosario
