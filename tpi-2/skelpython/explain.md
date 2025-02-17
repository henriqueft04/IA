# Exercicio 1

## Passo 1-> Detetar tipos
- straight forward tbh

## Passo 2-> Escolher tipo mais comum
- straight forward as well

## Passo 3-> Função auxiliar de ver os tipos
- achei que era uma maneira simples de fazer isto, não sei se é a melhor

## Passo 4-> Lidar com relações de membros e submembros
- tava a dar erro sem isto
- considera aepnas as delcaracoes locais
- guarda a ordem de entrada dos valores!!
- evita valores duplicados

## Passo 5-> AssocSome, não tenho um bom nome para este passo :)
- vai buscar os valores da entidade e todos os acestors
- mantem a ordem de entrada
- evita valores duplicados
- apenas guarda valores únicos

## Passo 6-> AssocOne, AssocNum
- se for one, retorna o mais comum
- se for num, retorna a média

---

# Exercicio 2

## Passo 1-> Função auxiliar das mães 🫂
- esta função retorna a mãe de uma variável

## Passo 2-> Função get_ancestors
- esta função retorna todos os ancestrais de uma variável

## Passo 3-> Testar a independencia
### Passo 3.1-> recolher as variáveis relevantes
### Passo 3.2-> constriuir grafo n direcionado
### Passo 3.3-> remover as arestas com variáveis given
### Passo 3.4-> verificar se há caminho, se sim, há dependencia

---

# Exercicio 3

## Passo 1 -> Verificar domínios vazios

## Passo 2 -> Caso base: atribuição completa
- Verifica se todas as variáveis têm exatamente um valor no domínio.
- Se sim:
  - Valida a atribuição completa contra todas as restrições.
  - Se satisfaz todas as restrições, adiciona a atribuição às soluções. Caso contrário, retorna uma lista vazia.

## Passo 3 -> Escolher variável para branch
- Escolhe uma variável com mais de um valor no domínio.
- Para estar mais escolho a variável com o menor domínio).

## Passo 4 -> Atribuir valor e propagar
- Para cada valor no domínio da variável escolhida:
  - Fixa esse valor.
  - Propaga as restrições para reduzir os domínios das variáveis dependentes.

## Passo 5 -> Recursão
- Chama-se recursivamente `search_all` com os novos domínios após a propagação.

## Passo 6 -> Remover duplicados

---

# Exercicio 4

## Passo 1 -> Criar variável auxiliar e combinações de entradas válidas
- Gera uma nova variável auxiliar (`aux_var`), que o dominio são tuplos de valores das variáveis dadas, que satisfazem a restrição de ordem superior (`HO constraint`).
- Usa o produto cartesiano dos domínios das variáveis para gerar todos os tuplos possíveis.
- Filtra os tuplos para incluir apenas aqueles que satisfazem a restrição de ordem superior.

## Passo 2 -> Adicionar restrições binárias
- Adiciona restrições binárias entre cada variável original e a variável auxiliar:
  - Garante que o valor de cada variável original corresponde ao elemento correto no tuplo selecionado na variável auxiliar.

## Passo 3 -> Restrição simétrica
- Adiciona uma restrição simétrica para garantir que as verificações funcionam em ambas as direções.


## Passo 3 -> Atualizar estrutura do problema
- Atualiza os domínios e as restrições do problema.
- A função retorna os domínios e restrições modificados.

---
