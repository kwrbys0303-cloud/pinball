#!/usr/bin/env python3
"""
fishing-v12.html から スマホ配布用の index.html を つくる。

ゲームの中身は 1文字も 変えない。まわりに スマホ用の 上着を 着せるだけ:
  - iPhone / Android の 画面まわりの おまじない（meta タグ）
  - ホーム画面に 追加したときの アイコンと 名前
  - 画面を 消させない・音を もどす・二本指で 拡大させない
  - 一度 ひらけば 電波が なくても あそべる（sw.js）

つかいかた:  python3 build-mobile.py
"""
import re, sys, pathlib

SRC = pathlib.Path('fishing-v12.html')
OUT = pathlib.Path('index.html')

HEAD = '''<!DOCTYPE html>
<!--
  ツリツリバースト 〜さかなの逆襲〜  スマホ配布版
  ============================================================
  中身は fishing-v12.html と 同じ。build-mobile.py で つくっています。
  直すときは fishing-v12.html を 直して、もう一度 build-mobile.py を
  走らせてください。ここを 直しても つぎの ビルドで 消えます。
-->
<html lang="ja">
<head>
<meta charset="UTF-8">
<!-- viewport-fit=cover：iPhone の 出っぱり(ノッチ)の 下まで 黒でうめる -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#05121f">
<meta name="color-scheme" content="dark">
<meta name="description" content="12投で どこまで いけるか。ワンタップで あそべる 釣りゲーム。">
<!-- ホーム画面に ついか したとき 全画面で ひらく -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="ツリツリバースト">
<!-- 数字を 電話番号だと かんちがい されないように -->
<meta name="format-detection" content="telephone=no, address=no, email=no">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="manifest" href="manifest.webmanifest">
<title>ツリツリバースト 〜さかなの逆襲〜</title>
<script>window.TSURI_STANDALONE = true;</script>
'''

SHELL = '''
<script>
/* ============================================================
   スマホ用の 上着。ゲームの 中身には さわらない
   ============================================================ */
(function(){
  'use strict';

  /* --- 二本指ひろげの 拡大を 止める ---
     iOS の Safari は user-scalable=no を 見てくれないので 自分で 止める。
     文字を 打つところ だけは じゃま しない。
     すばやい 2回たたき の 拡大は CSS の touch-action に まかせている。
     ここで touchend を 止めると、カードを 選ぶ タップ（click）まで
     いっしょに 消えてしまい、えらべなく なることが あるため */
  const isField = el => el && el.closest &&
    el.closest('input, textarea, [contenteditable]');
  document.addEventListener('gesturestart',  e=>{ if(!isField(e.target)) e.preventDefault(); }, {passive:false});
  document.addEventListener('gesturechange', e=>{ if(!isField(e.target)) e.preventDefault(); }, {passive:false});
  document.addEventListener('gestureend',    e=>{ if(!isField(e.target)) e.preventDefault(); }, {passive:false});

  /* --- あそんでいる あいだ 画面を 消させない ---
     ためる ために 長おし するので、ほうっておくと 画面が 暗くなる */
  let wake = null;
  async function keepAwake(){
    try {
      if ('wakeLock' in navigator && document.visibilityState === 'visible' && !wake){
        wake = await navigator.wakeLock.request('screen');
        wake.addEventListener('release', ()=>{ wake = null; });
      }
    } catch(e){ wake = null; }
  }

  /* --- ホーム画面に もどって また ひらいたとき 音を もどす ---
     iPhone は うらに まわると 音の箱が とまるので、起こしてやる */
  function wakeAudio(){
    try { if (window.actx && actx.state === 'suspended') actx.resume().catch(()=>{}); } catch(e){}
  }
  document.addEventListener('visibilitychange', ()=>{
    if (document.visibilityState === 'visible'){ keepAwake(); wakeAudio(); }
  });
  document.addEventListener('pointerdown', ()=>{ keepAwake(); wakeAudio(); }, {passive:true});
  keepAwake();

  /* --- 一度 ひらけば 電波が なくても あそべる ---
     「通信できたら いつも 最新、だめなら 前のもの」。
     キャッシュ優先に すると 新しい版に なかなか 入れかわらない */
  if (window.TSURI_STANDALONE && 'serviceWorker' in navigator && window.isSecureContext){
    window.addEventListener('load', ()=>{
      navigator.serviceWorker.register('sw.js').catch(()=>{});
    });
  }
})();
</script>
'''


def main():
    if not SRC.exists():
        sys.exit(f'{SRC} が 見つかりません')
    s = SRC.read_text(encoding='utf-8')

    m = re.search(r'<style>.*?</style>', s, re.S)
    body = re.search(r'<body>(.*?)</body>', s, re.S)
    if not m or not body:
        sys.exit('もとの ファイルの かたちが ちがいます')

    css = m.group(0)
    # 画面ぜんたいの あつかい。指ではらって ページが 動かないように する
    css = css.replace(
        '  html,body { width:100%; height:100%; overflow:hidden; background:#05121f;',
        '  html,body { width:100%; height:100%; overflow:hidden; background:#05121f;\n'
        '    position:fixed; inset:0; overscroll-behavior:none;\n'
        '    -webkit-tap-highlight-color:transparent; -webkit-touch-callout:none;\n'
        '    -webkit-user-select:none; -webkit-text-size-adjust:100%;',
        1)
    if 'overscroll-behavior' not in css:
        sys.exit('CSS の さしこみに 失敗しました')

    out = HEAD + css + '\n</head>\n<body>' + body.group(1).rstrip() + '\n' + SHELL + '</body>\n</html>\n'
    OUT.write_text(out, encoding='utf-8')
    print(f'{OUT} を つくりました（{len(out)//1024} KB）')


if __name__ == '__main__':
    main()
