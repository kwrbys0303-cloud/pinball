# ツリツリバースト をリンクで配る

スマホ（iPhone / Android）で、**リンクを踏むだけ**で遊べる形にしたものです。
iPad・パソコンは想定していません（縦画面専用）。

## 入っているファイル

| ファイル | なに |
|---|---|
| `index.html` | これ1つでゲームが動きます（絵も音も中に入っています／約1.8MB） |
| `manifest.webmanifest` | ホーム画面に追加したときの名前・アイコン・縦画面固定 |
| `sw.js` | 一度ひらけば、電波がなくても遊べるようにするもの |
| `icon-180.png` ほか | ホーム画面のアイコン |
| `fishing-v12.html` | ゲーム本体（元データ） |
| `build-mobile.py` | 元データから `index.html` を作りなおす道具 |

ゲームを直したいときは **`fishing-v12.html` を直して**、

```
python3 build-mobile.py
```

を走らせてください。`index.html` を直接いじると、次のビルドで消えます。

## GitHub Pages で公開する手順

1. GitHub でこのリポジトリを開く
2. **Settings**（歯車）→ 左メニューの **Pages**
3. Source を **Deploy from a branch** にする
4. Branch に `claude/fishing-game-design-yvyl39`、フォルダは `/ (root)` を選ぶ
5. **Save**

1〜2分待つと、Pages のページに URL が出ます。

```
https://kwrbys0303-cloud.github.io/pinball/
```

このリンクを送れば、相手はログインなしで遊べます。

> **注意：このリポジトリは今「プライベート」です。**
> 無料アカウントの場合、GitHub Pages はパブリックのリポジトリでしか使えません。
> Settings のいちばん下 → Change repository visibility → Public にすると使えます。
> （GitHub Pro なら、プライベートのままでも公開できます）

## ホーム画面に追加すると

アドレスバーが消えて、アプリのように全画面で開きます。

- **iPhone**：Safari で開く → 共有ボタン → 「ホーム画面に追加」
- **Android**：Chrome で開く → 右上の「︙」→ 「アプリをインストール」

## 更新したとき

`index.html` を push しなおせば、次にひらいたときに新しくなります。
`sw.js` は「通信できたら必ず最新を取りに行く」やり方にしてあるので、
古い版が残り続けることはありません。
