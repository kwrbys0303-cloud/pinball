#!/usr/bin/env python3
"""焼いた WebP を fishing-v12.html に 埋めこむ。

・BG_SRC の moon / dragon / abyss を 新しい絵に さしかえる
・SPR_SRC から 使わなくなった 魚5種・ヌシ3種・レア魚3種を 消し、
  ステージごとの 49体を 入れる
"""
import base64, os, re, sys

ROOT = os.path.join(os.path.dirname(__file__), '..')
SPR = os.path.join(ROOT, 'build', 'spr')
BG = os.path.join(ROOT, 'build', 'bg')
SIDS = ['sh', 'tw', 'mo', 'dr', 'sk', 'ab', 'ru']
DROP = ['iwashi', 'aji', 'tai', 'buri', 'maguro',
        'bshark', 'bocto', 'bdragon', 'rocto', 'rray', 'rpuff']

def uri(path):
    with open(path, 'rb') as f:
        return 'data:image/webp;base64,' + base64.b64encode(f.read()).decode()

def main(path):
    s = open(path, encoding='utf8').read()
    before = len(s)

    # ---- 背景 3枚 ----
    for name in ('moon', 'dragon', 'abyss'):
        u = uri(os.path.join(BG, name + '.webp'))
        s, n = re.subn(r"(\n  %s: ')[^']*(')" % name, lambda m: m.group(1) + u + m.group(2),
                       s, count=1)
        assert n == 1, name

    # ---- 使わない魚を 消す ----
    for k in DROP:
        s, n = re.subn(r"\n  %s: '[^']*',?" % k, '', s, count=1)
        assert n == 1, k

    # ---- 49体を 入れる ----
    lines = []
    for sid in SIDS:
        for key in [f'{sid}{i}' for i in range(1, 6)] + [sid + 'R', sid + 'B']:
            lines.append("  %s: '%s'," % (key, uri(os.path.join(SPR, key + '.webp'))))
    block = '\n'.join(lines)
    s, n = re.subn(r"(const SPR_SRC = \{\n)", lambda m: m.group(1) + block + '\n', s, count=1)
    assert n == 1
    open(path, 'w', encoding='utf8').write(s)
    print(f'{before/1024:.0f}KB -> {len(s)/1024:.0f}KB')

if __name__ == '__main__':
    main(sys.argv[1])
