## Explicações
No comando existem parâmetros com nomes de tabelas seguidos de números, estes representando a quantidade de dados que serão inseridos.

Há também o parâmetro **--batch** que aumenta a quantidade de dados inseridos por lote *(padrão = 1000)*. Aumentar o batch aumenta a velocidade porém também o consumo de RAM e CPU. **NÃO RECOMENDADO USAR BATCH MAIOR QUE 5000**

## Como executar
Execute o script `seed.py` a partir do diretório do backend. As quantidades são
totais por entidade nesta execução e o script preserva os dados existentes por
padrão.

```bash
cd backend
python seed.py --usuarios 1000 --conteudos 2000 --avaliacoes 5000 --favoritos 3000 --assistidos 3000
```

Cada conteúdo criado também recebe um registro correspondente em `filme`,
`serie` ou `anime`. Avaliações, favoritos e assistidos são gerados com
combinações únicas de usuário e conteúdo, respeitando as restrições do banco.

Opções úteis:

- `--batch 2000`: tamanho do lote de inserção;
- `--seed 42`: torna a geração aleatória reproduzível;
- `--reset`: limpa as tabelas antes de criar os dados. Essa opção é explícita e
  deve ser usada com cuidado.

Exemplo reproduzível em um banco vazio:

```bash
python seed.py --reset --usuarios 100 --conteudos 200 --avaliacoes 500 --seed 42
```