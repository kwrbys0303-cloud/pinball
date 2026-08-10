#!/usr/bin/env python3
"""fishing-v12.html 書きかえ その3：魚の数の下限・宝箱・レジェンド演出。"""
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

# ============================================================
# A. ランクごとの 下限を 満たす
# ============================================================
rep("""function topUpOcean(){
  let m = aliveFish();
  if (m < FISH_FLOOR){ addFish(FISH_FLOOR-m); banner('潮が かわった','魚が もどってきた'); }""",
    """/* ランクごとの 下限。★4・★5が 序盤に ゼロ、という さびしさを なくす。
   下限は 海の広さに 比例させる（せまい海で あふれさせないため）。
   ぜんたいの 上限（fishCap）は こえない */
function topUpRanks(){
  const c = [0,0,0,0,0];
  for (const f of fishPool) if (f.alive && !f.boss && !f.rare) c[f.rank]++;
  const k = areaK();
  for (let r=0;r<5;r++){
    let want = Math.round(RANK_MIN[r] * k) - c[r];
    let guard = 0;
    while (want > 0 && guard++ < 80 && aliveFish() < fishCap()){
      const made = spawnSchool(want, r);
      if (!made){ if (guard > 20) break; continue; }
      want -= made;
    }
  }
}
function topUpOcean(){
  let m = aliveFish();
  if (m < FISH_FLOOR){ addFish(FISH_FLOOR-m); banner('潮が かわった','魚が もどってきた'); }
  topUpRanks();""")

# ============================================================
# B. 宝箱：めぐみを 足し算に して、そのぶん 強くする
# ============================================================
# B-1. スコア倍率は かけ算の 別枠を やめ、カードと 同じ かっこの 中へ
rep("""  s.scoreMult = (1 + lv('score')*0.18) * fireM * allM * (1 + s.pend.scoreAdd)
              * (lv('rich')?2:1) * (lv('pray')?1.5:1) * (1 + s.gift.score)
              * s.tradeMul;""",
    """  // v12：たからばこの めぐみ（gift.score）を「べつの かけ算」から
  //      「カードと 同じ 足し算」に 移した。こうすると 火シナジーや
  //      よくばりセットと 二重に かかることが なくなるので、
  //      1つあたりを 強く しても 天井が こわれない
  s.scoreMult = (1 + lv('score')*0.18 + s.gift.score) * fireM * allM * (1 + s.pend.scoreAdd)
              * (lv('rich')?2:1) * (lv('pray')?1.5:1)
              * s.tradeMul;""")
# B-2. ワッカも 足し算（px）に
rep("""  let r = BASE_R + lv('radius')*20 + windA + s.pend.ring
        + (lv('net') ? 16 : 0) + (lv('ring') ? 70 : 0);
  r *= (lv('focus') ? 0.75 : 1) * allM * (1 + s.gift.ring);""",
    """  let r = BASE_R + lv('radius')*20 + windA + s.pend.ring
        + (lv('net') ? 16 : 0) + (lv('ring') ? 70 : 0) + s.gift.ring;
  r *= (lv('focus') ? 0.75 : 1) * allM;""")
# B-3. 上限を 足し算むけの 数字に
rep("""const CHEST_CAP  = { fish:20, score:0.30, ring:0.25 };""",
    """/* 足し算に なったので 数字の 意味が 変わった。
   score は「スコアの 足し算ぶん」（カードの がっぽりマネー 1段 = 0.18 と同じものさし）、
   ring は「ワッカの ふとさ そのもの（px）」。
   宝箱ビルドでも 高いスコアが 出るように、v11 より はっきり 強くした */
const CHEST_CAP  = { fish:34, score:1.30, ring:90 };""")
# B-4. 中身を 強く
rep("""      else if (c.kind==='fish'){
        P.fish = Math.min(PEND_CAP.fish, P.fish + 8);            // すぐに 8匹
        if (G.fish < CHEST_CAP.fish){ G.fish = Math.min(CHEST_CAP.fish, G.fish + 3);
          msgs.push('🐟 いま+8・毎投+3'); } else msgs.push('🐟 いま+8');
      }
      else if (c.kind==='score'){
        if (G.score < CHEST_CAP.score){ G.score = Math.round((G.score + 0.1)*10)/10;
          msgs.push('✨ スコアとお金 +0.1倍'); } else msgs.push('✨ もう いっぱい');
      }
      else if (c.kind==='ring'){
        if (G.ring < CHEST_CAP.ring){ G.ring = Math.round((G.ring + 0.1)*10)/10;
          msgs.push('🌊 ワッカ +0.1倍'); } else msgs.push('🌊 もう いっぱい');
      }
      else if (c.kind==='pull'){
        if (G.pull < PULL_CAP){ G.pull++; msgs.push('🧲 引きよせ +1'); }
        else msgs.push('🧲 もう いっぱい');
      }""",
    """      else if (c.kind==='fish'){
        P.fish = Math.min(PEND_CAP.fish, P.fish + 14);           // すぐに 14匹
        if (G.fish < CHEST_CAP.fish){ G.fish = Math.min(CHEST_CAP.fish, G.fish + 5);
          gift('🐟','うおのめぐみ','いま +14匹・毎投 +5匹'); }
        else gift('🐟','うおのめぐみ','いま +14匹');
      }
      else if (c.kind==='score'){
        if (G.score < CHEST_CAP.score){ G.score = Math.round((G.score + 0.15)*100)/100;
          gift('✨','しおのめぐみ','スコアとお金 +15%'); }
        else gift('✨','しおのめぐみ','もう いっぱい');
      }
      else if (c.kind==='ring'){
        if (G.ring < CHEST_CAP.ring){ G.ring = Math.min(CHEST_CAP.ring, G.ring + 11);
          gift('🌊','なみのめぐみ','ワッカ +11'); }
        else gift('🌊','なみのめぐみ','もう いっぱい');
      }
      else if (c.kind==='pull'){
        if (G.pull < PULL_CAP){ G.pull++; gift('🧲','いそのめぐみ','引きよせ +1'); }
        else gift('🧲','いそのめぐみ','もう いっぱい');
      }""")
# B-5. お金・券・ヌシの メッセージも「めぐみ」の形に
rep("""  const msgs = [], P = st.pend;""",
    """  // v12：たからばこの 中身は 「アイコン・名前・なかみ」の 3つに 分けて
  //      リザルトで 大きく 見せる（開けた うれしさを 出すため）
  const msgs = [], P = st.pend;
  const gift = (ic, nm, tx)=>msgs.push({ ic, nm, tx });""")
rep("""      if (c.kind==='coin'){ const g = chestCoin(); mo += g; msgs.push('¥'+g.toLocaleString()); }
      else if (c.kind==='ticket'){ if (i===0) msgs.push(gainTicket()); }""",
    """      if (c.kind==='coin'){ const g = chestCoin(); mo += g;
        gift('💰','小判','¥'+g.toLocaleString()); }
      else if (c.kind==='ticket'){ if (i===0){ const t = gainTicket();
        gift(t.startsWith('¥') ? '💰' : '🎫', t.startsWith('¥') ? '小判' : 'かけひき券', t); } }""")
rep("""    msgs.push(B.ic + ' ' + B.nm + ' ゲット！');
    if (B.chest) msgs.push('たからばこが わいた');""",
    """    msgs.push({ ic:B.ic, nm:B.nm, tx:'ゲット！', boss:1 });
    if (B.chest) msgs.push({ ic:'📦', nm:'たからばこ', tx:'ドッと わいた！' });""")
rep("""  if (rareN){ sfx.rare(); msgs.push(gainTicket()); }   // レア魚は 1投につき 券1枚""",
    """  if (rareN){ sfx.rare(); const t = gainTicket();
    msgs.push({ ic:t.startsWith('¥') ? '💰' : '🎫',
                nm:t.startsWith('¥') ? '小判' : 'かけひき券', tx:t, boss:1 }); }""")
# B-6. リザルトの 見せかた
rep("""  const rows = r.rows || [], nx = r.msgs.length;
  const bh = 46 + rows.length*24 + 40 + (nx ? nx*19 + 6 : 0);""",
    """  const rows = r.rows || [], nx = r.msgs.length;
  const bh = 46 + rows.length*24 + 40 + (nx ? nx*26 + 12 : 0);""")
rep("""  ctx.textAlign='left'; ctx.font='bold 13px sans-serif'; ctx.fillStyle='#ffd76a';
  r.msgs.forEach((m,i)=>ctx.fillText('📦 ' + m, 54, y+14+i*19));
  ctx.restore();""",
    """  // ---- たからばこの 中身。1つずつ 金の おびに のせて 大きく 出す ----
  y += 6;
  r.msgs.forEach((m,i)=>{
    const by = y + i*26, pop = clamp((r.t - 0.25 - i*0.11)*7, 0, 1);
    if (pop <= 0) return;
    ctx.save(); ctx.globalAlpha = Math.max(0,a) * pop;
    ctx.translate(240, by+11); ctx.scale(0.85+0.15*pop, 0.85+0.15*pop); ctx.translate(-240,-(by+11));
    const g = ctx.createLinearGradient(54, by, 426, by);
    g.addColorStop(0,'rgba(255,205,90,.30)'); g.addColorStop(.55,'rgba(255,235,160,.16)');
    g.addColorStop(1,'rgba(255,205,90,0)');
    ctx.fillStyle = g; roundPath(54, by, 372, 22, 7); ctx.fill();
    ctx.textAlign='left'; ctx.font='14px sans-serif'; ctx.fillStyle='#fff';
    ctx.fillText(m.ic, 60, by+16);
    ctx.font='bold 13px sans-serif'; ctx.fillStyle = m.boss ? '#ffd76a' : '#ffe9a8';
    ctx.fillText(m.nm, 84, by+16);
    ctx.textAlign='right'; ctx.font='bold 13px sans-serif'; ctx.fillStyle='#fff';
    ctx.fillText(m.tx, 420, by+16);
    ctx.restore();
  });
  ctx.restore();""")

# ============================================================
# C. レジェンドの 演出（ズームアップ＋音を 豪華に）
# ============================================================
rep("""  #legend .inner { text-align:center; animation:legendIn .55s cubic-bezier(.2,1.6,.4,1); }""",
    """  #legend .inner { text-align:center;
    animation:legendIn .5s cubic-bezier(.2,1.6,.4,1), legendZoom 2.1s .5s ease-out both; }
  /* うしろで まわる 光の すじ。出たときの 特別感を 上げる */
  #legend .inner::after { content:''; position:absolute; left:50%; top:50%;
    width:620px; height:620px; margin:-310px 0 0 -310px; border-radius:50%; z-index:-1;
    background:conic-gradient(from 0deg, rgba(255,225,150,.30) 0deg, transparent 22deg,
      rgba(255,225,150,.30) 45deg, transparent 67deg, rgba(255,225,150,.30) 90deg,
      transparent 112deg, rgba(255,225,150,.30) 135deg, transparent 157deg,
      rgba(255,225,150,.30) 180deg, transparent 202deg, rgba(255,225,150,.30) 225deg,
      transparent 247deg, rgba(255,225,150,.30) 270deg, transparent 292deg,
      rgba(255,225,150,.30) 315deg, transparent 337deg);
    -webkit-mask:radial-gradient(circle, transparent 14%, #000 42%, transparent 74%);
    mask:radial-gradient(circle, transparent 14%, #000 42%, transparent 74%);
    animation:legendRay 7s linear infinite; }""")
rep("""  @keyframes legendIn { 0%{transform:scale(.2) rotate(-12deg); opacity:0}
    60%{transform:scale(1.12) rotate(3deg); opacity:1} 100%{transform:scale(1) rotate(0)} }""",
    """  @keyframes legendIn { 0%{transform:scale(.2) rotate(-12deg); opacity:0}
    60%{transform:scale(1.12) rotate(3deg); opacity:1} 100%{transform:scale(1) rotate(0)} }
  /* 出たあと ゆっくり 寄っていく。最後に もう一段 グッと 寄せる */
  @keyframes legendZoom { 0%{transform:scale(1)} 62%{transform:scale(1.16)}
    76%{transform:scale(1.13)} 100%{transform:scale(1.42)} }
  @keyframes legendRay { to{transform:rotate(360deg)} }""")
rep("      setTimeout(drainNote,130); }, 1750);",
    "      setTimeout(drainNote,130); }, 2600);   // v12：ズームを 見せきる ぶん 長く")
rep("""  legend:()=>{ [523,659,784,1047,1319].forEach((f,i)=>setTimeout(()=>snd(f,.34,'triangle',.13),i*95)); },""",
    """  /* レジェンド。ただの 音階では 軽いので 3つ かさねる。
     ① 下から せり上がる うなり ② 主役の ファンファーレ ③ 上に のこる きらめき */
  legend:()=>{
    snd(70,1.5,'sawtooth',.10,240);                                    // ①
    [523,659,784,1047,1319,1568].forEach((f,i)=>{                      // ②
      setTimeout(()=>{ snd(f,.42,'triangle',.14); snd(f*2,.30,'sine',.06); }, i*88); });
    setTimeout(()=>{ [1047,1319,1568,2093].forEach((f,i)=>
      setTimeout(()=>snd(f,.5,'sine',.085), i*70)); }, 620);
    setTimeout(()=>{ snd(261,1.5,'triangle',.10); snd(392,1.5,'sine',.07);
                     snd(523,1.6,'sine',.06); }, 760);                 // ③ 和音で のばす
    for (let i=0;i<9;i++) setTimeout(()=>snd(1800+Math.random()*1900,.22,'sine',.045), 900+i*115);
  },""")

io.open(P, 'w', encoding='utf8').write(s)
print(f'part3: {count} 箇所')
