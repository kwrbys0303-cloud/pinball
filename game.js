// Pinball Game - Flipper Mechanics
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game constants
const GRAVITY = 0.3;
const FRICTION = 0.99;
const BALL_RADIUS = 10;
const FLIPPER_LENGTH = 70;
const FLIPPER_WIDTH = 12;

// Flipper angle settings
const FLIPPER_REST_ANGLE = 0.75;      // 静止角度（緩やか）
const FLIPPER_ACTIVE_ANGLE = -0.75;   // アクティブ角度
const FLIPPER_SPEED = 0.3;            // フリッパーの回転速度

// Launch power settings
const LAUNCH_POWER = 25;              // 最大パワー

// Ball state
let ball = {
    x: canvas.width / 2,
    y: 100,
    vx: 0,
    vy: 0,
    radius: BALL_RADIUS
};

// Flipper class
class Flipper {
    constructor(x, y, isLeft) {
        this.x = x;
        this.y = y;
        this.isLeft = isLeft;
        this.angle = isLeft ? FLIPPER_REST_ANGLE : -FLIPPER_REST_ANGLE;
        this.targetAngle = this.angle;
        this.isActive = false;
        this.justActivated = false;  // ボタンを押した瞬間かどうか
    }

    activate() {
        if (!this.isActive) {
            this.justActivated = true;  // 最初の押下を記録
        }
        this.isActive = true;
        this.targetAngle = this.isLeft ? FLIPPER_ACTIVE_ANGLE : -FLIPPER_ACTIVE_ANGLE;
    }

    deactivate() {
        this.isActive = false;
        this.targetAngle = this.isLeft ? FLIPPER_REST_ANGLE : -FLIPPER_REST_ANGLE;
    }

    update() {
        // フリッパーの角度を徐々に目標に近づける
        const angleDiff = this.targetAngle - this.angle;
        this.angle += angleDiff * FLIPPER_SPEED;
    }

    // フリッパーの先端位置を取得
    getTipPosition() {
        const tipX = this.x + Math.cos(this.angle) * FLIPPER_LENGTH * (this.isLeft ? 1 : -1);
        const tipY = this.y + Math.sin(this.angle) * FLIPPER_LENGTH;
        return { x: tipX, y: tipY };
    }

    // 発射角度を計算（拡張範囲: ±0.6 + t*1.4）
    getLaunchAngle(t) {
        // tはボールがフリッパーのどの位置にあるか（0=根元、1=先端）
        // 発射角度の範囲を拡大
        const baseAngle = this.isLeft ? -Math.PI / 2 : -Math.PI / 2;
        const spreadRange = 0.6 + t * 1.4;  // 位置に応じて範囲拡大

        if (this.isLeft) {
            // 左フリッパー: 右方向にも発射可能（-PI/2を中心に広い範囲）
            return baseAngle + spreadRange * (1 - t * 0.5);
        } else {
            // 右フリッパー: 左方向にも発射可能
            return baseAngle - spreadRange * (1 - t * 0.5);
        }
    }

    // ボールとの当たり判定と発射処理
    checkCollision(ball) {
        const tip = this.getTipPosition();

        // フリッパーのライン上での最近点を計算
        const dx = tip.x - this.x;
        const dy = tip.y - this.y;
        const len = Math.sqrt(dx * dx + dy * dy);
        const nx = dx / len;
        const ny = dy / len;

        // ボールからフリッパーの根元への相対位置
        const bx = ball.x - this.x;
        const by = ball.y - this.y;

        // フリッパーライン上への射影
        const proj = bx * nx + by * ny;
        const t = Math.max(0, Math.min(1, proj / len));

        // 最近点
        const closestX = this.x + nx * proj;
        const closestY = this.y + ny * proj;

        // 距離計算
        const distX = ball.x - closestX;
        const distY = ball.y - closestY;
        const dist = Math.sqrt(distX * distX + distY * distY);

        // 衝突判定（フリッパーの幅を考慮）
        if (dist < ball.radius + FLIPPER_WIDTH / 2 && proj >= 0 && proj <= len) {
            // 押した瞬間の即時発射処理
            if (this.justActivated) {
                this.justActivated = false;

                // 発射角度を計算（拡張範囲）
                const launchAngle = this.getLaunchAngle(t);

                // 最大パワーで発射
                ball.vx = Math.cos(launchAngle) * LAUNCH_POWER;
                ball.vy = Math.sin(launchAngle) * LAUNCH_POWER;

                // ボールをフリッパーから離す
                const pushDist = ball.radius + FLIPPER_WIDTH / 2 + 5;
                ball.x = closestX + (distX / dist) * pushDist;
                ball.y = closestY + (distY / dist) * pushDist;

                return true;
            }

            // 通常の反発処理（フリッパーが動いている場合）
            const pushDist = ball.radius + FLIPPER_WIDTH / 2 + 1;
            ball.x = closestX + (distX / dist) * pushDist;
            ball.y = closestY + (distY / dist) * pushDist;

            // フリッパーの回転による速度を加算
            if (this.isActive) {
                const rotSpeed = (this.targetAngle - this.angle) * 15;
                const perpX = -ny * rotSpeed;
                const perpY = nx * rotSpeed;
                ball.vx += perpX * (this.isLeft ? 1 : -1);
                ball.vy += perpY;
            }

            // 法線方向の反発
            const normalX = distX / dist;
            const normalY = distY / dist;
            const dotProduct = ball.vx * normalX + ball.vy * normalY;

            if (dotProduct < 0) {
                ball.vx -= 2 * dotProduct * normalX * 0.8;
                ball.vy -= 2 * dotProduct * normalY * 0.8;
            }

            return true;
        }

        return false;
    }

    draw() {
        const tip = this.getTipPosition();

        ctx.save();
        ctx.strokeStyle = this.isActive ? '#ff6b6b' : '#e94560';
        ctx.lineWidth = FLIPPER_WIDTH;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(tip.x, tip.y);
        ctx.stroke();

        // 支点を描画
        ctx.fillStyle = '#16213e';
        ctx.beginPath();
        ctx.arc(this.x, this.y, FLIPPER_WIDTH / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

// フリッパーの作成
const leftFlipper = new Flipper(100, canvas.height - 80, true);
const rightFlipper = new Flipper(canvas.width - 100, canvas.height - 80, false);

// 壁の描画
function drawWalls() {
    ctx.fillStyle = '#0f3460';
    // 左壁
    ctx.fillRect(0, 0, 20, canvas.height);
    // 右壁
    ctx.fillRect(canvas.width - 20, 0, 20, canvas.height);
    // 上壁
    ctx.fillRect(0, 0, canvas.width, 20);
}

// ボールの更新
function updateBall() {
    // 重力
    ball.vy += GRAVITY;

    // 摩擦
    ball.vx *= FRICTION;
    ball.vy *= FRICTION;

    // 位置更新
    ball.x += ball.vx;
    ball.y += ball.vy;

    // 壁との衝突
    if (ball.x - ball.radius < 20) {
        ball.x = 20 + ball.radius;
        ball.vx *= -0.8;
    }
    if (ball.x + ball.radius > canvas.width - 20) {
        ball.x = canvas.width - 20 - ball.radius;
        ball.vx *= -0.8;
    }
    if (ball.y - ball.radius < 20) {
        ball.y = 20 + ball.radius;
        ball.vy *= -0.8;
    }

    // 画面下に落ちたらリセット
    if (ball.y > canvas.height + 50) {
        resetBall();
    }
}

// ボールのリセット
function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = 100;
    ball.vx = (Math.random() - 0.5) * 4;
    ball.vy = 0;
}

// ボールの描画
function drawBall() {
    ctx.fillStyle = '#f1f1f1';
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();

    // ボールの光沢
    ctx.fillStyle = 'rgba(255,255,255,0.3)';
    ctx.beginPath();
    ctx.arc(ball.x - 3, ball.y - 3, ball.radius / 3, 0, Math.PI * 2);
    ctx.fill();
}

// キー入力処理
const keys = {};

document.addEventListener('keydown', (e) => {
    keys[e.key] = true;

    // 左フリッパー
    if (e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') {
        leftFlipper.activate();
    }
    // 右フリッパー
    if (e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') {
        rightFlipper.activate();
    }
    // ボール発射
    if (e.key === ' ') {
        if (ball.y > canvas.height) {
            resetBall();
        }
    }
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;

    // 左フリッパー
    if (e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') {
        leftFlipper.deactivate();
    }
    // 右フリッパー
    if (e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') {
        rightFlipper.deactivate();
    }
});

// ゲームループ
function gameLoop() {
    // 背景クリア
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 壁の描画
    drawWalls();

    // フリッパーの更新と描画
    leftFlipper.update();
    rightFlipper.update();
    leftFlipper.draw();
    rightFlipper.draw();

    // フリッパーとの衝突判定
    leftFlipper.checkCollision(ball);
    rightFlipper.checkCollision(ball);

    // ボールの更新と描画
    updateBall();
    drawBall();

    requestAnimationFrame(gameLoop);
}

// ゲーム開始
gameLoop();
