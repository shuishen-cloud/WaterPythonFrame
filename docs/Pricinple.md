## Git

- `pull` 采用 `rebase` 模式，防止频繁的 `pull` 污染分支历史，设置 `pull` 默认使用 `rebase` 而不是 `merege`（*`merege` 用于合并本地分支*）:

```shell
git config pull.rebase true
```
