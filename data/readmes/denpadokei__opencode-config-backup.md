# opencode-config-backup

[OpenChamber](https://openchamber.dev) + [OpenCode](https://opencode.ai) の設定ファイル集と、
AI エージェント向けのリストア手順書です。環境構築記事の参照リポジトリとして公開しています。

**リストア手順は [`RESTORE.md`](RESTORE.md) にあります**（AI に「このリポジトリの RESTORE.md に従って復元して」と渡せば実行できる構成）。

## 構成

```
opencode/       ~/.config/opencode の設定（MCP・plugins・メモリエージェント・スキル）
openchamber/    ~/.config/openchamber の設定（preferences・routing・settings のテンプレート）
backup.ps1      現在の設定をこのリポジトリへコピーしてコミット（-Push で push まで）
restore.ps1     このリポジトリの内容を設定フォルダへ復元
RESTORE.md      AI 用リストア手順書（前提・シークレット・検証チェックリスト込み）
```

## 使い方

```powershell
# バックアップ（設定を変えたあとに実行）
.\backup.ps1 -Push

# リストア（再インストール後など）
.\restore.ps1
```

## 含めないもの

シークレット（API キー・パスワード・鍵ペア）と個別環境の情報（パス・セッションID）は意図的に含めていません。
`backup.ps1` は実 `settings.json` を git 管理外の `settings.local.json` としてローカル保存するだけなので、
公開リポジトリには個人情報が載りません。詳細は RESTORE.md を参照してください。
