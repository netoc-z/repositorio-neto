"""Sistema Kelp - controle de produtos, pedidos e estoque (Python 3.10+)."""
import argparse
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

DB_PADRAO = Path(__file__).with_name('kelp.db')


def centavos(valor):
    try:
        d = Decimal(str(valor).replace(',', '.'))
    except InvalidOperation as exc:
        raise ValueError('Preço inválido.') from exc
    if not d.is_finite() or d < 0:
        raise ValueError('O preço deve ser um número não negativo.')
    return int((d * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def moeda(c):
    return f'R$ {c / 100:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


@contextmanager
def conexao(db=DB_PADRAO):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def iniciar(db=DB_PADRAO):
    with conexao(db) as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS produtos (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nome TEXT NOT NULL CHECK(length(trim(nome)) > 0),
          categoria TEXT NOT NULL DEFAULT '',
          tamanho TEXT NOT NULL DEFAULT '',
          preco_centavos INTEGER NOT NULL CHECK(preco_centavos >= 0),
          estoque INTEGER NOT NULL CHECK(estoque >= 0),
          ativo INTEGER NOT NULL DEFAULT 1 CHECK(ativo IN (0,1))
        );
        CREATE TABLE IF NOT EXISTS pedidos (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          cliente TEXT NOT NULL CHECK(length(trim(cliente)) > 0),
          criado_em TEXT NOT NULL,
          total_centavos INTEGER NOT NULL CHECK(total_centavos >= 0)
        );
        CREATE TABLE IF NOT EXISTS itens_pedido (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
          produto_id INTEGER NOT NULL REFERENCES produtos(id),
          quantidade INTEGER NOT NULL CHECK(quantidade > 0),
          preco_unitario_centavos INTEGER NOT NULL CHECK(preco_unitario_centavos >= 0),
          subtotal_centavos INTEGER NOT NULL CHECK(subtotal_centavos >= 0)
        );
        ''')


def cadastrar_produto(nome, categoria, tamanho, preco, estoque, db=DB_PADRAO):
    nome = nome.strip()
    if not nome:
        raise ValueError('Informe o nome do produto.')
    if type(estoque) is not int or estoque < 0:
        raise ValueError('Estoque deve ser inteiro não negativo.')
    with conexao(db) as c:
        cur = c.execute('INSERT INTO produtos(nome,categoria,tamanho,preco_centavos,estoque) VALUES (?,?,?,?,?)',
                        (nome, categoria.strip(), tamanho.strip(), centavos(preco), estoque))
        return cur.lastrowid


def listar_produtos(db=DB_PADRAO):
    with conexao(db) as c:
        return [dict(r) for r in c.execute('SELECT * FROM produtos WHERE ativo=1 ORDER BY id')]


def repor_estoque(produto_id, quantidade, db=DB_PADRAO):
    if type(quantidade) is not int or quantidade <= 0:
        raise ValueError('A reposição deve ser um inteiro positivo.')
    with conexao(db) as c:
        cur = c.execute('UPDATE produtos SET estoque=estoque+? WHERE id=? AND ativo=1', (quantidade, produto_id))
        if cur.rowcount != 1:
            raise ValueError('Produto não encontrado.')


def registrar_venda(cliente, itens, db=DB_PADRAO):
    """itens: lista de tuplas (produto_id, quantidade). Operação atômica."""
    cliente = cliente.strip()
    if not cliente:
        raise ValueError('Informe o nome do cliente.')
    if not itens:
        raise ValueError('O pedido precisa ter pelo menos um item.')
    agregados = {}
    for pid, qtd in itens:
        if type(pid) is not int or type(qtd) is not int or pid <= 0 or qtd <= 0:
            raise ValueError('Produto e quantidade devem ser inteiros positivos.')
        agregados[pid] = agregados.get(pid, 0) + qtd
    with conexao(db) as c:
        linhas = []
        for pid, qtd in agregados.items():
            p = c.execute('SELECT * FROM produtos WHERE id=? AND ativo=1', (pid,)).fetchone()
            if p is None:
                raise ValueError(f'Produto {pid} não encontrado.')
            if p['estoque'] < qtd:
                raise ValueError(f'Estoque insuficiente para {p["nome"]}: disponível {p["estoque"]}.')
            linhas.append((pid, qtd, p['preco_centavos'], qtd * p['preco_centavos']))
        total = sum(l[3] for l in linhas)
        cur = c.execute('INSERT INTO pedidos(cliente,criado_em,total_centavos) VALUES (?,?,?)',
                        (cliente, datetime.now().isoformat(timespec='seconds'), total))
        pedido_id = cur.lastrowid
        for pid, qtd, preco, subtotal in linhas:
            c.execute('UPDATE produtos SET estoque=estoque-? WHERE id=?', (qtd, pid))
            c.execute('INSERT INTO itens_pedido(pedido_id,produto_id,quantidade,preco_unitario_centavos,subtotal_centavos) VALUES (?,?,?,?,?)',
                      (pedido_id, pid, qtd, preco, subtotal))
        return pedido_id, total


def listar_pedidos(db=DB_PADRAO):
    with conexao(db) as c:
        pedidos = [dict(r) for r in c.execute('SELECT * FROM pedidos ORDER BY id DESC')]
        for pedido in pedidos:
            pedido['itens'] = [dict(r) for r in c.execute('''SELECT i.*, p.nome AS produto_nome
                FROM itens_pedido i JOIN produtos p ON p.id=i.produto_id
                WHERE i.pedido_id=? ORDER BY i.id''', (pedido['id'],))]
        return pedidos


def ler_inteiro(mensagem, minimo=0):
    try:
        n = int(input(mensagem).strip())
    except ValueError as exc:
        raise ValueError('Digite um número inteiro.') from exc
    if n < minimo:
        raise ValueError(f'O valor mínimo é {minimo}.')
    return n


def mostrar_produtos(db):
    produtos = listar_produtos(db)
    if not produtos:
        print('Nenhum produto cadastrado.')
    for p in produtos:
        print(f'#{p["id"]} | {p["nome"]} | {p["categoria"]} | Tam. {p["tamanho"]} | '
              f'{moeda(p["preco_centavos"])} | Estoque: {p["estoque"]}')


def menu(db):
    iniciar(db)
    while True:
        print('\n=== LOJA KELP ===')
        print('1 - Cadastrar produto\n2 - Listar produtos\n3 - Repor estoque\n4 - Registrar venda\n5 - Histórico de pedidos\n0 - Sair')
        opcao = input('Opção: ').strip()
        try:
            if opcao == '1':
                nome = input('Nome: ')
                categoria = input('Categoria: ')
                tamanho = input('Tamanho: ')
                preco = input('Preço (ex.: 59,90): ')
                estoque = ler_inteiro('Estoque inicial: ')
                pid = cadastrar_produto(nome, categoria, tamanho, preco, estoque, db)
                print(f'Produto cadastrado com ID {pid}.')
            elif opcao == '2':
                mostrar_produtos(db)
            elif opcao == '3':
                mostrar_produtos(db)
                pid = ler_inteiro('ID do produto: ', 1)
                qtd = ler_inteiro('Quantidade a adicionar: ', 1)
                repor_estoque(pid, qtd, db)
                print('Estoque atualizado.')
            elif opcao == '4':
                mostrar_produtos(db)
                cliente = input('Nome do cliente: ')
                itens = []
                while True:
                    pid = ler_inteiro('ID do produto (0 para finalizar): ')
                    if pid == 0:
                        break
                    qtd = ler_inteiro('Quantidade: ', 1)
                    itens.append((pid, qtd))
                pedido_id, total = registrar_venda(cliente, itens, db)
                print(f'Pedido #{pedido_id} registrado. Total: {moeda(total)}')
            elif opcao == '5':
                pedidos = listar_pedidos(db)
                if not pedidos:
                    print('Nenhum pedido registrado.')
                for p in pedidos:
                    print(f'Pedido #{p["id"]} | {p["cliente"]} | {p["criado_em"]} | {moeda(p["total_centavos"])}')
                    for item in p['itens']:
                        print(f'  - {item["produto_nome"]} x{item["quantidade"]} = {moeda(item["subtotal_centavos"])}')
            elif opcao == '0':
                print('Até logo!')
                return
            else:
                print('Opção inválida.')
        except ValueError as exc:
            print(f'Erro: {exc}')
        except (KeyboardInterrupt, EOFError):
            print('\nOperação interrompida.')
            return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sistema de estoque e vendas da Loja Kelp')
    parser.add_argument('--db', type=Path, default=DB_PADRAO, help='Caminho do banco SQLite')
    args = parser.parse_args()
    menu(args.db)
