#!/usr/bin/env python3
"""生きものの原本PNGから背景をぬいて、ゲームに埋めこむ WebP を作る。

原本の多くは「黒っぽい背景＋生きもののうしろに ぼんやりした光」という作り。
黒だけを消すと 光が四角く残り、明るさだけで消すと 黒い生きもの（アビスヌシザメ等）
まで消える。そこで「ふちから、なめらかな所だけを たどって ぬりつぶす」方式にした。
光のグラデーションは なめらかなので通りぬけ、生きものの輪郭は くっきりしているので
そこで止まる。
"""
import sys, os, json
import numpy as np
from PIL import Image, ImageFilter

def shifts(a):
    """上下左右にずらした4枚を返す（境界はもとの値で埋める）"""
    up    = np.vstack([a[:1],  a[:-1]])
    down  = np.vstack([a[1:],  a[-1:]])
    left  = np.hstack([a[:, :1],  a[:, :-1]])
    right = np.hstack([a[:, 1:],  a[:, -1:]])
    return up, down, left, right

def dilate(m):
    u, d, l, r = shifts(m)
    return m | u | d | l | r

def fill_holes(fg):
    """外からとどかない穴（生きものの内側）を前景に含める"""
    outside = np.zeros_like(fg)
    outside[0, :] = outside[-1, :] = True
    outside[:, 0] = outside[:, -1] = True
    outside &= ~fg
    for _ in range(4000):
        n = dilate(outside) & ~fg
        if (n == outside).all():
            break
        outside = n
    return ~outside

def largest_blob(fg, keep_ratio=0.06):
    """いちばん大きなかたまりと、その6%以上の大きさのかたまりだけ残す"""
    lab = np.zeros(fg.shape, np.int32)
    cur = 0
    sizes = {}
    todo = fg.copy()
    while todo.any():
        idx = np.argmax(todo)
        seed = np.zeros(fg.shape, bool)
        seed.flat[idx] = True
        while True:
            n = dilate(seed) & fg
            if (n == seed).all():
                break
            seed = n
        cur += 1
        lab[seed] = cur
        sizes[cur] = int(seed.sum())
        todo &= ~seed
        if cur > 40:
            break
    if not sizes:
        return fg
    big = max(sizes.values())
    keep = {k for k, v in sizes.items() if v >= big * keep_ratio}
    return np.isin(lab, list(keep))

def cutout(path, work=384, grad_th=7.0):
    im = Image.open(path).convert('RGBA')
    W, H = im.size
    a0 = np.asarray(im)[:, :, 3]
    if (a0 < 250).mean() > 0.05:          # もともと透過ずみの絵は そのまま使う
        return im

    sm = im.convert('RGB').resize((work, int(work * H / W)), Image.LANCZOS)
    sm = sm.filter(ImageFilter.GaussianBlur(1.1))
    arr = np.asarray(sm, np.float32)
    lum = arr @ np.array([0.299, 0.587, 0.114], np.float32)

    u, d, l, r = shifts(lum)
    grad = np.maximum.reduce([abs(lum - u), abs(lum - d), abs(lum - l), abs(lum - r)])
    # 色の変わり目も 見る（暗い背景の上の 暗い生きものは 明るさでは 出ない）
    cu, cd, cl, cr = shifts(arr)
    cgrad = np.maximum.reduce([abs(arr - x).max(axis=2) for x in (cu, cd, cl, cr)])
    edge = np.maximum(grad, cgrad * 0.8)

    passable = edge < grad_th
    bg = np.zeros(lum.shape, bool)
    bg[0, :] = bg[-1, :] = True
    bg[:, 0] = bg[:, -1] = True
    bg &= passable
    for _ in range(4000):
        n = dilate(bg) & passable
        if (n == bg).all():
            break
        bg = n
    bg = dilate(dilate(bg))               # 輪郭ぎわに 残る 背景を すこし 削る

    fg = fill_holes(~bg)
    fg = largest_blob(fg, 0.03)
    fg = fill_holes(fg)

    mask = Image.fromarray((fg * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    mask = mask.filter(ImageFilter.GaussianBlur(max(1.0, W / work * 0.8)))
    out = im.copy()
    out.putalpha(mask)
    return out

def trim(im, th=8):
    a = np.asarray(im)[:, :, 3]
    ys, xs = np.where(a > th)
    if len(xs) == 0:
        return im
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

def bake(src, dst, target_w, quality=82, flip=False):
    im = trim(cutout(src))
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    w, h = im.size
    sc = target_w / w
    im = im.resize((max(2, round(w * sc)), max(2, round(h * sc))), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=quality, method=6)
    return im.size

if __name__ == '__main__':
    src, dst, w = sys.argv[1], sys.argv[2], int(sys.argv[3])
    print(bake(src, dst, w))
