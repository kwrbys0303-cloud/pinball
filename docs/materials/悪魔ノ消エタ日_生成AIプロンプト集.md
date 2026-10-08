# 「悪魔ノ消エタ日」生成AIプロンプト集（2026年10月8日）

背景画像と、場面1〜4の音源（BGM）を別のAIで作るためのプロンプト。
スライドの生徒の写真の枠（オープニング・エンディングなど）は別に空けておく。

## 共通の考え方
- 音源：ハ長調／イ短調。C・Am・F・G7 の4コードのみ。各コード最低1小節（遅い場面は2小節）。セリフの下で流すので音数少なく。
- 画像：全場面同じ絵のタッチ。人物・文字なし。下3分の1は字幕用に暗め・模様少なめ。
- プロンプトは英語（生成AIに通りやすい）。

---

## 音源（場面1〜4）

### 共通の一文（各プロンプトの後ろにつける）
```
Instrumental only, no vocals. Key of C major / A minor. Use ONLY these four chords: C, Am, F, G7 — no other chords. Each chord must last at least one full bar (4 beats). Steady tempo, clear downbeat, no tempo or key changes. Sparse arrangement that leaves space for spoken dialogue and a live ukulele group playing along. About 90 seconds, loopable.
```

### 場面1　王女の城（コミカル＋不穏）
コード進行（各1小節・104BPM）：C｜C｜Am｜Am｜F｜F｜G7｜G7｜Am｜Am｜F｜G7｜Am｜Am｜F｜G7｜
```
A comedic yet sinister royal march for a spoiled, cruel princess in her castle. Playful and mischievous on the surface, with an ominous undertone hinting at something dark. Pizzicato strings, bassoon, harpsichord, tuba bass, light glockenspiel accents, soft low string swells on the A minor bars. 104 BPM, 4/4.
Chord progression (one chord per bar): C | C | Am | Am | F | F | G7 | G7 | Am | Am | F | G7 | Am | Am | F | G7 | then repeat.
```
ウクレレ：1拍目と3拍目に「ジャン、ジャン」と短く切って弾く。

### 場面2　戦いの幕開け（10月8日 差し替え）
コード進行（各1小節・112BPM）：Am｜F｜C｜G7｜を最初から最後までくり返す。最初の4小節（約9秒）は静か、5小節目の太鼓の一発から戦いモード。
```
The opening of a battle in a fantasy story. It starts quiet and tense for the first 4 bars (about 9 seconds): soft low sustained strings and a quiet timpani roll. At bar 5, a big drum hit marks the moment the soldiers charge in, and the music switches into battle mode: driving staccato string ostinato, bold brass stabs, snare drum and deep war drums. Exciting and adventurous, with a slightly playful, comedic edge (this is a fun battle, not a scary one). Keep building energy toward the end and finish with a strong final hit on G7.
112 BPM, 4/4.
Chord progression (exactly one chord per bar, the same 4-bar pattern from start to finish): Am | F | C | G7 | Am | F | C | G7 | ... repeat.
Instrumental only, no vocals. Key of A minor / C major. Use ONLY these four chords: Am, F, C, G7 — no other chords. Each chord lasts exactly one full bar (4 beats). Steady tempo, clear downbeat, no tempo or key changes. No bongos or congas (live bongo will be added). Leave space for spoken dialogue and a live ukulele group playing along. About 60 seconds.
```
ウクレレ：最初の4小節は1小節に1回そっと。5小節目で大塚のボンゴ「ドン！」を音源の太鼓に重ね、家来たちが駆けこむ。そのあとはダウン・アップ（セリフの間は1拍目だけ）。最後のG7の一発を「はじめ！」の直前に合わせる。

### 場面3　戦い（テンポよく・うきうきするコミカルな戦い）
コード進行（各1小節・132BPM）：Am｜F｜G7｜C｜×2 → F｜G7｜Am｜Am｜→ くり返し
```
A fun, bouncy, comedic battle scene — exciting but playful, like a cartoon action chase. Brass stabs, snare drum march rhythm, pizzicato strings, quick xylophone runs. Upbeat and cheerful. IMPORTANT: no bongos, no congas, no busy hand percussion — leave space for live bongo and ukulele. 132 BPM, 4/4.
Chord progression (one chord per bar): Am | F | G7 | C | Am | F | G7 | C | F | G7 | Am | Am | then repeat.
```
ウクレレ：ダウン・アップの速いストローク。ボンゴが主役。最後の「ジャーン！！」は生演奏なので、音源はその手前でフェードアウト。

### 場面4　はんぶんこ（静かで真剣な対峙）
コード進行（各2小節・60BPM）：Am｜Am｜F｜F｜C｜C｜G7｜G7｜（G7で終わり、糸の前奏へ）
```
A quiet, serious confrontation between a cornered princess and a lonely swordsman. Still, tense, but with a hint of tenderness. Very sparse: soft solo piano with long sustained strings, lots of space between notes. No drums. 60 BPM, 4/4.
Chord progression (each chord held for two bars): Am | Am | F | F | C | C | G7 | G7 | — end unresolved on G7.
```
ウクレレ：基本は弾かない。「おいしい。」の直前などに C を1回だけそっと鳴らす。

### 場面5
いきものがかり「YELL」（ピアノ）を流すので作らない。

---

## 背景画像（人物なし・風景中心）

### 共通の一文（各プロンプトの後ろにつける）
```
Wide 16:9 storybook fantasy illustration, painterly, soft lighting, rich colors, family-friendly and not scary. No people, no characters, no faces, no human silhouettes, no text, no letters, no logos. Keep the lower third of the image simple and slightly darker so white subtitles are easy to read.
```

### プロローグ・題名
```
A distant fantasy kingdom at twilight. A castle on a hill under a deep purple sky with the first stars appearing. A faint dark mist drifts around the castle, hinting at a hidden curse. Mysterious and beautiful.
```

### 場面1　王女の城
```
A grand royal throne room. A golden throne at the end of a long table piled high with sweets — donuts, puddings, cakes — and many empty chairs. Candles and red velvet curtains, luxurious, but cold purple light from tall windows and deep shadows make it feel lonely and slightly sinister.
```

### 場面2　ひとりの剣士
```
A windswept rocky hill at the border of a neighboring kingdom. A single large flat rock, dry grass bending in the wind, one bare tree, grey clouds. A castle silhouette far away on the horizon. Dark storm clouds gather on one side of the sky, as if a battle is coming. Lonely and quiet.
```

### 場面3　戦い
```
The same windswept hill, now full of energy: a dramatic sky with sunbeams breaking through moving clouds, grass and dust swirling in the wind. Bright, bold colors, exciting adventure mood.
```

### 場面4　はんぶんこ
```
The same hill at dusk, very quiet. Moonlight shines down on the large flat rock like a spotlight. Deep blue tones, still air, a few fireflies. Calm, serious, and gentle.
```

### 場面5　新しい道
```
Sunrise. A winding country road leads from the hill across green fields toward a small, warmly lit town in the distance. Golden morning light, hopeful and warm, the road continuing far ahead.
```

---

## コツ
- 音源：指定外のコードが混ざることがある。ウクレレで C・Am・F・G7 を合わせて確かめ、ずれたら作り直すか、その部分を使わない。
- 画像：場面2〜4は同じ丘。場面2を先に作り、それを参考画像にして天気・時間帯だけ変えると場所がつながる。
- 画像のNG指定欄があれば：people, person, character, face, text, watermark, blood
