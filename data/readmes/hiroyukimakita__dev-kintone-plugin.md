# dev-kintone-plugin

kintone プラグインの開発環境、テンプレート

[tasshi-me/kintone-plugin-template: kintoneプラグインの開発テンプレート](https://github.com/tasshi-me/kintone-plugin-template) をベースに、自分好みに以下の変更を加えています。

- 開発環境は Devbox を使用可能にする
- Node のパッケージ管理を `volta` で管理可能にする
- Node のパッケージ管理を `pnpm` で管理可能にする
- プラグイン作成コマンドを一元化し `ppk` の存在により実行を分ける
- `public/` 配下の変更も監視対象に
- 開発環境を Devbox で構築し、環境変数は `.env` から init hook で読み込む
- その他軽微な変更

もともとの開発環境は以下で詳しく解説いただいており大変参考になります。  
参考：[kintoneプラグイン開発の技術スタックと開発環境](https://zenn.dev/tasshi/articles/kintone-plugin-tech-stack-2025#%E3%83%93%E3%83%AB%E3%83%89%E3%83%84%E3%83%BC%E3%83%AB%2F%E3%83%90%E3%83%B3%E3%83%89%E3%83%A9%E3%83%BC%3A-rsbuild)

## 概要

このテンプレートは、React + TypeScript を使用して kintone プラグインを開発するための基盤を提供します。  
モダンな開発環境とツールを備えており、すぐにプラグイン開発を開始できます。

## 特徴

- **React 19 + TypeScript**: 型安全な開発環境
- **Rsbuild**: 高速なビルドツール
- **エントリーポイント分離**: デスクトップ、モバイル、設定画面を個別に管理
- **コード品質管理**: Biome による静的解析とフォーマット
- **自動パッケージング**: kintone-plugin-packer によるプラグインパッケージの生成
- **自動アップロード**: cli-kintone plugin upload による開発環境への自動アップロード

## 必要要件

- Devbox（[Overview - Jetify Docs](https://www.jetify.com/docs/devbox/installing-devbox)）
  以下は devbox shell 内で管理されるので個別にインストール不要
  - Node.js (`package.json` ファイルで `volta pin` されたバージョンを使用)
  - pnpm (`package.json` ファイルで `volta pin` されたバージョンを使用)

現状だと、devbox を使用せずとも `volta` や `node`、`pnpm` が使用可能な環境であればそのまま使用できるのではと思います。  
また、もともとの `package-lock.json` も残してあるので `npm` でも使用可能かと思います。  
※ 動作確認してあるのは Devbox 環境のみ

## devbox shell に入る

開発環境でのコマンド実行は、devbox shell 内で動作確認しています。

```
/workspace/dev-kintone-plugin $ devbox shell

# devbox shell が起動し、（devbox）と表示されます。
(devbox) /bin/bash /workspace/dev-kintone-plugin $
# pnpm が使える
(devbox) /bin/bash /workspace/dev-kintone-plugin $ pnpm --version
# devbox shell から抜ける場合
(devbox) /bin/bash /workspace/dev-kintone-plugin $ exit
```

## 環境変数の設定

`pnpm start`や`pnpm upload`を使用する場合は、以下の環境変数を設定してください。

※ `.env.example` をコピーして `.env` を作成してください。  
※ 環境変数を変更した後は devbox shell に入り直す必要があります。

```bash
KINTONE_BASE_URL=https://your-subdomain.cybozu.com
KINTONE_USERNAME=your-username
KINTONE_PASSWORD=your-password
```

[cli-kintone plugin upload](https://cli.kintone.dev/ja/guide/commands/plugin-upload/) に移行しましたが、
[@kintone/plugin-uploader](https://github.com/kintone/js-sdk/tree/master/packages/plugin-uploader) に引き続き同じ環境変数で動く模様です。

## セットアップ

```bash
# 依存関係のインストール
(devbox) /bin/bash /workspace/dev-kintone-plugin $ pnpm i --frozen-lockfile
```

## 開発の流れ

### 1. プラグインの開発

```bash
# 開発サーバーの起動（ビルド + アップロード + 監視）
(devbox) /bin/bash /workspace/dev-kintone-plugin $ pnpm start
```

このコマンドは以下を実行します:

- ソースコードのビルド
- プラグインのパッケージング
- kintone 環境への自動アップロード
- ファイル変更の監視と自動再ビルド

### 2. コードの編集

- `src/desktop/`: デスクトップ版のコード
- `src/mobile/`: モバイル版のコード
- `src/config/`: 設定画面のコード（React）
- `src/helpers/`: ヘルパー関数
- `src/types/`: 型定義

### 3. ビルド

```bash
# プロダクションビルド
(devbox) /bin/bash /workspace/dev-kintone-plugin $ pnpm build

# JavaScriptのビルドのみ
(devbox) /bin/bash /workspace/dev-kintone-plugin $ pnpm build:js

# プラグインパッケージの作成のみ
(devbox) /bin/bash /workspace/dev-kintone-plugin $ pnpm build:package
```

ビルド成果物:

- `lib/`: ビルドされたJavaScript/CSSファイル
- `dist/plugin.zip`: kintoneにインストール可能なプラグインパッケージ

## コード品質

```bash
# リントチェック
(devbox) /bin/bash /workspace/dev-kintone-plugin $ pnpm lint

# リントの自動修正
(devbox) /bin/bash /workspace/dev-kintone-plugin $ pnpm fix
```

## プロジェクト構造

```
.
├── src/
│   ├── config/          # 設定画面（React）
│   │   ├── App.tsx      # メインコンポーネント
│   │   ├── index.tsx    # エントリーポイント
│   │   └── style.css    # スタイル
│   ├── desktop/         # デスクトップ版
│   │   ├── index.ts
│   │   └── style.css
│   ├── mobile/          # モバイル版
│   │   ├── index.ts
│   │   └── style.css
│   ├── helpers/         # ヘルパー関数
│   └── types/           # 型定義
├── public/
│   └── manifest.json    # プラグインマニフェスト
├── lib/                 # ビルド出力先
├── dist/                # プラグインパッケージ出力先
├── rsbuild.config.ts    # Rsbuild設定
└── tsconfig.json        # TypeScript設定
```

## カスタマイズ

### プラグイン情報の変更

`public/manifest.json`を編集して、プラグインの名前、説明、アイコンなどを変更してください。

### 機能の追加

1. 必要なファイル（`src/desktop/`, `src/mobile/`, `src/config/`）を編集
2. 必要に応じて`src/helpers/`にヘルパー関数を追加
3. `npm start`で変更を確認

## スクリプト一覧

| コマンド             | 説明                                             |
| -------------------- | ------------------------------------------------ |
| `pnpm start`         | 開発サーバー起動（ビルド + アップロード + 監視） |
| `pnpm build`         | プロダクションビルド                             |
| `pnpm build:js`      | JavaScriptのビルドのみ                           |
| `pnpm build:package` | プラグインパッケージの作成のみ                   |
| `pnpm lint`          | リントチェック                                   |
| `pnpm fix`           | リントの自動修正                                 |
| `pnpm upload`        | プラグインのアップロード                         |

## ライセンス

MIT

## 作者

- tasshi <tasshi.me@gmail.com>  
- [HiroyukiMakita](https://github.com/HiroyukiMakita) により一部変更

## 参考リンク

- [kintone developer network](https://developer.cybozu.io/hc/ja)
- [kintone JavaScript SDK](https://github.com/kintone/js-sdk)
- [Rsbuild](https://rsbuild.dev/)
- [React](https://react.dev/)
