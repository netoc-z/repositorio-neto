# Sistema de Gestão da Loja Kelp

Projeto Integrado de Análise e Desenvolvimento de Sistemas. A proposta é apoiar o cadastro de produtos, o registro de pedidos e o controle do estoque da loja Kelp.

## Primeira versão

Este protótipo de terminal demonstra o cálculo do total de um pedido. O usuário informa produtos, quantidades e preços unitários; o programa valida os dados, calcula os subtotais e mostra o valor total.

## Disciplinas integradas

| Disciplina | Aplicação no projeto | Evidência inicial |
|---|---|---|
| Linguagem de Programação | Tipos numéricos, entrada e saída de dados, funções | `main.py` |
| Algoritmos e Programação Estruturada | Sequência, validação, decisão e repetição | Funções e laço do pedido em `main.py` |
| Matemática Computacional | Subtotal = quantidade × preço; total = soma dos subtotais | Função `calcular_total` e exemplo abaixo |

## Exemplo de cálculo

Um item com quantidade 2 e preço unitário R$ 35,00 tem subtotal de R$ 70,00. Outro item com quantidade 1 e preço unitário R$ 20,00 resulta em total do pedido de R$ 90,00.

## Como executar

Requer Python 3. Abra um terminal nesta pasta e execute:

```bash
python main.py
```

Este protótipo ainda não salva os dados depois que o programa é encerrado. Persistência, cadastro completo e integração com banco de dados ficam para as próximas etapas.
