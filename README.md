# Gerenciador de Gastos

#### Link do projeto: https://gerenciador-gastos-n70s.onrender.com/

## Descrição do Problema

Já se perdeu nos gastos no meio do mês? Ou então não soube para onde seu dinheiro estava indo? Esse é um problema comum, e é exatamente o que o projeto busca solucionar, a falta de controle financeiro.

## Proposta da Solução

A solução propõe um gerenciador de gastos que funciona de maneira simples: Você insere o valor gasto, a data, uma descrição e a categoria, e pronto, o registro está feito.
O projeto é direto ao ponto, para atingir uma solução rápida e ágil para esses problemas.

## Público-alvo

O projeto visa alcançar aqueles que querem atingir um maior nível de controle financeiro, voltado especialmente jovens que começaram a morar sozinhos e recém atingiram sua independência financeira.

## Funcionalidades
- Registrar gasto (com valor, data, descrição e categoria)
- Listar gastos
- Editar gastos
- Excluir gastos

## Tecnologias utilizadas
- Python 3.13
- Flask 3.1.2
- SQLAlchemy 3.1.1
- SQLite

## Instruções de uso

Clone o repositório
```
    git clone https://github.com/luiskkjk/gerenciador_gastos.git
```

Crie e ative o ambiente virtual
```
    python -m venv .venv
    .venv\Scripts\activate # Windows
    source .venv/bin/activate # Linux
```

Instale as dependências
```
    pip install -r src/requirements.txt
```

Execute o projeto
```
    cd src
    python -m flask run

    Acesse em http://127.0.0.1:5000
```

### Instruções para o teste
```
    pytest tests/test_app.py
```

### Instruções para o ruff
```
    ruff check .
```

## Autor 

Luis Eduardo Borges - https://github.com/luiskkjk

## Repositório

https://github.com/luiskkjk/gerenciador_gastos

* Versão 2.6.6
