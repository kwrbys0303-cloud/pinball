#!/usr/bin/env python3
"""v12 の 処理を 軽くする。

実測（デスクトップ／魚806匹）:
  描画 2.85ms（★のきらめき 0.79ms ぶんを 含む）／引き上げ中 3.23ms
スマホは これの 5〜10倍 かかるので、ここが そのまま カクつきに なる。
魚を へらさずに 済むところから 順に 削る。
"""
import io

P = 'fishing-v12.html'
s = io.open(P, encoding='utf8').read()
n = 0

def rep(a, b, cnt=1):
    global s, n
    got = s.count(a)
    if got != cnt:
        raise SystemExit(f'[NG {got}回] {a[:90]!r}')
    s = s.replace(a, b)
    n += 1

# ------------------------------------------------------------
# 1. 空きスロットさがしを O(1) に
#    fishPool.find は 毎回 先頭から 探すので、魚が 800匹 いると
#    1匹 わかせるたびに 800回 まわる。大漁タイムで 400匹 わくと 32万回。
#    前回 止まった所から 続きを 見るだけで ほぼ 1回で 見つかる
# ------------------------------------------------------------
rep("""const fishPool = [], chestPool = [], bubPool = [], parPool = [];""",
    """const fishPool = [], chestPool = [], bubPool = [], parPool = [];
/* 空いている 魚のいれものを さがす。前に 見つけた ところから 続きを 見る */
let poolCur = 0;
function freeFish(){
  const len = fishPool.length;
  for (let i=0;i<len;i++){
    const f = fishPool[poolCur];
    poolCur = poolCur+1 < len ? poolCur+1 : 0;
    if (!f.alive) return f;
  }
  return null;
}""")
rep("""function spawnFishAt(rank, cx, cy, spread){
  const f = fishPool.find(o=>!o.alive); if (!f) return null;""",
    """function spawnFishAt(rank, cx, cy, spread){
  const f = freeFish(); if (!f) return null;""")
rep("""function spawnBoss(){
  const f = fishPool.find(o=>!o.alive); if (!f) return;""",
    """function spawnBoss(){
  const f = freeFish(); if (!f) return;""")
rep("""    const f = fishPool.find(o=>!o.alive); if (!f) return;
    const t = clamp(0.22 + Math.random()*0.5, 0.08, maxT()-0.06);""",
    """    const f = freeFish(); if (!f) return;
    const t = clamp(0.22 + Math.random()*0.5, 0.08, maxT()-0.06);""")

# ------------------------------------------------------------
# 2. 魚を 見る ループを 1本に
#    いままで 全スロット(1240個)を「ふつうの魚」「レア魚」「ヌシ」で
#    3回 なめていた。1回で 仕分ける
# ------------------------------------------------------------
rep("""  for (const f of fishPool)  if (f.alive && !f.boss && !f.rare) drawFish(f);
  for (const f of fishPool)  if (f.alive && f.rare) drawRare(f);
  for (const f of fishPool)  if (f.alive && f.boss) drawBoss(f);""",
    """  drawLater.length = 0;
  for (const f of fishPool){
    if (!f.alive) continue;
    if (f.rare || f.boss) drawLater.push(f);      // レア魚とヌシは いちばん手前
    else drawFish(f);
  }
  for (const f of drawLater) if (f.rare) drawRare(f);
  for (const f of drawLater) if (f.boss) drawBoss(f);""")
rep("""function draw(){
  atmoT += 0.016;""",
    """const drawLater = [];
function draw(){
  atmoT += 0.016;
  // ★のきらめきは 1匹ごとに 図形を ぬるので、★の魚が 300匹 いると
  // それだけで 描画が 3割 のびる。毎フレーム 一部だけを 光らせ、
  // 順ぐりに ずらす。見た目は 全体が チカチカして いるまま
  sparkStep = Math.max(1, Math.ceil((rankCnt[st.market.star]||0) / 45));
  sparkPhase = sparkStep > 1 ? (sparkPhase + 1) % sparkStep : 0;
  sparkI = 0;""")
rep("""let lite = false, liteMode = 'auto', frameAvg = 16.7;""",
    """let lite = false, liteMode = 'auto', frameAvg = 16.7;
let sparkStep = 1, sparkPhase = 0, sparkI = 0;""")
rep("""  if (star && !lite){                           // 星のきらめき（軽量モードでは 出さない）""",
    """  if (star && !lite && (sparkI++ % sparkStep) === sparkPhase){   // 星のきらめき""")

# ------------------------------------------------------------
# 3. 引きよせ の えらび方
#    毎回 全部の魚から 配列を 3つ 作って 並べかえていた。
#    まず ワッカの まわりだけ 集めてから 並べかえる
# ------------------------------------------------------------
rep("""    fishPool.filter(f=>f.alive && !f.caught && blinkPh(f)!==2)
      .map(f=>({ f, d:Math.hypot(f.x-p.x, f.y-p.y) }))
      .filter(o=>o.d < st.radius + PULL_RING)
      .sort((a,b)=>a.d-b.d).slice(0, st.pull)
      .forEach(o=>{ o.f.caught=true; o.f.miss=0; o.f.tx=p.x; o.f.ty=p.y; got.push(o.f); });""",
    """    const lim = st.radius + PULL_RING, lim2 = lim*lim, near = [];
    for (const f of fishPool){
      if (!f.alive || f.caught || blinkPh(f)===2) continue;
      const dx = f.x-p.x, dy = f.y-p.y, d2 = dx*dx + dy*dy;
      if (d2 < lim2) near.push({ f, d:d2 });          // 平方根は とらない（順番は 同じ）
    }
    near.sort((a,b)=>a.d-b.d);
    for (let i=0;i<near.length && i<st.pull;i++){
      const o = near[i];
      o.f.caught=true; o.f.miss=0; o.f.tx=p.x; o.f.ty=p.y; got.push(o.f);
    }""")

# ------------------------------------------------------------
# 4. 端末に あわせて 魚の 上限を 上げ下げする
#    速い端末は そのまま たくさん、おいつかない端末だけ 静かに へらす。
#    へらしたぶんは 投のはじめに（画面が 切りかわる ときに）だけ 引きあげるので、
#    遊んでいる さいちゅうに 魚が 消えることは ない
# ------------------------------------------------------------
rep("""const FISH_CAP    = 1100;   // v12：上限ひきあげ""",
    """const FISH_CAP    = 900;    // v12：上限ひきあげ（v11は620）
const CAP_MIN     = 0.60;   // おそい端末で ここまでは さがる""")
rep("""const fishCap = ()=>Math.round(FISH_CAP * areaK());""",
    """let capK = 1;
const fishCap = ()=>Math.round(FISH_CAP * areaK() * capK);""")
rep("""  frameAvg += (Math.min(60, raw) - frameAvg) * 0.06;
  if (liteMode === 'auto') lite = lite ? frameAvg > 19.5 : frameAvg > 24;""",
    """  frameAvg += (Math.min(60, raw) - frameAvg) * 0.06;
  if (liteMode === 'auto') lite = lite ? frameAvg > 19.5 : frameAvg > 24;
  // おいついていない ときは 魚の 上限を すこしずつ さげ、
  // 余裕が もどったら ゆっくり 上げなおす
  if (st){
    if (frameAvg > 26)      capK = Math.max(CAP_MIN, capK - 0.010);
    else if (frameAvg < 19) capK = Math.min(1, capK + 0.002);
  }""")
rep("""function topUpOcean(){
  let m = aliveFish();""",
    """function topUpOcean(){
  // 上限が さがっている ときは、投の きりかえで だけ 多いぶんを 引きあげる
  // （ランクの ひくい魚から。デカい魚は 残す）
  let over = aliveFish() - fishCap();
  if (over > 0){
    for (let r=0; r<5 && over>0; r++){
      for (const f of fishPool){
        if (over <= 0) break;
        if (f.alive && !f.boss && !f.rare && !f.caught && f.rank === r){ f.alive = false; over--; }
      }
    }
  }
  let m = aliveFish();""")

io.open(P, 'w', encoding='utf8').write(s)
print(f'{n} 箇所')
