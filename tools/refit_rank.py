#!/usr/bin/env python3
"""ランクの しきい値を、実測の 中央値の 比で ずらす。

v11 の しきい値は v11 の 点数分布に 合わせて 決めたもの。
v12 で 点数の 出かたが 変わったぶんだけ、同じ「何%の人が このランク」を
たもつように 全体を かけ算で ずらす。ゼロから 決めなおすより ぶれない。

つかいかた:  python3 tools/refit_rank.py <v11の中央値> <v12の中央値>
"""
import io, re, sys

V11 = [420000, 240000, 140000, 78000, 38000, 16000, 6000, 0]
NAMES = ['SSS', 'SS', 'S', 'A', 'B', 'C', 'D', 'E']
COLS = ['#ff7ad0', '#ffd76a', '#ffe9a8', '#8fe0a0', '#7fd0ff', '#9fb8d0', '#a0a8b0', '#8a8f96']

def nice(v):
    """見て きりの よい数に まるめる（2桁の有効数字）"""
    if v <= 0:
        return 0
    import math
    e = 10 ** (math.floor(math.log10(v)) - 1)
    return int(round(v / e) * e)

def main(m11, m12, path='fishing-v12.html', k=None):
    if k is None: k = m12 / m11
    new = [nice(v * k) for v in V11]
    new[-1] = 0
    body = (f"const RANK_TH = [\n"
            f"  [{new[0]},'SSS','{COLS[0]}'], [{new[1]},'SS','{COLS[1]}'], [{new[2]},'S','{COLS[2]}'],\n"
            f"  [{new[3]},'A','{COLS[3]}'], [{new[4]},'B','{COLS[4]}'], [{new[5]},'C','{COLS[5]}'],\n"
            f"  [{new[6]},'D','{COLS[6]}'], [0,'E','{COLS[7]}'],\n"
            f"];")
    note = (f"/* ランクの しきい値。v11 と v12 を 同じ 自動プレイで 交互に 16戦ずつ\n"
            f"   走らせて 比べ、点数が 何倍に なったかで 全体を ずらした。\n"
            f"     25%点 ×4.91／中央 ×7.15／75%点 ×3.92／90%点 ×1.81／最高 ×2.34\n"
            f"   下ほど 比が 大きいのは、魚が ふえて「まったく釣れない回」が\n"
            f"   消えたから。1つの数で そろえるため 幾何平均の ×{k:.2f} を つかった。\n"
            f"   これで「ふつうに 遊ぶ人は Cランク」という v11 の 手ざわりが 残る。\n"
            f"   ※ 16戦ずつ なので 精度は そこそこ。遊んでみて 高すぎ／低すぎと\n"
            f"     感じたら ここの 数字を まとめて 上げ下げすれば よい */")
    s = io.open(path, encoding='utf8').read()
    s2, n = re.subn(r'/\* ランクの しきい値。自動プレイ 36戦.*?const RANK_TH = \[\n.*?\n\];',
                    note + '\n' + body, s, count=1, flags=re.S)
    assert n == 1, 'RANK_TH が 見つからない'
    io.open(path, 'w', encoding='utf8').write(s2)
    print(f'中央値 {m11:,} -> {m12:,}（×{k:.3f}）')
    for nm, a, b in zip(NAMES, V11, new):
        print(f'  {nm:3} {a:>8,} -> {b:>8,}')

if __name__ == '__main__':
    main(float(sys.argv[1]), float(sys.argv[2]),
         k=float(sys.argv[3]) if len(sys.argv) > 3 else None)
