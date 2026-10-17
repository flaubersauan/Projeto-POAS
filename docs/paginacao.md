# Paginação

A API possui três tipos de paginação. Cada tipo fica em um módulo próprio na
pasta `backend/schemas/pagination`:

- `cursor.py`: paginação das entidades armazenadas no banco de dados;
- `tmdb.py`: paginação das consultas externas ao TMDB;
- `kitsu.py`: paginação das consultas externas ao Kitsu.

Cada módulo possui três esquemas:

- **Parâmetros:** dados recebidos para realizar a consulta;
- **Paginação:** metadados necessários para interpretar ou continuar a
  consulta;
- **Página:** combinação dos dados retornados com os metadados de paginação.

Todos os retornos paginados seguem a estrutura geral:

```json
{
  "data": [],
  "pagination": {}
}
```

## Esquemas de retorno

### TMDB

Ao pesquisar por filme ou série no TMDB, alguns dados não são retornados na
listagem e só ficam disponíveis em uma consulta pelo ID. Por isso, existem
dois esquemas de retorno para cada tipo de conteúdo:

- `FilmeListRead`: dados de um filme em uma listagem;
- `FilmeRead`: dados completos de um filme consultado pelo ID;
- `SerieListRead`: dados de uma série em uma listagem;
- `SerieRead`: dados completos de uma série consultada pelo ID.

As páginas do TMDB devem usar `TmdbPage[FilmeListRead]` ou
`TmdbPage[SerieListRead]` nas listagens. Consultas individuais retornam
`FilmeRead` ou `SerieRead`, sem uma página de resultados.

### Kitsu

As consultas de anime utilizam o esquema `AnimeRead` para representar um
anime normalizado pela aplicação.

Uma listagem pode ser representada por `KitsuPage[AnimeRead]` e uma consulta
individual por `AnimeRead`.

## Paginação por cursor

É utilizada nas entidades da própria aplicação, como `Usuario`. O cursor é o
ID do último registro retornado e permite buscar os registros seguintes sem
usar páginas numéricas.

### Parâmetros

Modelo: `CursorPaginationParams`

- `limit`: quantidade máxima de registros, entre 1 e 20; padrão: `20`;
- `cursor`: ID a partir do qual a busca deve continuar; padrão: `0`.

Exemplo de requisição:

```text
GET /usuarios?limit=20&cursor=15
```

### Retorno

Modelo: `CursorPagination`

- `cursor`: ID do último registro retornado; `null` quando não há registros;
- `has_more`: indica se existem mais registros após a listagem atual.

Exemplo:

```json
{
  "data": [],
  "pagination": {
    "cursor": 35,
    "has_more": true
  }
}
```

Quando o cursor informado ultrapassa o último ID disponível, a API retorna
`200 OK` com uma página vazia:

```json
{
  "data": [],
  "pagination": {
    "cursor": null,
    "has_more": false
  }
}
```

Os esquemas envolvidos são `CursorPaginationParams`, `CursorPagination` e
`CursorPage[T]`.

As listagens de conteúdos assistidos também utilizam paginação por cursor:

- `GET /filmes/assistidos`;
- `GET /series/assistidas`;
- `GET /animes/assistidos`.

Esses endpoints recebem os mesmos parâmetros `limit` e `cursor` e retornam
`CursorPage[T]`. O cursor corresponde ao `id` do registro de assistência, e
não ao ID externo do filme, série ou anime.

As listagens de conteúdos favoritos seguem o mesmo contrato:

- `GET /filmes/favoritos`;
- `GET /series/favoritas`;
- `GET /animes/favoritos`.

O cursor corresponde ao `id` do registro de favorito.

As avaliações também utilizam paginação por cursor:

- `GET /usuarios/avaliacoes`;
- `GET /filmes/{filme_id}/avaliacoes`;
- `GET /series/{serie_id}/avaliacoes`;
- `GET /animes/{anime_id}/avaliacoes`.

O cursor corresponde ao `id` da avaliação.

As listagens de favoritos, assistidos e avaliações aceitam o parâmetro
`ordenacao`:

- `ordenacao=recentes` (padrão): mais recentes primeiro;
- `ordenacao=antigos`: mais antigos primeiro.

Quando a listagem é paginada, o cursor continua sendo o ID do registro, mas a
consulta usa a data da linha apontada pelo cursor e o ID como desempate. Isso
mantém a navegação correta mesmo quando dois registros possuem a mesma data.

## Paginação do TMDB

O TMDB utiliza páginas numeradas. A API recebe `page` e `limit`; o parâmetro
`page` é enviado ao TMDB, enquanto `limit` define o limite adotado pela API.

### Parâmetros

Modelo: `TmdbPaginationParams`

- `page`: número da página, a partir de `1`; padrão: `1`;
- `limit`: quantidade máxima de itens, entre 1 e 20; padrão: `20`.

Exemplo de requisição:

```text
GET /filmes?busca=matrix&page=1&limit=20
```

### Retorno

Modelo: `TmdbPagination`

- `page`: página atual;
- `total_pages`: quantidade total de páginas disponível no TMDB;
- `total_results`: quantidade total de resultados;
- `has_more`: indica se existe uma página posterior.

Exemplo:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "total_pages": 5,
    "total_results": 87,
    "has_more": true
  }
}
```

Os esquemas envolvidos são `TmdbPaginationParams`, `TmdbPagination` e
`TmdbPage[T]`.

## Paginação do Kitsu

O Kitsu utiliza paginação por deslocamento (`offset`) e quantidade de itens
(`limit`). Na API da aplicação, os parâmetros são recebidos de forma simples
e devem ser convertidos para a sintaxe exigida pelo Kitsu.

### Parâmetros

Modelo: `KitsuPaginationParams`

- `limit`: quantidade de itens, entre 1 e 20; padrão: `10`;
- `offset`: quantidade de itens a ignorar antes do primeiro resultado; padrão:
  `0`.

Exemplo de requisição para a API:

```text
GET /animes?limit=5&offset=0
```

Essa requisição deve ser enviada ao Kitsu como:

```text
/anime?page[limit]=5&page[offset]=0
```

### Retorno

Modelo: `KitsuPagination`

- `limit`: quantidade solicitada;
- `offset`: deslocamento utilizado;
- `total_results`: quantidade total de resultados;
- `has_more`: indica se existem mais resultados após a listagem atual.

Exemplo:

```json
{
  "data": [],
  "pagination": {
    "limit": 5,
    "offset": 0,
    "total_results": 42,
    "has_more": true
  }
}
```

Os esquemas envolvidos são `KitsuPaginationParams`, `KitsuPagination` e
`KitsuPage[T]`.