#!/usr/bin/env python3
"""manifest.json を読んで、49体ぶんの切りぬき WebP を作る。

ゲーム中の大きさは ランクで 変える（★1は とても小さく、★5・レア・ヌシは 大きく）。
焼く幅は「ゲームで いちばん大きく 出る幅の 約2倍」。それ以上は 見た目が
変わらないのに ファイルだけ 太る。
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cutout import bake

ROOT = os.path.join(os.path.dirname(__file__), '..')
ASSETS = os.path.join(ROOT, 'assets', 'creatures')
OUT = os.path.join(ROOT, 'build', 'spr')

# ステージid → ゲーム本体のステージid
SID = {'shallow':'sh', 'twin':'tw', 'moon':'mo', 'dragon':'dr',
       'sky':'sk', 'abyss':'ab', 'ruins':'ru'}
# ランク別の 焼く幅（px）と 画質
W_RANK = {1:(40,66), 2:(64,66), 3:(94,66), 4:(122,68), 5:(152,68)}
W_RARE = (152, 70)
W_BOSS = (184, 70)

# 右をむいている絵。焼くときに 左右を ひっくり返す（本体は「絵は左むき」が前提）
FLIP = set()

def main():
    os.makedirs(OUT, exist_ok=True)
    man = json.load(open(os.path.join(ASSETS, 'manifest.json'), encoding='utf8'))
    total = 0
    rows = []
    for stg in man['stages']:
        sid = SID[stg['id']]
        jobs = [(f"{sid}{f['rank']}", f['file'], W_RANK[f['rank']], f['name'])
                for f in stg['fish']]
        jobs.append((f"{sid}R", stg['rare']['file'], W_RARE, stg['rare']['name']))
        jobs.append((f"{sid}B", stg['boss']['file'], W_BOSS, stg['boss']['name']))
        for key, src, (w, q), nm in jobs:
            dst = os.path.join(OUT, key + '.webp')
            size = bake(os.path.join(ASSETS, src), dst, w, quality=q,
                        flip=(key in FLIP))
            n = os.path.getsize(dst)
            total += n
            rows.append((key, nm, size, n))
    for k, nm, sz, n in rows:
        print(f'{k:5} {nm:22} {sz[0]:4}x{sz[1]:<4} {n/1024:6.1f}KB')
    print(f'--- {len(rows)}体 合計 {total/1024:.0f}KB（base64で約{total*1.34/1024:.0f}KB）')

if __name__ == '__main__':
    main()
