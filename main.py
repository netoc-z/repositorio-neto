"""Protótipo inicial para calcular o total de um pedido da loja Kelp."""


def ler_inteiro_positivo(mensagem):
    """Lê um número inteiro maior que zero."""
    while True:
        try:
            valor = int(input(mensagem))
            if valor > 0:
                return valor
            print("Digite um número maior que zero.")
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_preco(mensagem):
    """Lê um preço não negativo, aceitando vírgula ou ponto decimal."""
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor >= 0:
                return valor
            print("O preço não pode ser negativo.")
        except ValueError:
            print("Digite um preço válido, como 35,00.")


def calcular_total(itens):
    """Soma quantidade vezes preço unitário para cada item."""
    return sum(item["quantidade"] * item["preco_unitario"] for item in itens)


def registrar_pedido():
    itens = []
    print("\nRegistro de pedido - Loja Kelp")

    while True:
        nome = input("Nome do produto (ou ENTER para finalizar): ").strip()
        if not nome:
            if itens:
                break
            print("Adicione pelo menos um produto ao pedido.")
            continue

        quantidade = ler_inteiro_positivo("Quantidade: ")
        preco = ler_preco("Preço unitário (R$): ")
        itens.append({"nome": nome, "quantidade": quantidade, "preco_unitario": preco})
        print(f"Subtotal do item: R$ {quantidade * preco:.2f}")

    total = calcular_total(itens)
    print("\nResumo do pedido")
    for item in itens:
        subtotal = item["quantidade"] * item["preco_unitario"]
        print(f"- {item['nome']}: {item['quantidade']} x R$ {item['preco_unitario']:.2f} = R$ {subtotal:.2f}")
    print(f"Total do pedido: R$ {total:.2f}")


def main():
    print("=== Sistema inicial da Loja Kelp ===")
    registrar_pedido()
    print("\nFim do programa.")


if __name__ == "__main__":
    main()
