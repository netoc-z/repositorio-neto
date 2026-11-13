# Sistema de Gestão da Loja Kelp

Projeto Integrado do curso de Análise e Desenvolvimento de Sistemas. O sistema apoia o cadastro de produtos, o controle de estoque, o registro de vendas e a consulta ao histórico de pedidos da loja Kelp.

## Integrantes

- Kelly Santos Vieira
- Gabriel Vinicius Pereira
- Arlindo Ferreira
- Pedro Henrique

## Problema

Controles manuais ou planilhas dispersas podem dificultar a consulta de produtos e pedidos, favorecer erros e atrasar o atendimento. O projeto propõe organizar essas operações em um programa simples.

## Funcionalidades atuais

- Cadastrar produtos com nome, categoria, tamanho, preço e estoque inicial.
- Listar produtos ativos.
- Repor estoque.
- Registrar uma venda com um ou mais itens.
- Calcular o total e reduzir o estoque após a venda.
- Consultar o histórico de pedidos e seus itens.
- Salvar produtos, vendas e estoque em um banco SQLite local.

O nome do cliente fica associado ao pedido. Esta versão ainda não tem cadastro separado de clientes, login de funcionários, status dos pedidos ou interface gráfica.

## Tecnologias

- Python 3.10 ou superior
- SQLite, pela biblioteca padrão do Python

## Como executar

Abra um terminal nesta pasta e execute:

```bash
python kelp.py
```

No Windows, também pode funcionar:

```bash
py kelp.py
```

O programa cria `kelp.db` automaticamente na primeira execução. Esse arquivo guarda os dados locais e não é necessário para executar o sistema; o código recria a estrutura do banco.

## Como usar

1. Escolha `1` para cadastrar um produto.
2. Escolha `2` para listar os produtos e consultar seus IDs.
3. Escolha `3` para repor estoque.
4. Escolha `4` para registrar uma venda. Informe os IDs e quantidades dos produtos; digite `0` quando terminar de incluir itens.
5. Escolha `5` para consultar o histórico de pedidos.
6. Escolha `0` para sair.

## Integração das disciplinas

| Disciplina | Aplicação no sistema |
|---|---|
| Linguagem de Programação | Python, funções, entrada e saída, módulos e SQLite |
| Algoritmos e Programação Estruturada | Menu com seleção, repetição, validação e funções separadas |
| Matemática Computacional | Preços em centavos, subtotais, total da venda e atualização do estoque |

## Continuidade do projeto

A linha de base anterior incluiu o levantamento do problema e dos requisitos, a modelagem do banco de dados e os protótipos das telas. O avanço de 2026/2 é a implementação inicial em Python com persistência local, controle de estoque, vendas e histórico.

`kelp.py` é a versão principal atual. `main.py` permanece no repositório como protótipo simples anterior, usado para demonstrar o cálculo de um pedido.
