# Tutoriais

Este repositório publica tutoriais escritos em Markdown no GitHub
Pages. Para adicionar conteúdo, basta criar um arquivo, fazer commit e
enviar para a branch `main`.

## Adicionar um tutorial

1. Abra o [modelo de post](./POST_TEMPLATE.md).
2. Copie o modelo para `src/posts/nome-do-tutorial.md`.
3. Preencha os metadados e substitua o conteúdo de exemplo.
4. Faça commit do novo arquivo.
5. Envie o commit para a branch `main`.

Use um nome de arquivo curto, em letras minúsculas, sem espaços ou
acentos. Separe as palavras com hífens. Esse nome será usado no endereço
do tutorial.

Exemplo:

```text
src/posts/compilacao-e-execucao-de-programas-mpi.md
```

## Metadados obrigatórios

Todo tutorial começa com este bloco:

```yaml
---
title: "Título exibido na página"
publishedAt: "2026-07-15"
summary: "Descrição curta exibida na lista de tutoriais."
---
```

- `title`: título completo do tutorial.
- `publishedAt`: data de publicação no formato `AAAA-MM-DD`.
- `summary`: resumo curto usado na página inicial.

O título já é renderizado pelo site. Não adicione outro título de nível
1 (`# Título`) no corpo do arquivo.

## Publicar

Depois de criar ou editar um tutorial, envie a alteração:

```bash
git add src/posts/nome-do-tutorial.md
git commit -m "Adiciona tutorial sobre o assunto"
git push origin main
```

O workflow `.github/workflows/deploy-pages.yml` cria o site e publica a
nova versão automaticamente. O andamento pode ser acompanhado na aba
**Actions** do repositório no GitHub.

Antes do primeiro deploy, configure **Settings > Pages > Source** para
usar **GitHub Actions**.

---

Baseado em [https://github.com/josean-dev/sveltekit-blog](https://github.com/josean-dev/sveltekit-blog)
