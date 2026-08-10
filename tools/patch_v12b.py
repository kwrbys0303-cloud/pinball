#!/usr/bin/env python3
"""fishing-v12.html 書きかえ その2：名前と絵の 参照先を ステージごとに 切りかえる。"""
import io

P = 'fishing-v12.html'
s = io.open(P, encoding='utf8').read()
count = 0

def rep(old, new, n=1):
    global s, count
    got = s.count(old)
    if got != n:
        raise SystemExit(f'[NG {got}回 (期待{n}回)] {old[:100]!r}')
    s = s.replace(old, new)
    count += 1

# ---- さかなの逆襲メッセージ：RANKS[r].n → rn(r) ----
for a, b in [("`${RANKS[r].n}の にげ足 パワーアップ！`", "`${rn(r)}の にげ足 パワーアップ！`"),
             ("`${RANKS[r].n}の 耳 パワーアップ！`", "`${rn(r)}の 耳 パワーアップ！`"),
             ("`${RANKS[r].n}の 反しゃ神けい パワーアップ！`", "`${rn(r)}の 反しゃ神けい パワーアップ！`"),
             ("`${RANKS[r].n}が バラバラに なった！`", "`${rn(r)}が バラバラに なった！`"),
             ("`${RANKS[r].n}が 深いところへ にげこんだ！`", "`${rn(r)}が 深いところへ にげこんだ！`"),
             ("`${RANKS[r].n}が どんどん ふえる！`", "`${rn(r)}が どんどん ふえる！`"),
             ("`海が ${RANKS[r].n}だらけに なっていく！`", "`海が ${rn(r)}だらけに なっていく！`"),
             ("`${RANKS[r].n}が 分身を おぼえた！`", "`${rn(r)}が 分身を おぼえた！`"),
             ("`${RANKS[r].n}が 全力しっそうを おぼえた！`", "`${rn(r)}が 全力しっそうを おぼえた！`"),
             ("`${RANKS[r].n}が 点めつを おぼえた！`", "`${rn(r)}が 点めつを おぼえた！`"),
             ("`${RANKS[r].n}が しゅんかん移どうを おぼえた！`", "`${rn(r)}が しゅんかん移どうを おぼえた！`"),
             ("`💰 そのかわり ${RANKS[r].n}の 点数 ${FISH_MULT}ばい！`",
              "`💰 そのかわり ${rn(r)}の 点数 ${FISH_MULT}ばい！`")]:
    rep(a, b)

rep("    img: FISH_SPR[r], ic: u.ic, title: u.t(r), sub: u.s(r),",
    "    img: fspr(r), ic: u.ic, title: u.t(r), sub: u.s(r),")

# ---- 絵のキー ----
rep("const FISH_SPR  = ['iwashi','aji','tai','buri','maguro'];\n"
    "const BOSS_SPR  = { shark:'bshark', octo:'bocto', dragon:'bdragon' };\n"
    "const RARE_SPR  = { octo:'rocto', ray:'rray', puff:'rpuff' };\n",
    "")
rep("    const gs = sprAt(FISH_SPR[f.rank], s*2.9, 'gray', flip);",
    "    const gs = sprAt(fspr(f.rank), s*2.9, 'gray', flip);")
rep("  const spr = sprAt(FISH_SPR[f.rank], s*2.9, dull ? 'gray' : star ? 'star' : '', flip);",
    "  const spr = sprAt(fspr(f.rank), s*2.9, dull ? 'gray' : star ? 'star' : '', flip);")
rep("  const spr = sprAt(RARE_SPR[R.id], s*3.1, 'gold');",
    "  const spr = sprAt(R.spr, s*3.1, 'gold');")
rep("  const spr = sprAt(BOSS_SPR[B.id], s*3.1, 'gold');",
    "  const spr = sprAt(B.spr, s*3.1, 'gold');")
rep("""      if (f.boss){ o.spr = BOSS_SPR[st.bossType.id]; o.nm = st.bossType.nm;""",
    """      if (f.boss){ o.spr = st.bossType.spr; o.nm = st.bossType.nm;""")
rep("""      else if (f.rare){ o.spr = RARE_SPR[st.rareType.id]; o.nm = st.rareType.nm;""",
    """      else if (f.rare){ o.spr = st.rareType.spr; o.nm = st.rareType.nm;""")
rep("""      else { o.spr = FISH_SPR[f.rank]; o.nm = RANKS[f.rank].n + (f.clone ? '(分身)' : '');""",
    """      else { o.spr = fspr(f.rank); o.nm = rn(f.rank) + (f.clone ? '(分身)' : '');""")
rep("  for (let r=0;r<5;r++) rows.push({ spr:FISH_SPR[r], nm:RANKS[r].n, v:nowScore(r),",
    "  for (let r=0;r<5;r++) rows.push({ spr:fspr(r), nm:rn(r), v:nowScore(r),")
rep("  if (rare) rows.push({ spr:RARE_SPR[st.rareType.id], nm:st.rareType.nm,",
    "  if (rare) rows.push({ spr:st.rareType.spr, nm:st.rareType.nm,")
rep("  if (boss) rows.push({ spr:BOSS_SPR[st.bossType.id], nm:st.bossType.nm,",
    "  if (boss) rows.push({ spr:st.bossType.spr, nm:st.bossType.nm,")
rep("""    one('#ffb36a', B.ic, B.nm, B.tale, B.prize, BOSS_SPR[B.id],""",
    """    one('#ffb36a', B.ic, B.nm, B.tale, B.prize, B.spr,""")
rep("""    one('#b4e8ff', R.ic, R.nm, R.tale, RARE_PRIZE, RARE_SPR[R.id],""",
    """    one('#b4e8ff', R.ic, R.nm, R.tale, RARE_PRIZE, R.spr,""")
rep("""    h += `<div><span><img class="stF" src="${SPR_SRC[FISH_SPR[i]]}" alt=""> ${R.n}</span>`""",
    """    h += `<div><span><img class="stF" src="${SPR_SRC[fspr(i)]}" alt=""> ${rn(i)}</span>`""")
rep("""    return `<div class="${cls}"><img class="f" src="${SPR_SRC[FISH_SPR[i]]}" alt="">""",
    """    return `<div class="${cls}"><img class="f" src="${SPR_SRC[fspr(i)]}" alt="">""")

# ---- さかな市場：名前を ステージの魚から 組み立てる ----
rep("""const MARKETS = [
  { nm:'イワシの下剋上',   star:0, dull:4, mul:2.6 },
  { nm:'アジのむれ祭り',   star:1, dull:3, mul:2.4 },
  { nm:'タイのおでまし',   star:2, dull:0, mul:2.0 },
  { nm:'ブリ旋風',         star:3, dull:2, mul:1.8 },
  { nm:'マグロの時代',     star:4, dull:1, mul:1.7 },
];""",
    """/* 名前は ステージの魚の 名前から その場で 作る（「サンゴスズメの下剋上」など） */
const MARKETS = [
  { pat:'@の下剋上',   star:0, dull:4, mul:2.6 },
  { pat:'@のむれ祭り', star:1, dull:3, mul:2.4 },
  { pat:'@のおでまし', star:2, dull:0, mul:2.0 },
  { pat:'@せんぷう',   star:3, dull:2, mul:1.8 },
  { pat:'@の時代',     star:4, dull:1, mul:1.7 },
];
const mkNm = m => m.pat.replace('@', rn(m.star));""")
rep("""  h += `<div class="stSec">さかな市場　${s.market.nm}</div><div class="statGrid">`;""",
    """  h += `<div class="stSec">さかな市場　${mkNm(s.market)}</div><div class="statGrid">`;""")
rep("""     <div style="font-size:12px;opacity:.65;margin-top:5px">${st.stage.ic} ${st.stage.nm}　${st.market.nm}</div>`;""",
    """     <div style="font-size:12px;opacity:.65;margin-top:5px">${st.stage.ic} ${st.stage.nm}　${mkNm(st.market)}</div>`;""")

# ---- ヌシ・レア魚の 抽選を makeFoe に ----
rep("""    st.bossType = BOSSES[(Math.random()*BOSSES.length)|0];
    st.rareType = RARES[(Math.random()*RARES.length)|0];""",
    """    st.bossType = makeFoe('boss');
    st.rareType = makeFoe('rare');""")
rep("""  st.bossType = BOSSES[(Math.random()*BOSSES.length)|0];
  st.rareType = RARES[(Math.random()*RARES.length)|0];""",
    """  st.bossType = makeFoe('boss');
  st.rareType = makeFoe('rare');""")
# 初期値も つじつまを 合わせる（ステージが 決まる前に 参照されても 落ちないように）
rep("    bossType:BOSSES[0], rareType:RARES[0], objs:[],",
    "    bossType:Object.assign({nm:'',ic:'',tale:'',spr:'shB'},BOSSES[0]),\n"
    "    rareType:Object.assign({nm:'',ic:'',tale:'',spr:'shR'},RARES[0]), objs:[],")

io.open(P, 'w', encoding='utf8').write(s)
print(f'part2: {count} 箇所')
