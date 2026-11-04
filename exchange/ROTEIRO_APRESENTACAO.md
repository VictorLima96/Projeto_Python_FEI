# Exchange do Victor — como funciona e como apresentar

Projeto de CCP110 (Fundamentos de Algoritmos) — exchange de criptomoedas em Python, via console, com os dados salvos em `.txt`.

---

## 1. Como rodar

```bash
cd C:\Users\vitue\Documents\Projeto_FEI\exchange
python exchange.py
```

Se você apagar a pasta `dados`, o programa **recria** ela com um investidor de teste:

| CPF | Senha | Nome |
| --- | --- | --- |
| `12345678900` | `123456` | Victor Lima |
| `98765432100` | `654321` | Maria Souza |

---

## 2. Estrutura do projeto

```text
exchange/
  exchange.py            -> o programa principal: só menus e navegação
  funcoes.py             -> as regras: arquivo, login, saldo, extrato, compra, venda
  dados/
    investidores.txt     -> quem tem conta e quanto tem de cada moeda
    moedas.txt           -> cotação e taxas de cada moeda
    extrato.txt          -> histórico de todas as operações
```

**Por que dois arquivos `.py`?** O `exchange.py` só decide *o que mostrar*; o `funcoes.py` só decide *o que fazer*. Isso é o conteúdo de módulos da aula 13 (`import funcoes`) e deixa o código legível para explicar no vídeo.

### O que tem dentro de cada `.txt`

**`investidores.txt`** — uma linha por investidor:

```text
cpf;nome;senha;reais;btc;eth;xrp
12345678900;Victor Lima;123456;1000.00;0.00000000;0.00000000;0.00
```

**`moedas.txt`** — uma linha por moeda:

```text
nome;cotacao;taxa_compra;taxa_venda
BTC;350000.00;0.0200;0.0300
```

**`extrato.txt`** — uma linha por operação (só cresce, nunca é reescrito):

```text
cpf;data;hora;sinal;valor;moeda;cotacao;taxa;reais;btc;eth;xrp
12345678900;31-10-2026;11:13;+;500.00000000;REAL;0.00;0.00;1500.00;0.00000000;0.000000;0.00
```

O separador é `;` porque nome e data nunca têm ponto e vírgula. Na leitura eu uso `split(";")` e converto cada campo com `float()`.

---

## 3. Como cada coisa funciona (para você explicar)

### 3.1 Login

```text
CPF (só os 11 números) -> valida len(cpf) == 11 e cpf.isdigit()
Senha (6 dígitos)      -> valida len(senha) == 6 e senha.isdigit()
```

O CPF é a **chave** do dicionário `investidores`. Se `cpf in investidores` e a senha bater, o login retorna o CPF; senão, oferece "Tentar novamente? (S/N)".
Cada validação tem **3 tentativas** — se o usuário digitar lixo 3 vezes, volta ao menu em vez de travar o programa.

### 3.2 Saldo

Pede a senha de novo (a função `confirmar_senha`, com 3 tentativas) e mostra `mostrar_saldos`: nome, CPF com máscara e as 4 posições da carteira.

A carteira é um dicionário dentro do dicionário:

```python
investidores["12345678900"]["carteira"]
# {"REAL": 1000.0, "BTC": 0.0, "ETH": 0.0, "XRP": 0.0}
```

### 3.3 Extrato

Lê o `extrato.txt` linha por linha e **filtra pelo CPF**. Cada linha vira uma operação:

| Coluna | Significado |
| --- | --- |
| data / hora | momento da operação (`datetime.now()`) |
| sinal | `+` entrou, `-` saiu |
| valor | quantidade movimentada (reais em depósito/saque, moeda em compra/venda) |
| moeda | `REAL`, `BTC`, `ETH` ou `XRP` |
| CT | cotação usada na operação (0 em depósito/saque) |
| TX | **taxa cobrada em reais** (0 em depósito/saque) |
| REAL/BTC/ETH/XRP | saldo **depois** da operação |

> ⚠️ **Ponto para o vídeo:** o exemplo no slide do professor não fecha na conta (ele mostra `+ 100.00 XRP` com `CT: 2.57` e o saldo caindo 101 reais, o que daria 38,9 XRP). Eu escolhi uma convenção única e mantive em todo o programa — diga isso se perguntarem: *"padronizei a coluna valor como a quantidade movimentada e a TX como a taxa em reais, porque o exemplo do enunciado é inconsistente entre as linhas."*

### 3.4 Depósito e saque

Depósito soma em `carteira["REAL"]`. Saque subtrai, mas **antes** confere:

```python
if valor > carteira["REAL"]:
    print("Saldo insuficiente!...")
    return
```

Sempre registra no extrato e chama `salvar_investidores()` — ou seja, grava no `.txt` **na hora**, não só no "Sair".

### 3.5 Compra (a conta que o professor vai conferir)

O usuário digita **quanto quer gastar em reais**. A taxa é cobrada **por cima**:

```text
valor_investido = 100.00
taxa            = 100.00 * 2%  = 2.00
total debitado  = 102.00

quantidade      = 100.00 / 350000 = 0.00028571 BTC
```

Validação: `if total > carteira["REAL"]` → recusa. Depois:

```python
carteira["REAL"] -= total
carteira["BTC"] += quantidade
```

### 3.6 Venda

O usuário digita **a quantidade da moeda**. A taxa sai do valor bruto:

```text
quantidade = 0.00028571 BTC
bruto      = 0.00028571 * 350000 = 99.9985
taxa       = 99.9985 * 3%        = 3.00
recebe     = 96.9985  ~ 97.00
```

Validação: não deixa vender mais do que tem (com folga de `0.00000001` por causa do arredondamento do `float`).

**Frase boa para o vídeo:** *"comprei por 100 e vendi de volta por 97: os 5% de diferença são as taxas de 2% na compra e 3% na venda. É assim que a exchange ganha."*

### 3.7 Atualizar cotação

```python
variacao = random.uniform(-0.05, 0.05)   # entre -5% e +5%
nova = round(antiga * (1 + variacao), 2)
```

Roda para **todas** as moedas, mostra `antes -> depois (variação %)` e salva no `moedas.txt`.
Se a conta der zero ou negativo (preço muito baixo), força `0.01`.

### 3.8 Persistência

- `"a"` (append) **só no extrato** — histórico nunca é apagado.
- `"w"` (write) em investidores e moedas — reescreve o estado completo.
- Tudo com `encoding="utf-8"` e `close()`.
- Se o `.txt` não existir, o programa cria. Se uma linha estiver corrompida, ele pula a linha em vez de quebrar.

---

## 4. Onde cada conceito de aula aparece

Use esta tabela se o professor perguntar "onde você usou X".

| Conceito | Aula | Onde está no código |
| --- | --- | --- |
| Variáveis, tipos, `input`/`print`, f-string, `%` | 01 | todo o projeto |
| Teste de mesa | 02 | as contas de compra/venda |
| `if`/`else`, validações | 03 | login, saldo insuficiente, quantidade inválida |
| `and`/`or`, `elif` | 04 | `len(cpf) == 11 and cpf.isdigit()`, menu |
| `while True` + `break` | 05 | menus e login |
| Repetição aninhada | 06 | percorrer moedas no extrato/cotação |
| Funções, `return`, parâmetros, escopo | 07 | 20 funções no `funcoes.py` |
| Listas, `append`, índice | 08 | linhas do extrato |
| `for`, list comprehension | 09 | montagem do extrato |
| `random.uniform` | 10 | atualização de cotação |
| Dicionários (`chave: valor`, `.items()`, `.get()`) | 11 | investidores, carteira, moedas |
| Arquivos `open`/`write`/`readlines`/`close` | 12 | os 3 `.txt` |
| Módulos, `if __name__ == "__main__"` | 13 | `exchange.py` importa `funcoes.py` |

**Conceitos que você adicionou além da aula** (conta ponto no critério "novos conceitos"): módulo próprio, caminho absoluto com `os.path` (`__file__`), tratamento de erro com `try/except`, `datetime` para data/hora, tolerância de `float` na venda, formatação por casas decimais por moeda.

---

## 5. Roteiro do vídeo (3 a 8 minutos)

> Grave a tela inteira, com o terminal e o Bloco de Notas lado a lado. Feche tudo que não for usar. Faça um ensaio cronometrado antes.

### Preparação (antes de gravar)

1. Deixe o projeto com os dados de teste originais (1000 reais, sem cripto) — apague `extrato.txt` e restaure `investidores.txt`.
2. Abra o Bloco de Notas com `dados\investidores.txt` e outra janela com `extrato.txt`.
3. Aumente a fonte do terminal (`Ctrl + scroll`).
4. Deixe o roteiro do lado, mas **não leia** — fale naturalmente.

### Roteiro minuto a minuto

| Tempo | O que mostrar | O que falar |
| --- | --- | --- |
| 0:00–0:30 | Pasta do projeto | "Esse é meu projeto de exchange de criptomoedas. Ele roda no console, em Python, e guarda tudo em arquivos `.txt` para não perder dados." |
| 0:30–1:00 | `exchange.py` e `funcoes.py` | "Separei em dois arquivos: um só com os menus e outro com as regras, usando módulos." |
| 1:00–1:40 | Login **errado** e depois **certo** | "O CPF tem que ter 11 números, sem pontos, e a senha 6 dígitos. Se errar, ele avisa e deixa tentar de novo." |
| 1:40–2:20 | Opção 1 (saldo) | "Pede a senha outra vez. Aparece nome, CPF e as quatro posições da carteira." |
| 2:20–2:55 | Opção 3 (depositar 500) | "Depositei 500." **Alt+Tab no `.txt`**: "e o arquivo já mudou, sem eu ter saído do programa." |
| 2:55–3:25 | Opção 4: sacar 100, depois sacar 99999 | "O saque não deixa o saldo ficar negativo — ele recusa." |
| 3:25–4:15 | Opção 5: comprar 100 em BTC | "Mostra a cotação e as taxas. Bitcoin cobra 2% na compra, então debita 102 e credita 0,00028571 BTC." |
| 4:15–4:50 | Opção 2: extrato | "Cada linha tem data, hora, sinal, valor, moeda, a cotação usada, a taxa e o saldo depois da operação." |
| 4:50–5:30 | Opção 6: vender tudo | "Aqui a taxa é 3%. Vendi por 97 o que comprei por 100 — a diferença é o lucro da exchange." |
| 5:30–6:00 | Opção 7: atualizar cotação | "As cotações variam com `random`, no máximo 5% para cima ou para baixo, e já são salvas." |
| 6:00–6:40 | Opção 8, fechar o programa, **abrir de novo** e logar | "Fechei e abri de novo: saldo, cripto e histórico continuam iguais, porque tudo está no `.txt`." |
| 6:40–7:00 | Encerramento | "Então o projeto cobre login, saldo, extrato, depósito, saque, compra, venda, cotação e persistência." |

### Números para usar (dão conta redonda)

| Passo | Resultado |
| --- | --- |
| Saldo inicial | R$ 1000,00 |
| Depositar 500 | R$ 1500,00 |
| Comprar 100 em BTC (cotação 350.000, taxa 2%) | debita R$ 102,00 → R$ 1398,00 e 0,00028571 BTC |
| Vender 0,00028571 BTC (taxa 3%) | recebe R$ 97,00 → R$ 1495,00 |

> Se você atualizar a cotação **antes** de vender, os números mudam. Faça a venda antes e deixe a atualização para o final.

---

## 6. Perguntas prováveis (e resposta curta)

**"Por que a carteira é um dicionário?"**
Porque o acesso é por nome (`carteira["BTC"]`) e não por posição. Se eu adicionar uma moeda nova, o código não muda de estrutura.

**"E se o programa fechar no meio de uma compra?"**
Cada operação grava no arquivo logo depois de alterar a memória. No pior caso, perde-se a operação que estava sendo digitada, nunca as anteriores.

**"Por que `"a"` no extrato e `"w"` nos outros?"**
`"w"` apaga o conteúdo do arquivo. No extrato isso destruiria o histórico, então uso `"a"`, que só acrescenta no fim.

**"Como você garante o limite de 5%?"**
`random.uniform(-0.05, 0.05)` gera um número entre −0,05 e 0,05, e eu multiplico por `(1 + variação)`.

**"Por que sobrou 0,00000001 de moeda?"**
Arredondamento de `float`. Por isso comparo com uma folga de `0.00000001` na venda e zero o resíduo quando ele é menor que isso.

**"Dá para fazer em dupla?"**
Sim, mas aí precisa do usuário administrador (cadastrar/excluir investidor e criptomoeda, consultar saldo/extrato de qualquer CPF). A estrutura atual já permite: é só acrescentar um `"tipo": "admin"` no dicionário e um menu novo.

---

## 7. Checklist antes de entregar

- [ ] Rodei o programa do zero (sem a pasta `dados`) e ele criou tudo
- [ ] Testei login errado, CPF com ponto e senha com letra
- [ ] Testei saque maior que o saldo
- [ ] Testei compra maior que o saldo
- [ ] Testei venda maior do que eu tenho
- [ ] Fechei e abri o programa e os dados continuaram
- [ ] O extrato tem as operações na ordem em que aconteceram
- [ ] Abri os `.txt` no Bloco de Notas e estão legíveis
- [ ] Relatório de 3 a 5 páginas escrito
- [ ] Vídeo de 3 a 8 minutos, público, com o link funcionando
- [ ] Códigos enviados no prazo do Moodle

---

## 8. Se quiser refazer o código você mesmo (ordem que funciona)

1. **Arquivos primeiro**: `criar_arquivos_iniciais`, `carregar_*` e `salvar_*`. Teste abrindo e fechando o programa com um `print` do dicionário.
2. **Login**: `pedir_cpf`, `pedir_senha`, `fazer_login`. Ainda sem menu.
3. **Menus**: `menu_investidor` com as 8 opções chamando funções vazias (`pass`). Isso já é a Entrega 1.
4. **Saldo + depósito + saque**: as três primeiras funções de verdade (Entrega 2).
5. **Extrato**: `registrar_extrato` e `consultar_extrato` (Entrega 3).
6. **Compra e venda**: as contas com taxa. Teste no papel antes (Entrega 3).
7. **Cotação**: `random.uniform` e `salvar_moedas` (Entrega 4).

Fazendo nessa ordem, cada etapa já é uma entrega parcial do Moodle.

---

## 9. Ajustes se for em dupla (ainda não implementado)

O que falta para a versão em dupla:

1. `investidores.txt` ganha uma coluna `tipo` (`investidor` / `admin`).
2. `login` devolve o tipo e o `main` escolhe qual menu abrir.
3. Funções novas: `cadastrar_investidor`, `excluir_investidor`, `cadastrar_moeda`, `excluir_moeda`, `consultar_saldo_admin`, `consultar_extrato_admin`.
4. `excluir_*` pede confirmação (`input("Confirma? (S/N)")`) e mostra os dados antes.
5. A carteira precisa passar a aceitar moeda nova: em vez de `REAL/BTC/ETH/XRP` fixos, usar `carteira[moeda]` criado no cadastro.
