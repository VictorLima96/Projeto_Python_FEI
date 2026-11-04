# Projeto Final — Exchange de Criptomoedas (CCP110 Fundamentos de Algoritmos)

**Documento consolidado de referência + guia de execução**
Fontes: `Ref/Projeto - Exchange de Criptomoedas.pdf` e as aulas 01 a 13 (completas).
Texto bruto extraído dos PDFs: pasta `_texto_extraido/` (útil para buscar com Ctrl+F).

> Como usar: **Parte 1** é o "o que entregar". **Parte 2** é a cola de Python por aula, já com o "onde isso aparece no projeto". **Parte 3** liga cada funcionalidade aos conceitos. **Parte 4** é o roteiro passo a passo. **Parte 5** é o checklist final.

---

## Sumário

1. [Especificação do projeto (consolidada)](#1-especificação-do-projeto-consolidada)
2. [Base de Python das aulas (cola por tópico)](#2-base-de-python-das-aulas-cola-por-tópico)
3. [De → Para: funcionalidade × conceito](#3-de--para-funcionalidade--conceito)
4. [Guia passo a passo para executar o projeto](#4-guia-passo-a-passo-para-executar-o-projeto)
5. [Checklists, erros comuns e plano de testes](#5-checklists-erros-comuns-e-plano-de-testes)
6. [Mapa dos PDFs (onde achar cada coisa)](#6-mapa-dos-pdfs-onde-achar-cada-coisa)

---

# 1. Especificação do projeto (consolidada)

## 1.1 Visão geral

Criar uma **exchange de criptomoedas via console**: o investidor faz login com CPF + senha, consulta saldo e extrato, deposita e saca reais, compra e vende criptomoedas, e atualiza as cotações. Os dados **não podem ser perdidos** quando o programa fecha → tudo persistido em arquivos `.txt`.

- Individual **ou** em dupla (a dupla tem um **usuário administrador** com funções extras).
- Proibido copiar código (plágio = nota zero).

## 1.2 Criptomoedas e taxas (obrigatórias)

| Moeda | Taxa na **compra** | Taxa na **venda** |
|---|---|---|
| Bitcoin (BTC) | 2% | 3% |
| Ethereum (ETH) | 1% | 2% |
| Ripple (XRP) | 1% | 1% |

O projeto exige essas 3 moedas. Na versão em dupla, o administrador pode **cadastrar novas criptomoedas** (com nome, cotação, taxa de compra e taxa de venda) — ou seja, a lista de moedas deixa de ser fixa e passa a ser dado.

## 1.3 Menu do investidor

```
1. Consultar saldo
2. Consultar extrato
3. Depositar
4. Sacar
5. Comprar criptomoedas
6. Vender criptomoedas
7. Atualizar cotação
8. Sair
```

## 1.4 Menu do administrador (somente dupla)

```
1. Cadastrar novo investidor
2. Excluir investidor
3. Cadastrar nova criptomoeda
4. Excluir criptomoeda
5. Consultar saldo de um investidor
6. Consultar extrato de um investidor
7. Atualizar cotação das criptomoedas
8. Sair
```

## 1.5 Regras de negócio, função por função

| Funcionalidade | Entrada pedida | Regras / saída esperada |
|---|---|---|
| **Login** | CPF **sem pontos e sem traços** + senha **numérica de 6 dígitos** | Se conferir, libera o menu completo. Senão, acesso negado. |
| **Consultar saldo** | Senha de 6 dígitos | Mostra **Nome, CPF** (formatado `123.456.789-00`), Reais, BTC, ETH, XRP. |
| **Consultar extrato** | Senha de 6 dígitos | Lista as operações no formato do item 1.6. |
| **Depositar** | Valor do depósito | Soma em Reais; mostrar saldos atualizados; registrar no extrato. |
| **Sacar** | Valor do saque | **Saldo não pode ficar negativo**; mostrar saldos atualizados; registrar no extrato. |
| **Comprar** | Senha → escolha da moeda e quanto | Mostra as cotações, aplica a **taxa de compra**, **saldo não pode ficar negativo**, registrar no extrato. |
| **Vender** | Senha → escolha da moeda e quanto | Mostra as cotações, aplica a **taxa de venda**, não pode vender mais do que possui, registrar no extrato. |
| **Atualizar cotação** | (nada, ou nada além do comando) | Varia **todas** as cotações com `random`: **mínimo −5% e máximo +5%** do valor anterior. |
| **Cadastrar investidor** (dupla) | Nome, CPF (sem pontos/traços) e senha | CPF não pode repetir. |
| **Excluir investidor** (dupla) | CPF | Se existir, **mostrar os dados e pedir confirmação** antes de excluir. |
| **Cadastrar criptomoeda** (dupla) | Nome, cotação, taxa de compra, taxa de venda | Passa a aparecer nas operações. |
| **Excluir criptomoeda** (dupla) | Nome | Se existir, mostrar dados e **pedir confirmação**. |
| **Consultar saldo/extrato de um investidor** (dupla) | CPF do investidor | Não pede senha do investidor; mostra o mesmo formato do item 1.5. |

## 1.6 Formato do extrato (o slide é a referência)

```
Nome: Gabriela Biondi
CPF: 123.456.789-00
01-01-2024 12:50 + 500.00 REAL CT: 0.0      TX: 0.00 REAL: 500.00 BTC: 0.0 ETH: 0.0   XRP: 0.0
01-01-2024 13:00 + 100.00 XRP  CT: 2.57     TX: 0.01 REAL: 399.00 BTC: 0.0 ETH: 0.0   XRP: 38.9
02-01-2024 14:50 - 100.00 REAL CT: 0.0      TX: 0.00 REAL: 299.00 BTC: 0.0 ETH: 0.0   XRP: 38.9
02-01-2024 18:00 + 100.00 ETH  CT: 16108.0  TX: 0.01 REAL: 198.00 BTC: 0.0 ETH: 0.006 XRP: 38.9
```

Colunas: **data-hora · sinal (+/−) · valor · moeda · CT (cotação usada) · TX (taxa) · saldos após a operação**.

⚠️ **Atenção (o exemplo do slide não fecha aritmeticamente):** em `+ 100.00 XRP CT: 2.57` o saldo em reais cai exatamente 101,00 (500 → 399), o que corresponde a 100/2.57 ≈ 38,9 XRP — não 100 XRP. Já em `+ 100.00 ETH CT: 16108.0`, 100 reais compram 0,0062 ETH, e o saldo mostra 0,006. Ou seja: no exemplo, a coluna *valor* está em **reais gastos** na compra, e o `TX` nem sempre bate com a taxa da tabela.
**Decisão que você precisa tomar e documentar (uma única convenção, aplicada em todo o programa):**
- `valor` = quantidade da **moeda** movimentada (mais natural para "comprar 0,01 BTC"); ou
- `valor` = **reais** movimentados.
- `TX` = taxa em reais, em quantidade de cripto, ou só informativa.
Escolha, escreva no relatório e mantenha consistente — é o tipo de detalhe que o professor confere no vídeo.

## 1.7 Persistência (requisito eliminatório na prática)

- Todos os dados em arquivos **`.txt`** (não use banco de dados, não use pickle/JSON como formato principal).
- Precisa sobreviver a: fechar o programa, `Ctrl+C`, erro/crash, desligar o computador.
- Implicação prática: **gravar logo após cada operação que muda estado** (depósito, saque, compra, venda, cadastro, exclusão, atualização de cotação) — não só no "Sair".
- Escreva com `open(..., "w")` para sobrescrever / `open(..., "a")` para acrescentar (extrato); `write()` não pula linha sozinho — inclua `\n`; feche com `close()` ou use `with`. Na leitura: `readlines()`, `strip()` e `split(";")`. Tudo isso é a **aula 12**.

## 1.8 Individual × Dupla — o que muda

| Item | Individual | Dupla |
|---|---|---|
| Usuário | 1 tipo (investidor) | Investidor **+ administrador** |
| Criptomoedas | 3 fixas (BTC, ETH, XRP) | Cadastráveis/excluíveis pelo admin |
| Investidores | Já existentes no `.txt` | Cadastráveis/excluíveis pelo admin |
| Consultar saldo/extrato | Só o próprio | Próprio **e** de qualquer investidor (admin) |

## 1.9 Entregas parciais (cronograma no Moodle — confira as datas!)

**Entrega 1**
- Individual: login do investidor funcionando + menu pós-login + **funções criadas sem lógica** (stubs) para cada opção + "Sair" funcionando.
- Dupla: tudo acima **+** login e menu do administrador + stubs das opções do admin.

**Entrega 2**
- Individual: consultar saldo, depositar, sacar.
- Dupla: + cadastrar investidores, consultar saldo de um investidor.

**Entrega 3**
- Individual: consultar extrato, comprar, vender.
- Dupla: + cadastrar criptomoedas, consultar extrato de um investidor.

**Entrega 4**
- Individual: atualizar cotação + **gravar em `.txt`**.
- Dupla: + atualizar cotação de uma criptomoeda (individual/por moeda).

**Entrega final**
- Todos os códigos funcionando + documentação + vídeo.

## 1.10 Critérios de avaliação e itens obrigatórios da entrega

Critérios: funcionamento · atendimento às especificações · aplicação dos conceitos de aula · aplicação de conceitos novos/adaptações · explicação no vídeo e na documentação.

Entrega:
1. **Todos os códigos-fonte**;
2. **Relatório de 3 a 5 páginas** com a documentação do projeto;
3. **Link de vídeo público** (YouTube ou similar), **de 3 a 8 minutos**, mostrando **todas** as funcionalidades — inclusive **os arquivos `.txt` sendo atualizados durante as operações**. Em dupla, os dois apresentam.

---

# 2. Base de Python das aulas (cola por tópico)

> Cada seção: o conceito da aula → sintaxe enxuta → **uso direto no projeto**. Os exemplos são os do material da disciplina (não são o seu projeto).

## Aula 01 — Variáveis, tipos, `print`, `input`, operadores

- Variável: nome = valor. Nome começa com letra ou `_`, sem espaços, **case-sensitive**, sem acento (evite).
- Tipos: `int`, `float`, `complex`, `str`, `bool`.
- `print()`, composição com `%d/%f/%.2f`, `.format()`, f-string.
- `input()` **sempre devolve `str`** → converter: `int()`, `float()`.
- Aritméticos: `+ - * / // % **`. Módulo `math`: `import math` → `math.sqrt()`, `math.ceil()`, `math.pi`.

```python
nome = "Fulano da Silva"
idade = int(input("Idade: "))
preco = float(input("Preço: "))
print("Total: R$ %.2f" % (preco * 1.1))
print(f"Olá {nome}, você tem {idade} anos")
```

**No projeto:** todo `input()` de valor precisa de `float()`; todo `print()` de dinheiro usa `%.2f`; cripto precisa de mais casas (`%.6f` ou `%.8f`). `math.ceil` ajuda em validações de quantidade.

## Aula 02 — Pseudocódigo, fluxograma, teste de mesa, VSCode

- Três formas de escrever algoritmo: pseudocódigo, diagrama de blocos, linguagem.
- **Teste de mesa** = simular a execução linha a linha anotando o valor das variáveis.
- Ambiente: VSCode.

**No projeto:** use teste de mesa antes de codar compra/venda (é onde o saldo "some"). Faça a tabela `saldo_reais | qtd_btc | preco | taxa | resultado` e confira 3 casos: compra normal, compra que zera o saldo, compra acima do saldo.

## Aula 03 — Operadores relacionais e decisão (`if` / `else`)

- Relacionais: `== != > < >= <=` → resultado `bool`.
- `if condicao:` + **indentação obrigatória**; `else:` para o caso falso.

```python
a = int(input("Digite um numero: "))
if a > 0:
    print("Esse numero eh positivo!")
else:
    print("Esse numero nao eh positivo!")
```

**No projeto:** validação de login, senha, saldo suficiente, quantidade > 0, CPF existente. **Sempre rejeite valor negativo/zero** em depósito, saque, compra e venda.

## Aula 04 — Operadores lógicos, precedência, decisão encadeada

- `and`, `or`, `not`. Precedência: `not` > `and` > `or`.
- Precedência geral: parênteses → aritméticos → relacionais → lógicos.
- **Seleção encadeada**: `if / elif / else`. Evite `if` dentro de `if` quando puder escrever `elif` (seleção encadeada homogênea).
- `elif` é o que a aula chama de encadeamento — use para escolher BTC/ETH/XRP.

```python
if (a < b + c) and (b < a + c) and (c < a + b):
    if (a == b) and (b == c):
        print("Triangulo equilatero")
    elif (a == b) or (a == c) or (b == c):
        print("Triangulo isosceles")
    else:
        print("Triangulo escaleno")
else:
    print("Nao e triangulo")
```

**No projeto:** menu (`elif opcao == 5:`), escolha da moeda, e a condição composta da compra:
`if quantidade * cotacao * (1 + taxa) <= saldo_reais and quantidade > 0:`

## Aula 05 — Repetição (`while`, `for`, `range`, `break`)

- `while condicao:` repete enquanto verdadeiro. **Contador** (conta ocorrências) × **acumulador** (soma valores).
- `while True:` + `break` = menu infinito até "Sair".
- `for x in range(inicio, fim, passo):` — `fim` é **exclusivo**.

```python
while True:
    entrada = int(input("Digite um numero a somar ou 0 pra sair: "))
    if entrada == 0:
        break
    somatoria = somatoria + entrada
```

**No projeto:** o laço do menu; o laço de "senha errada, tente de novo"; `for` para percorrer moedas/linhas do extrato.

## Aula 06 — Repetição aninhada

- Loop dentro de loop; o interno roda inteiro a cada iteração do externo. Serve para matrizes/listas de listas.

**No projeto:** percorrer `moedas × investidores` (ex.: atualizar todas as cotações, ou montar relatório), e varrer o extrato por moeda.

## Aula 07 — Funções

- `def nome(parametros):` … `return valor`. Função = bloco com tarefa específica, reutilizável.
- **Variável local** existe só dentro da função; **global** é vista por todos e só pode ser alterada com `global` (evite: prefira parâmetros + `return`).
- Parâmetros opcionais com valor padrão.
- `lambda` para funções de uma linha.

```python
def soma(x, y):
    res = x + y
    return res

def maximo(x, y):
    return x if x > y else y
```

**No projeto:** é o coração da entrega 1 — **uma função por opção do menu** (`consultar_saldo()`, `depositar()`, …), chamadas de dentro do `while` do menu. Uma boa divisão: `login()`, `menu_investidor()`, `menu_admin()`, `carregar_dados()`, `salvar_dados()`, `atualizar_cotacoes()`, `registrar_extrato()`.

## Aula 08 — Listas e tuplas

- Lista `[]`: indexada a partir de **0**, heterogênea, mutável.
- `append(x)` fim · `insert(i, x)` · `pop(i)` · `remove(x)` · `len(L)`.
- `x in L` para saber se existe; `L.index(x)` para a posição; `for` para percorrer.
- **Slicing**: `L[1:3]`, `L[:2]`, `L[-1]`.
- **Cópia**: `z1 = z` só cria outro nome para a mesma lista; para copiar de verdade: `z1 = z[:]` (ou `list(z)`).
- **Tuplas** `()` são imutáveis — boas para dados fixos.

**No projeto:** cotação e saldos por moeda podem ser listas, mas dicionário é mais legível (aula 11). Use tupla para o par fixo `(taxa_compra, taxa_venda)` das 3 moedas obrigatórias.

## Aula 09 — `map`, `filter`, list comprehension

```python
quadrados = [x * x for x in range(10)]
pares = [n for n in numeros if n % 2 == 0]
positivos = list(filter(lambda x: x > 0, numeros))
convertidos = list(map(lambda c: (c * 9/5) + 32, temperaturas))
```

**No projeto:** formatar linhas do extrato, filtrar operações de uma moeda, montar lista de cotações para exibir antes de comprar/vender.

## Aula 10 — Listas aninhadas e matrizes + `random`

- Matriz = lista de listas: `M = [[0]*3 for _ in range(10)]` (⚠️ **não** use `[[0]*3]*10`, isso cria linhas compartilhadas).
- Acesso `M[linha][coluna]`.
- Aleatórios: `from random import randint, random` — `randint(0,10)`, `random()*10`.

**No projeto:** a atualização de cotação é exatamente isto:
`nova = antiga * (1 + random.uniform(-0.05, 0.05))` — garante o intervalo **−5% a +5%**. Guarde a cotação antiga para exibir no relatório/vídeo.

## Aula 11 — Dicionários

- `{chave: valor}`; chave única e imutável; acesso por chave, não por índice.
- `d["k"]`, `d.get("k", default)`, `d["k"] = v` (adiciona/atualiza), `del d["k"]`, `d.items()`, `d.keys()`, `d.values()`, `for k, v in d.items():`.

```python
estoque = {"banana": 3, "maca": 5}
estoque["uva"] = 10
for fruta, qtd in estoque.items():
    print(fruta, qtd)
```

**No projeto:** é a estrutura mais natural para:
- **cotações:** `{"BTC": 350000.0, "ETH": 16000.0, "XRP": 2.57}`
- **taxas:** `{"BTC": (0.02, 0.03), "ETH": (0.01, 0.02), "XRP": (0.01, 0.01)}`
- **carteira do usuário:** `{"REAL": 580.0, "BTC": 0.0158, ...}`
- **investidores:** `{"12345678900": {"nome": ..., "senha": ..., "carteira": {...}}}`
Isso resolve o individual **e** já deixa pronto o "cadastrar/excluir moeda" da dupla (basta `del cotacoes[nome]`).

## Aula 12 — Arquivos

- **Objetivo:** perenidade dos dados. Arquivo = linhas de texto (`.txt`, `.dat`, `.csv`…).
- **Abrir:** `arquivo = open("teste.txt", "w")`. Modos (tabela da p.3 do slide, que está em imagem): `"r"` ler (erro se não existe) · `"w"` escrever (**apaga o conteúdo** se o arquivo existir) · `"a"` acrescentar no fim · `+` para leitura e escrita · `b` para binário.
- **Escrever:** `arquivo.write("texto")` — funciona como o `print` com marcadores, mas **você precisa incluir o `\n`** para pular linha.
- **Fechar:** `arquivo.close()` (o slide insiste nisso: depois de escrever, feche).
- **Ler:** `open(..., "r")` e `for linha in arquivo.readlines():` — cada `linha` vem **com o `\n` no final** (por isso o `strip()`).

```python
# --- jeito do slide (open/write/close) ---
arquivo = open("teste.txt", "w")
for linha in range(1, 101):
    arquivo.write("Linha %d\n" % linha)
arquivo.close()

arquivo = open("teste.txt", "r")
for linha in arquivo.readlines():
    print(linha)
arquivo.close()

# --- jeito "à prova de esquecimento" (with fecha sozinho) ---
with open("carteira.txt", "w", encoding="utf-8") as arq:
    for cpf, dados in investidores.items():
        arq.write(f"{cpf};{dados['nome']};{dados['senha']}\n")

with open("extrato.txt", "a", encoding="utf-8") as arq:   # "a" não apaga o histórico
    arq.write(linha_do_extrato + "\n")

with open("carteira.txt", "r", encoding="utf-8") as arq:
    for linha in arq:
        linha = linha.strip()
        if linha == "":
            continue
        campos = linha.split(";")
```

**Exercícios da aula (p.8-14) e por que servem para o projeto:**

| Exercício | O que treina | Ligação com a exchange |
|---|---|---|
| Ex.01 — gravar pares e ímpares em arquivos separados | escrita em `"w"` | gravar `investidores.txt` / `moedas.txt` |
| Ex.02 — gerar arquivo só com múltiplos de 4 | ler → filtrar → escrever | atualizar cotações e regravar `moedas.txt` |
| Ex.03 — ler nome/telefone e gravar em `contatos.txt` até nome vazio | entrada em loop + gravação | cadastro de investidores |
| Ex.04 — **agenda de telefones com menu 1-Novo / 2-Procura / 3-Atualiza / 4-Apaga / 0-Sair** | CRUD com persistência e loop infinito | **é o ensaio geral do seu projeto**: mesmo esqueleto (menu + `while True` + arquivo) |

> 💡 O Ex.04 é o melhor treino possível: se você conseguir fazer a agenda com os dados sobrevivendo ao fechamento do programa, você já dominou 80% da mecânica da Entrega 4.

**No projeto:**
- **`"w"` para sobrescrever o estado** (investidores, moedas) e **`"a"` para o extrato** (histórico nunca é reescrito);
- grave **logo após cada operação** que muda estado (requisito de não perder dados);
- `readlines()`/`for linha in arq` + `strip()` + `split(";")` na leitura; converta com `float()`/`int()`;
- `try/except FileNotFoundError` no primeiro uso (arquivo ainda não existe);
- **nunca** gravar float com vírgula (senão o `float()` quebra na leitura);
- não use `"w"` por engano no extrato: você apaga todo o histórico do usuário.

Regras de ouro: `strip()` em toda linha lida · separador que **não** apareça nos dados · fechar sempre (ou usar `with`) · testar com arquivo vazio, inexistente e com linha em branco.

## Aula 13 — Strings, módulos/pacotes, Tkinter

- Strings são sequências (indexáveis e fatiáveis). Métodos úteis: `strip()`, `split()`, `replace()`, `upper()`, `lower()`, `capitalize()`, `count()`, `find()`, `isdigit()`, `isalpha()`.
- `ord()` / `chr()` para ASCII/Unicode.
- **Módulo** = arquivo `.py` importável (`import math` / `from math import sqrt`).
- `if __name__ == "__main__": main()` → só executa quando o arquivo é rodado direto, não quando é importado.
- **Pacote** = pasta de módulos, com `__init__.py`.
- **Tkinter** (opcional, GUI): `Tk()`, `title()`, `geometry()`, `Label`, `Button(command=...)`, `Entry().get()`, `.place(x=, y=, anchor=CENTER)`, `messagebox.showinfo/askyesno`, `mainloop()`.

**No projeto:**
- `strip()`/`split(";")` são a dupla que fecha o ciclo da aula 12: você **grava** com `write()` e **relê** com `split()`;
- `isdigit()` + `len(senha) == 6` valida a senha; `len(cpf) == 11 and cpf.isdigit()` valida o CPF;
- o `__main__` permite separar `main.py` + `funcoes.py` (organização que conta como "aplicação de novos conceitos");
- o console é obrigatório; Tkinter é extra (só se quiser impressionar — não substitui o console).

---

# 3. De → Para: funcionalidade × conceito

| Funcionalidade | Conceitos que você vai usar (aula) |
|---|---|
| Login CPF + senha | `input`, `str.isdigit`, `len`, `if/else`, dicionário (1, 3, 11, 13) |
| Menus e navegação | `while True` + `break`, `elif`, funções (5, 4, 7) |
| Funções-stub da Entrega 1 | `def` + `pass`/`return`, chamada no menu (7) |
| Consultar saldo | dicionário da carteira, formatação `%.2f`/`%.6f` (11, 1) |
| Consultar extrato | leitura de `.txt`, `for`, `readlines`, `split`, formatação (12, 5, 13) |
| Depositar | `float(input)`, validação `> 0`, acumulador, gravação (1, 3, 5, 12) |
| Sacar | `if valor <= saldo`, atualização de saldo, gravação (3, 12) |
| Comprar | cotação × quantidade, taxa %, `if saldo suficiente`, `elif` moeda (4, 11) |
| Vender | taxa de venda, `if qtd <= carteira`, arredondamento (3, 4, 1) |
| Atualizar cotação | `random.uniform(-0.05, 0.05)`, laço em dicionário (10, 11) |
| Persistência | `open("w")`/`open("a")`/`open("r")`, `write`, `readlines`, `split`, `strip`, `try/except` (12, 13) |
| Admin: cadastrar/excluir | dicionário, `in`, confirmação `if resp == "s"`, gravação (11, 3, 12) |
| Extra: GUI | Tkinter (13) |

---

# 4. Guia passo a passo para executar o projeto

> Regra de ouro: **entregue funcionando a cada parcial**, não deixe tudo para o fim. Cada fase abaixo já é uma entrega.

## Fase 0 — Decisões e preparação (antes de escrever código)

1. **Individual ou dupla?** Isso muda escopo (admin) e o vídeo (os dois apresentam). Decida agora.
2. Confirme no Moodle: **datas** das entregas parciais e formato de submissão.
3. Revise a **aula 12 (Arquivos)** — base da Entrega 4. O Ex.04 (agenda de contatos com menu + persistência) é o ensaio geral do projeto: faça-o antes de começar.
4. Defina a **convenção do extrato** (seção 1.6). Escreva num papel e não mude mais.
5. Defina a **estrutura de arquivos** (sugestão — não é obrigatória):
   ```
   projeto/
     main.py
     funcoes.py          (opcional: separar por módulos = conceito da aula 13)
     dados/
       investidores.txt   -> cpf;nome;senha;reais;btc;eth;xrp
       moedas.txt         -> nome;cotacao;taxa_compra;taxa_venda
       extrato.txt        -> cpf;data;hora;sinal;valor;moeda;ct;tx;reais;btc;eth;xrp
   ```
   Alternativa simples: um `.txt` por investidor para o extrato (`extrato_12345678900.txt`).
6. **Crie dados de teste à mão** (2 investidores, 3 moedas com cotações iniciais). Sem isso você não testa nada.

## Fase 1 — Esqueleto + login (Entrega 1)

1. `main.py` com `def main():` e `if __name__ == "__main__": main()`.
2. Função `carregar_investidores()` que lê o `.txt` para um dicionário (por enquanto pode ler vazio).
3. Função `login()`: pede CPF e senha, valida formato (`isdigit`, `len`), procura no dicionário, retorna o CPF logado ou `None`.
4. `menu_investidor(cpf)`: imprime as 8 opções em `while True`, lê a opção, `if/elif` chama a função correspondente, `opcao == 8` → `break`.
5. **Crie as 7 funções-stub** (`def consultar_saldo(cpf): pass`) — exatamente o que a Entrega 1 pede ("funções criadas, sem lógica").
6. Se dupla: `login_admin()`, `menu_admin()` e os 7 stubs do admin.
7. Teste: login certo, login errado, senha com letra, CPF com ponto, opção inválida, sair.

✅ *Critério de saída:* entra com login válido, navega por todas as opções sem quebrar, sai com 8.

## Fase 2 — Saldo, depósito e saque (Entrega 2)

1. Implemente `consultar_saldo(cpf)` com o formato do item 1.5 (CPF exibido formatado, valores com 2 casas para reais).
2. `validar_senha(cpf)` reaproveitável — saldo/extrato/compra/venda pedem senha de novo; **não duplique código**.
3. `depositar(cpf)`: lê valor, `if valor <= 0` recusa, soma na carteira, registra no extrato, **salva**.
4. `sacar(cpf)`: `if valor > saldo_reais` recusa ("saldo não pode ficar negativo"); senão subtrai, registra, salva.
5. Dupla: `cadastrar_investidor()` (CPF não repetido, senha 6 dígitos) e `consultar_saldo_investidor()` pelo CPF.
6. **Teste de mesa obrigatório:** depósito de 500 → saque de 100 → saque de 500 (deve recusar) → saldo tem que ser 400.

✅ *Critério de saída:* os saldos batem com a conta no papel, e o `.txt` está atualizado depois de cada operação.

## Fase 3 — Extrato, compra e venda (Entrega 3)

1. `registrar_operacao(...)`: função única que grava a linha do extrato (data/hora com `datetime`, sinal, valor, moeda, CT, TX, saldos). Uma função só = formato sempre igual.
2. `consultar_extrato(cpf)`: lê o arquivo do investidor e imprime o cabeçalho + linhas.
3. `comprar(cpf)`: senha → mostra cotações → escolhe moeda → quantidade → calcula `total = qtd * cotacao * (1 + taxa_compra)` → `if total > saldo` recusa → debita reais, credita cripto, registra, salva.
4. `vender(cpf)`: espelho da compra, com `taxa_venda` e validação `qtd <= saldo_da_moeda`.
5. **Decida o arredondamento** (`round(x, 8)` para cripto) e use em todo lugar — senão sobra `0.00000000001` de BTC e a validação de venda falha.
6. Dupla: `cadastrar_criptomoeda()`, `consultar_extrato_investidor()`.
7. **Testes de mesa:** compra que consome todo o saldo, compra acima do saldo, venda de 100% da posição, venda acima da posição, venda com cotação atualizada entre compra e venda.

✅ *Critério de saída:* comprar 100 reais de XRP e vender tudo devolve menos que 100 (por causa das taxas) e o extrato explica exatamente por quê.

## Fase 4 — Cotação e persistência (Entrega 4)

1. `atualizar_cotacoes()`: para cada moeda, `nova = antiga * (1 + random.uniform(-0.05, 0.05))`, arredonda, mostra "antes → depois (%)", salva `moedas.txt`.
2. **Persistência completa:** `salvar_investidores()`, `salvar_moedas()`, gravação do extrato. Carregue tudo no início do programa.
3. **Teste de desligamento:** rode, deposite, **mate o processo no meio** (`Ctrl+C` ou feche o terminal) e reabra — os dados têm que estar lá. Faça isso também no meio de uma compra.
4. Bordas: arquivo vazio, arquivo inexistente (`try/except FileNotFoundError`), linha em branco ou corrompida (`try/except` + `continue`), `.txt` com espaço extra (`strip`), cotação com mais casas que o esperado.
5. **Cuidado com o modo:** `"w"` no arquivo de extrato **apaga todo o histórico** — extrato é sempre `"a"`; estado (investidores/moedas) é `"w"` com o conteúdo completo reescrito.
6. Dupla: "atualizar cotação de uma criptomoeda" (versão individual, sem afetar as outras).

✅ *Critério de saída:* fecha e abre 3 vezes seguidas e nada muda; abrir os `.txt` no Bloco de Notas mostra tudo gravado.

## Fase 5 — Fechamento: relatório, vídeo, revisão

**Relatório (3 a 5 páginas)** — sugestão de estrutura:
1. Introdução e objetivo (1 parágrafo).
2. Descrição das funcionalidades (o que cada opção faz).
3. Modelagem dos dados: quais `.txt`, qual formato de linha, por quê.
4. Regras de negócio: taxas, validações, convenção do extrato, fórmula da cotação.
5. Organização do código: funções/módulos e o fluxo do menu (um diagrama ajuda).
6. Dificuldades e decisões (o que você adaptou/criou além da aula → conta ponto em "novos conceitos").
7. Conclusão.

**Vídeo (3 a 8 min)** — roteiro que cobre tudo:
1. 0:00–0:30 apresentação e o que é a exchange.
2. Login válido **e** inválido (mostre a validação).
3. Saldo inicial.
4. Depósito → **abra o `.txt` na tela mostrando a mudança**.
5. Saque válido e saque recusado por saldo insuficiente.
6. Compra: mostre a cotação, a taxa aplicada e o cálculo.
7. Venda (inclusive tentativa de vender mais do que tem).
8. Extrato completo.
9. Atualizar cotação (mostre o antes/depois e o limite de ±5%).
10. **Feche o programa e abra de novo** para provar a persistência.
11. (Dupla) login admin, cadastrar/excluir investidor com confirmação, cadastrar/excluir moeda, consultar saldo/extrato de outro investidor. Cada um explica sua parte.
12. Encerramento.

**Honestidade acadêmica:** escreva o código você mesmo, entenda cada linha e saiba explicar no vídeo — o critério "explicação do vídeo" e a regra de plágio tornam isso parte da nota.

---

# 5. Checklists, erros comuns e plano de testes

## 5.1 Checklist de requisitos

**Investidor**
- [ ] Login com CPF sem máscara + senha numérica de 6 dígitos
- [ ] Menu com as 8 opções exatas
- [ ] Consultar saldo (nome, CPF, reais, BTC, ETH, XRP) com senha
- [ ] Consultar extrato com senha
- [ ] Depositar (mostra saldos atualizados)
- [ ] Sacar sem deixar saldo negativo
- [ ] Comprar com taxa correta por moeda
- [ ] Vender com taxa correta por moeda
- [ ] Atualizar cotação das 3 moedas dentro de ±5%
- [ ] Sair

**Dupla (adicional)**
- [ ] Login e menu do administrador
- [ ] Cadastrar investidor
- [ ] Excluir investidor com confirmação
- [ ] Cadastrar criptomoeda (nome, cotação, taxa compra, taxa venda)
- [ ] Excluir criptomoeda com confirmação
- [ ] Consultar saldo de um investidor (por CPF, sem senha)
- [ ] Consultar extrato de um investidor
- [ ] Atualizar cotação (todas / uma)

**Técnico / entrega**
- [ ] Dados em `.txt` (nada só em memória)
- [ ] Gravação após cada operação
- [ ] Nenhum `print` de debug esquecido
- [ ] Código organizado em funções (sem bloco gigante no `main`)
- [ ] Nomes de variáveis claros, sem acento
- [ ] Relatório de 3 a 5 páginas
- [ ] Vídeo de 3 a 8 min, público, mostrando os `.txt` mudando
- [ ] Fontes completas + link enviados no prazo

## 5.2 Erros que mais custam nota (e como evitar)

| Erro | Correção |
|---|---|
| Saldo vira negativo | Valide **antes** de debitar: `if total <= saldo:` |
| Taxa aplicada ao contrário | Compra → usuário paga a mais; venda → recebe a menos. Escreva a fórmula no papel primeiro. |
| Extrato com formato diferente a cada operação | Uma única função `registrar_operacao()` |
| Perder dados ao fechar | Salvar a cada operação, não só no "Sair" |
| Float com vírgula no `.txt` | Grave sempre com ponto; converta na leitura |
| `write()` sem `\n` | Toda linha gravada precisa do `\n` explícito |
| `open(..., "w")` no extrato | Histórico usa **sempre** `"a"`; `"w"` apaga tudo |
| `input()` sem `float()` → `TypeError` | Converta **toda** entrada numérica |
| Senha/CPF aceitando lixo | `isdigit()` + `len()`, e laço para repetir |
| Comparar float com `==` | Use tolerância: `abs(a - b) < 1e-9` |
| `[[0]*3]*10` para matriz | `[[0]*3 for _ in range(10)]` |
| Cópia de lista "fantasma" | `lista[:]` ou `list(lista)` |
| Cotação variando mais de 5% | `random.uniform(-0.05, 0.05)` e arredondar depois |
| Menu que não sai / loop infinito | `break` no "Sair" e testar a opção inválida |
| Excluir sem confirmar | `input("Confirma (s/n)? ")` antes do `del` |
| Só testar o caminho feliz | Teste também entrada errada, saldo zero, arquivo vazio |

## 5.3 Plano de testes mínimo (tabela para o relatório)

| # | Cenário | Entrada | Esperado |
|---|---|---|---|
| 1 | Login válido | CPF ok + senha ok | entra no menu |
| 2 | Login inválido | senha errada | mensagem de erro, volta ao login |
| 3 | CPF com máscara | `123.456.789-00` | recusado |
| 4 | Senha com letra | `12a456` | recusado |
| 5 | Depósito | 500 | reais +500, extrato +1 linha |
| 6 | Saque maior que saldo | 900 (saldo 500) | recusado, saldo intacto |
| 7 | Compra | 100 em BTC | debita 102 (2%), credita BTC, extrato |
| 8 | Compra acima do saldo | 1000 (saldo 100) | recusado |
| 9 | Venda total | 100% da posição | recebe valor − taxa de venda |
| 10 | Venda acima da posição | 2× o que tem | recusado |
| 11 | Atualizar cotação | 1 execução | variação entre −5% e +5% |
| 12 | Persistência | fechar e reabrir | tudo igual |
| 13 | Arquivo inexistente | 1ª execução | programa abre com dados vazios, sem crash |
| 14 | (Dupla) excluir investidor | CPF + confirmação | removido do `.txt` |
| 15 | (Dupla) cadastrar moeda | DOGE, 0.85, 1%, 1% | aparece na compra/venda |
| 16 | Extrato não perde histórico | 3 operações + 1 nova | arquivo tem as 4 linhas, não 1 |
| 17 | Arquivo aberto em `"w"` com lista vazia | salvar sem investidores | não corrompe; programa reabre com dados vazios |

---

# 6. Mapa dos PDFs (onde achar cada coisa)

| Arquivo | Conteúdo | Páginas-chave |
|---|---|---|
| `Projeto - Exchange de Criptomoedas.pdf` | Especificação | p.4 taxas · p.6 menu investidor · p.8 formato extrato · p.13 ±5% · p.17-25 admin · p.26 persistência · p.27 entrega · p.29 critérios · p.30 vídeo · p.31-35 parciais |
| `aula01.pdf` | Variáveis, tipos, print/input, operadores, math | p.14 tipos · p.21-25 formatação · p.26-28 input · p.29-31 aritméticos |
| `aula02.pdf` | Pseudocódigo, fluxograma, teste de mesa, VSCode | p.5 teste de mesa |
| `aula03.pdf` | Relacionais, `if/else`, indentação | p.7-11 if · p.15-17 else |
| `aula04.pdf` | Lógicos, precedência, `elif`/encadeada | p.8-9 precedência · p.11-18 encadeada |
| `aula05.pdf` | `while`, `for`, `range`, `break`, contador/acumulador | p.6-17 while/break · p.18-20 for |
| `aula06.pdf` | Repetição aninhada | p.2-5 |
| `aula07.pdf` | Funções, escopo, parâmetros opcionais, lambda | p.3 def/return · p.18-21 escopo · p.26 lambda |
| `aula08.pdf` | Listas, métodos, slicing, cópia, tuplas | p.8-13 métodos · p.21-24 cópia · p.25 tuplas |
| `aula09.pdf` | map, filter, list comprehension | p.7-14 |
| `aula10.pdf` | Listas aninhadas/matrizes, `random` | p.7 random · p.13 matrizes |
| `aula11.pdf` | Dicionários | p.7-18 sintaxe e métodos |
| `aula12.pdf` | **Arquivos**: `open`/`write`/`readlines`/`close`, modo `"w"` e `"a"`, CRUD persistente | p.3 modos de abertura · p.4-5 escrita · p.6-7 leitura · p.10 exemplo contatos · p.14 agenda (CRUD) |
| `aula13.pdf` | Strings, módulos/pacotes, Tkinter | p.7 métodos de string · p.14-15 `__main__` · p.19-31 Tkinter |

---

### Observações finais

- Os PDFs são slides: vários exemplos de código estão **em imagem** e não vieram na extração de texto. Se precisar do exemplo exato, abra a página indicada na tabela acima. Casos conhecidos: a tabela de modos do `open()` (aula 12, p.3) e as tabelas de operadores (aula 01, p.15-17 e p.29).
- O texto extraído (para busca por palavra-chave) está em `C:\Users\vitue\Documents\Projeto_FEI\_texto_extraido\` — já inclui a `aula12.txt`.
- Nada aqui implementa o projeto: são referência, decisões a tomar e roteiro. O código é seu.
