"""
games.py - MindMate Interactive Entertainment & Wellness Mini-Games Hub
Contains HTML5 Canvas + Web Audio API powered interactive games, ambient sound mixer,
virtual mood pet companion (Mochi), daily spin wheel, fortune cookie, kaleidoscope painter,
glow snake, chime piano, rhythm harmony game, crystal ball oracle, zen darts, and mood tarot.
"""

def get_spin_wheel_widget():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 15px; font-family: 'Inter', system-ui, sans-serif;
        background: linear-gradient(135deg, #1e1b4b, #0f172a); color: white;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        min-height: 480px; overflow: hidden;
    }
    .wheel-box { position: relative; width: 320px; height: 320px; margin: 10px 0; }
    #wheelCanvas { width: 100%; height: 100%; border-radius: 50%; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .wheel-pointer {
        position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
        font-size: 32px; z-index: 10; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.4));
    }
    .btn-spin {
        background: linear-gradient(135deg, #f43f5e, #fb923c); color: white;
        border: none; padding: 12px 35px; border-radius: 25px; font-weight: 800;
        font-size: 16px; cursor: pointer; box-shadow: 0 6px 20px rgba(244,63,94,0.4);
        transition: transform 0.15s; margin-top: 15px;
    }
    .btn-spin:hover { transform: scale(1.06); }
    .prize-result {
        margin-top: 12px; font-size: 16px; font-weight: 700; color: #fef08a;
        min-height: 24px; text-align: center;
    }
    </style>
    </head>
    <body>
    <div class="wheel-box">
        <div class="wheel-pointer">🔻</div>
        <canvas id="wheelCanvas" width="320" height="320"></canvas>
    </div>
    <button class="btn-spin" id="spinBtn" onclick="spinWheel()">🎡 Spin Daily Wheel!</button>
    <div class="prize-result" id="prizeText">Spin to win your daily wellness boost!</div>

    <script>
    const canvas = document.getElementById('wheelCanvas');
    const ctx = canvas.getContext('2d');
    const prizes = [
        "🌟 +50 Wellness XP",
        "🫁 5 Deep Breaths",
        "💧 Drink Water",
        "💖 Self-Compassion",
        "🎧 Favorite Song",
        "🌸 Smile in Mirror",
        "✨ +100 Big XP",
        "🧘 1 Min Stillness"
    ];
    const colors = ["#f43f5e", "#8b5cf6", "#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#06b6d4", "#6366f1"];
    const numPrizes = prizes.length;
    const arc = (Math.PI * 2) / numPrizes;

    let angle = 0, isSpinning = false;

    function drawWheel() {
        ctx.clearRect(0, 0, 320, 320);
        for (let i = 0; i < numPrizes; i++) {
            const startAngle = angle + i * arc;
            ctx.beginPath();
            ctx.fillStyle = colors[i];
            ctx.moveTo(160, 160);
            ctx.arc(160, 160, 150, startAngle, startAngle + arc);
            ctx.lineTo(160, 160);
            ctx.fill();
            ctx.stroke();

            // Text
            ctx.save();
            ctx.fillStyle = "white";
            ctx.font = "bold 11px Inter, sans-serif";
            ctx.translate(160, 160);
            ctx.rotate(startAngle + arc / 2);
            ctx.textAlign = "right";
            ctx.fillText(prizes[i], 135, 4);
            ctx.restore();
        }
        ctx.beginPath();
        ctx.arc(160, 160, 22, 0, Math.PI * 2);
        ctx.fillStyle = "#0f172a";
        ctx.fill();
        ctx.lineWidth = 3;
        ctx.strokeStyle = "white";
        ctx.stroke();
    }

    drawWheel();

    function spinWheel() {
        if (isSpinning) return;
        isSpinning = true;
        document.getElementById('prizeText').textContent = "Spinning...";
        
        const spinRounds = 5 + Math.random() * 4;
        const totalRotation = spinRounds * Math.PI * 2 + Math.random() * Math.PI * 2;
        const duration = 4000;
        const start = performance.now();
        const initialAngle = angle;

        function animate(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const easeOut = 1 - Math.pow(1 - progress, 3);
            angle = initialAngle + totalRotation * easeOut;
            drawWheel();

            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                isSpinning = false;
                const normalizedAngle = (Math.PI * 2 - (angle % (Math.PI * 2)) - Math.PI / 2 + Math.PI * 2) % (Math.PI * 2);
                const prizeIndex = Math.floor(normalizedAngle / arc) % numPrizes;
                document.getElementById('prizeText').textContent = `🎉 You won: ${prizes[prizeIndex]}!`;
            }
        }
        requestAnimationFrame(animate);
    }
    </script>
    </body>
    </html>
    """


def get_bubble_wrap_game():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 15px; font-family: 'Inter', system-ui, sans-serif;
        background: radial-gradient(circle at 50% 10%, #1e293b, #0f172a);
        color: white; display: flex; flex-direction: column; align-items: center;
        min-height: 680px; overflow: hidden;
    }
    .header {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; max-width: 680px; margin-bottom: 12px;
        background: rgba(255,255,255,0.06); padding: 12px 20px;
        border-radius: 20px; backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stat-badge { font-size: 16px; font-weight: 700; color: #38bdf8; }
    .btn-action {
        background: linear-gradient(135deg, #38bdf8, #2563eb);
        color: white; border: none; padding: 8px 18px; border-radius: 12px;
        font-weight: 700; cursor: pointer; transition: transform 0.15s, box-shadow 0.15s;
    }
    .btn-action:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(56,189,248,0.4); }
    .grid-container {
        display: grid; grid-template-columns: repeat(8, 1fr); gap: 10px;
        max-width: 680px; width: 100%; padding: 18px;
        background: rgba(255,255,255,0.03); border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08); box-shadow: inset 0 2px 20px rgba(0,0,0,0.5);
    }
    .bubble {
        aspect-ratio: 1; border-radius: 50%;
        background: radial-gradient(circle at 35% 30%, rgba(255,255,255,0.85) 0%, rgba(56,189,248,0.45) 30%, rgba(14,165,233,0.2) 70%, rgba(2,132,199,0.5) 100%);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3), inset 0 -3px 6px rgba(0,0,0,0.25), 0 0 10px rgba(56,189,248,0.3);
        cursor: pointer; position: relative; transition: transform 0.08s ease-out, filter 0.1s;
    }
    .bubble:hover { transform: scale(1.08); filter: brightness(1.2); }
    .bubble.popped {
        background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.05), rgba(15,23,42,0.6));
        box-shadow: inset 0 4px 8px rgba(0,0,0,0.7);
        transform: scale(0.92); cursor: default; filter: brightness(0.6);
    }
    .bubble.popped::after {
        content: ""; position: absolute; top: 50%; left: 50%; width: 14px; height: 14px;
        background: rgba(56,189,248,0.3); border-radius: 50%; transform: translate(-50%, -50%);
    }
    .float-text {
        position: absolute; color: #38bdf8; font-weight: 800; font-size: 18px;
        pointer-events: none; animation: floatFade 0.6s ease-out forwards;
    }
    @keyframes floatFade {
        0% { opacity: 1; transform: translate(-50%, -50%) scale(0.8); }
        50% { transform: translate(-50%, -75%) scale(1.2); }
        100% { opacity: 0; transform: translate(-50%, -100%) scale(1); }
    }
    .stress-bar-bg {
        width: 100%; max-width: 680px; height: 10px; background: rgba(255,255,255,0.1);
        border-radius: 10px; margin-top: 14px; overflow: hidden;
    }
    .stress-bar-fill {
        height: 100%; width: 100%; background: linear-gradient(90deg, #22c55e, #eab308, #ef4444);
        transition: width 0.3s ease;
    }
    .toast-msg {
        position: fixed; bottom: 25px; background: #22c55e; color: white;
        padding: 10px 22px; border-radius: 20px; font-weight: 700; font-size: 14px;
        display: none; animation: popIn 0.3s ease-out;
    }
    @keyframes popIn { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    </style>
    </head>
    <body>
    <div class="header">
        <div class="stat-badge">🫧 Popped: <span id="popCount">0</span></div>
        <div class="stat-badge">🔥 Combo: x<span id="comboCount">1</span></div>
        <button class="btn-action" onclick="resetGrid()">🔄 Fresh Sheet</button>
    </div>
    <div class="grid-container" id="grid"></div>
    <div class="stress-bar-bg"><div class="stress-bar-fill" id="stressFill"></div></div>
    <div style="font-size:13px; color:#94a3b8; margin-top:6px;">Stress Relieved: <span id="stressText">0%</span></div>
    <div class="toast-msg" id="toast">✨ Sheet Cleared! Refreshing endless bubbles...</div>

    <script>
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function playPopSound(freq = 600) {
        try {
            if (!audioCtx) audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            const f = freq + (Math.random() * 200 - 100);
            osc.frequency.setValueAtTime(f, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(f * 0.15, audioCtx.currentTime + 0.08);
            gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.08);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.09);
        } catch(e) {}
    }

    let pops = 0, combo = 1, lastPop = 0;
    const totalBubbles = 48;
    const grid = document.getElementById('grid');
    const popCountEl = document.getElementById('popCount');
    const comboCountEl = document.getElementById('comboCount');
    const stressFillEl = document.getElementById('stressFill');
    const stressTextEl = document.getElementById('stressText');
    const toast = document.getElementById('toast');

    function popBubble(b, e) {
        if (b.classList.contains('popped')) return;
        b.classList.add('popped');
        pops++;
        popCountEl.textContent = pops;

        const now = Date.now();
        if (now - lastPop < 400) {
            combo = Math.min(combo + 1, 20);
        } else {
            combo = 1;
        }
        lastPop = now;
        comboCountEl.textContent = combo;

        playPopSound(500 + combo * 25);

        const rect = b.getBoundingClientRect();
        const float = document.createElement('div');
        float.className = 'float-text';
        float.textContent = combo >= 5 ? `🔥 x${combo}` : '💥 Pop!';
        float.style.left = (rect.left + rect.width / 2) + 'px';
        float.style.top = (rect.top) + 'px';
        document.body.appendChild(float);
        setTimeout(() => float.remove(), 600);

        const poppedCount = document.querySelectorAll('.bubble.popped').length;
        const percent = Math.round((poppedCount / totalBubbles) * 100);
        stressFillEl.style.width = (100 - percent) + '%';
        stressTextEl.textContent = percent + '%';

        if (poppedCount === totalBubbles) {
            toast.style.display = 'block';
            setTimeout(() => {
                toast.style.display = 'none';
                resetGrid();
            }, 1200);
        }
    }

    function resetGrid() {
        grid.innerHTML = '';
        for (let i = 0; i < totalBubbles; i++) {
            const b = document.createElement('div');
            b.className = 'bubble';
            b.addEventListener('mousedown', (e) => popBubble(b, e));
            b.addEventListener('mouseenter', (e) => {
                if (e.buttons === 1) popBubble(b, e);
            });
            grid.appendChild(b);
        }
        stressFillEl.style.width = '100%';
        stressTextEl.textContent = '0%';
    }

    resetGrid();
    </script>
    </body>
    </html>
    """


def get_memory_matrix_game():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 15px; font-family: 'Inter', system-ui, sans-serif;
        background: radial-gradient(circle at 50% 10%, #1e1b4b, #0f172a);
        color: white; display: flex; flex-direction: column; align-items: center;
        min-height: 680px;
    }
    .header {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; max-width: 580px; margin-bottom: 15px;
        background: rgba(255,255,255,0.06); padding: 12px 20px;
        border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);
    }
    .stat { font-weight: 700; color: #a78bfa; font-size: 16px; }
    .grid {
        display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
        width: 100%; max-width: 580px;
    }
    .card { aspect-ratio: 1; perspective: 1000px; cursor: pointer; }
    .card-inner {
        width: 100%; height: 100%; position: relative;
        transform-style: preserve-3d; transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 18px; box-shadow: 0 6px 16px rgba(0,0,0,0.3);
    }
    .card.flipped .card-inner { transform: rotateY(180deg); }
    .card.matched .card-inner { transform: rotateY(180deg) scale(0.95); opacity: 0.85; }
    .card-front, .card-back {
        position: absolute; width: 100%; height: 100%; backface-visibility: hidden;
        border-radius: 18px; display: flex; align-items: center; justify-content: center;
        font-size: 38px; border: 1px solid rgba(255,255,255,0.15);
    }
    .card-front { background: linear-gradient(135deg, #312e81, #1e1b4b); color: #818cf8; font-size: 28px; }
    .card-back { background: linear-gradient(135deg, #4338ca, #6d28d9); transform: rotateY(180deg); }
    .btn-reset {
        background: #6366f1; color: white; border: none; padding: 8px 18px;
        border-radius: 12px; font-weight: 700; cursor: pointer;
    }
    .btn-reset:hover { background: #4f46e5; }
    .win-overlay {
        position: fixed; inset: 0; background: rgba(15,23,42,0.85);
        display: none; flex-direction: column; align-items: center; justify-content: center;
        z-index: 100; backdrop-filter: blur(8px);
    }
    .win-box {
        background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 35px 50px;
        border-radius: 24px; text-align: center; border: 2px solid #a78bfa;
        box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }
    </style>
    </head>
    <body>
    <div class="header">
        <div class="stat">🎯 Moves: <span id="moves">0</span></div>
        <div class="stat">⭐ Pairs: <span id="pairs">0</span>/8</div>
        <button class="btn-reset" onclick="initGame()">🔄 New Game</button>
    </div>
    <div class="grid" id="grid"></div>
    <div class="win-overlay" id="winOverlay">
        <div class="win-box">
            <div style="font-size: 60px;">🏆</div>
            <h2 style="color:white; margin:10px 0;">Brilliant Mind!</h2>
            <p style="color:#c4b5fd;">You cleared all mood pairs in <span id="finalMoves"></span> moves!</p>
            <button class="btn-reset" style="margin-top:15px; font-size:16px;" onclick="initGame()">✨ Play Again</button>
        </div>
    </div>

    <script>
    const emojis = ["💖","😊","🌟","🌸","🧘","🦋","🌈","☕"];
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function playTone(freq, type = 'sine', duration = 0.15) {
        try {
            if (!audioCtx) audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        } catch(e) {}
    }

    let deck = [], flipped = [], matchedCount = 0, moves = 0, lock = false;
    const grid = document.getElementById('grid');
    const movesEl = document.getElementById('moves');
    const pairsEl = document.getElementById('pairs');
    const winOverlay = document.getElementById('winOverlay');

    function initGame() {
        winOverlay.style.display = 'none';
        deck = [...emojis, ...emojis].sort(() => Math.random() - 0.5);
        grid.innerHTML = '';
        flipped = [];
        matchedCount = 0;
        moves = 0;
        lock = false;
        movesEl.textContent = '0';
        pairsEl.textContent = '0';

        deck.forEach((emoji, idx) => {
            const card = document.createElement('div');
            card.className = 'card';
            card.dataset.emoji = emoji;
            card.dataset.index = idx;
            card.innerHTML = `
                <div class="card-inner">
                    <div class="card-front">🧠</div>
                    <div class="card-back">${emoji}</div>
                </div>
            `;
            card.onclick = () => flipCard(card);
            grid.appendChild(card);
        });
    }

    function flipCard(card) {
        if (lock || card.classList.contains('flipped') || card.classList.contains('matched')) return;
        card.classList.add('flipped');
        playTone(440, 'sine', 0.1);
        flipped.push(card);

        if (flipped.length === 2) {
            moves++;
            movesEl.textContent = moves;
            lock = true;
            const [c1, c2] = flipped;
            if (c1.dataset.emoji === c2.dataset.emoji) {
                setTimeout(() => {
                    c1.classList.add('matched');
                    c2.classList.add('matched');
                    playTone(660, 'triangle', 0.25);
                    setTimeout(() => playTone(880, 'triangle', 0.3), 100);
                    matchedCount++;
                    pairsEl.textContent = matchedCount;
                    flipped = [];
                    lock = false;
                    if (matchedCount === 8) {
                        setTimeout(() => {
                            document.getElementById('finalMoves').textContent = moves;
                            winOverlay.style.display = 'flex';
                        }, 500);
                    }
                }, 300);
            } else {
                setTimeout(() => {
                    playTone(220, 'sawtooth', 0.1);
                    c1.classList.remove('flipped');
                    c2.classList.remove('flipped');
                    flipped = [];
                    lock = false;
                }, 800);
            }
        }
    }
    initGame();
    </script>
    </body>
    </html>
    """


def get_cosmic_particles_game():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { margin:0; padding:0; box-sizing:border-box; user-select:none; }
    body { background:#030712; overflow:hidden; font-family:'Inter',sans-serif; color:white; }
    #canvas { width:100vw; height:100vh; display:block; }
    .hud {
        position:absolute; top:20px; left:20px; z-index:10;
        background:rgba(15,23,42,0.7); backdrop-filter:blur(10px);
        padding:12px 20px; border-radius:18px; border:1px solid rgba(255,255,255,0.1);
    }
    .hud h3 { margin:0 0 4px; font-size:16px; color:#38bdf8; }
    .hud p { margin:0; font-size:13px; color:#94a3b8; }
    .modes { position:absolute; top:20px; right:20px; z-index:10; display:flex; gap:8px; }
    .mode-btn {
        background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15);
        color:white; padding:8px 14px; border-radius:12px; cursor:pointer; font-weight:600;
        backdrop-filter:blur(8px); transition:0.2s;
    }
    .mode-btn.active, .mode-btn:hover { background:#38bdf8; color:#0f172a; border-color:#38bdf8; }
    </style>
    </head>
    <body>
    <div class="hud">
        <h3>🌌 Cosmic Zen Particles</h3>
        <p>Move mouse / touch to guide galaxy vortex. Click to burst energy.</p>
    </div>
    <div class="modes">
        <button class="mode-btn active" onclick="setPalette('neon')">✨ Neon</button>
        <button class="mode-btn" onclick="setPalette('aurora')">🌿 Aurora</button>
        <button class="mode-btn" onclick="setPalette('sunset')">🌅 Sunset</button>
    </div>
    <canvas id="canvas"></canvas>

    <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    let w = canvas.width = window.innerWidth;
    let h = canvas.height = window.innerHeight;

    window.onresize = () => {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    };

    const palettes = {
        neon: ['#38bdf8', '#818cf8', '#c084fc', '#f472b6', '#34d399'],
        aurora: ['#34d399', '#2dd4bf', '#38bdf8', '#a7f3d0', '#6ee7b7'],
        sunset: ['#fb7185', '#f43f5e', '#fb923c', '#facc15', '#ec4899']
    };
    let currentPalette = palettes.neon;

    function setPalette(name) {
        currentPalette = palettes[name];
        document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
        event.target.classList.add('active');
        particles.forEach(p => p.color = currentPalette[Math.floor(Math.random() * currentPalette.length)]);
    }

    class Particle {
        constructor() { this.reset(); }
        reset() {
            this.x = Math.random() * w;
            this.y = Math.random() * h;
            this.vx = (Math.random() - 0.5) * 1.5;
            this.vy = (Math.random() - 0.5) * 1.5;
            this.radius = Math.random() * 2.5 + 1;
            this.color = currentPalette[Math.floor(Math.random() * currentPalette.length)];
        }
        update(mouse) {
            if (mouse.x !== null) {
                const dx = mouse.x - this.x;
                const dy = mouse.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 220) {
                    const force = (220 - dist) / 220;
                    this.vx += (dx / dist) * force * 0.6;
                    this.vy += (dy / dist) * force * 0.6;
                }
            }
            this.x += this.vx;
            this.y += this.vy;
            this.vx *= 0.96;
            this.vy *= 0.96;
            if (this.x < 0) this.x = w;
            if (this.x > w) this.x = 0;
            if (this.y < 0) this.y = h;
            if (this.y > h) this.y = 0;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.shadowBlur = 12;
            ctx.shadowColor = this.color;
            ctx.fill();
            ctx.shadowBlur = 0;
        }
    }

    const particles = Array.from({ length: 220 }, () => new Particle());
    const mouse = { x: null, y: null };

    window.addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
    window.addEventListener('mouseleave', () => { mouse.x = null; mouse.y = null; });
    window.addEventListener('click', e => {
        for (let i = 0; i < 40; i++) {
            const p = new Particle();
            p.x = e.clientX;
            p.y = e.clientY;
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 8 + 2;
            p.vx = Math.cos(angle) * speed;
            p.vy = Math.sin(angle) * speed;
            particles.push(p);
        }
        if (particles.length > 320) particles.splice(0, 40);
    });

    function loop() {
        ctx.fillStyle = 'rgba(3, 7, 18, 0.22)';
        ctx.fillRect(0, 0, w, h);
        particles.forEach(p => { p.update(mouse); p.draw(); });
        for (let i = 0; i < particles.length; i += 2) {
            for (let j = i + 1; j < particles.length; j += 4) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 75) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(56, 189, 248, ${0.18 * (1 - dist / 75)})`;
                    ctx.lineWidth = 0.7;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(loop);
    }
    loop();
    </script>
    </body>
    </html>
    """


def get_brick_breaker_game():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 15px; font-family: 'Inter', system-ui, sans-serif;
        background: radial-gradient(circle at 50% 20%, #1e1b4b, #090d16);
        color: white; display: flex; flex-direction: column; align-items: center;
        min-height: 680px; overflow: hidden;
    }
    .header {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; max-width: 640px; margin-bottom: 10px;
        background: rgba(255,255,255,0.06); padding: 10px 18px;
        border-radius: 18px; border: 1px solid rgba(255,255,255,0.1);
    }
    .stat { font-weight: 700; color: #38bdf8; font-size: 15px; }
    canvas {
        background: rgba(15,23,42,0.8); border: 2px solid rgba(255,255,255,0.12);
        border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        cursor: none; display: block;
    }
    .toast {
        position: fixed; bottom: 20px; background: rgba(56,189,248,0.9);
        color: #0f172a; padding: 10px 24px; border-radius: 20px;
        font-weight: 800; font-size: 15px; display: none; animation: pop 0.3s ease;
    }
    @keyframes pop { from { transform: translateY(20px); opacity:0; } to { transform: translateY(0); opacity:1; } }
    </style>
    </head>
    <body>
    <div class="header">
        <div class="stat">✨ Score: <span id="score">0</span></div>
        <div class="stat">🔥 Zen Streak: <span id="streak">0</span></div>
        <div class="stat">🧱 Mode: <span style="color:#22c55e;">Endless Relaxing</span></div>
    </div>
    <canvas id="gameCanvas" width="620" height="520"></canvas>
    <div class="toast" id="zenToast">✨ Pure Joy! Cascade Unleashed!</div>

    <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const scoreEl = document.getElementById('score');
    const streakEl = document.getElementById('streak');
    const zenToast = document.getElementById('zenToast');

    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function playNote(freq) {
        try {
            if (!audioCtx) audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.15);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.16);
        } catch(e) {}
    }

    let paddleWidth = 120, paddleHeight = 14, paddleX = (canvas.width - paddleWidth) / 2;
    let ballX = canvas.width / 2, ballY = canvas.height - 40;
    let ballDx = 3.5, ballDy = -3.5, ballRadius = 8;
    let score = 0, streak = 0;

    const rowCount = 4, colCount = 6, brickWidth = 85, brickHeight = 22, brickPadding = 12, offsetTop = 45, offsetLeft = 24;
    const colors = ["#f43f5e", "#fb923c", "#facc15", "#38bdf8"];
    let bricks = [];

    function initBricks() {
        bricks = [];
        for (let c = 0; c < colCount; c++) {
            bricks[c] = [];
            for (let r = 0; r < rowCount; r++) {
                bricks[c][r] = { x: 0, y: 0, status: 1, color: colors[r] };
            }
        }
    }

    canvas.addEventListener('mousemove', e => {
        const rect = canvas.getBoundingClientRect();
        paddleX = e.clientX - rect.left - paddleWidth / 2;
        if (paddleX < 0) paddleX = 0;
        if (paddleX + paddleWidth > canvas.width) paddleX = canvas.width - paddleWidth;
    });

    function collisionDetection() {
        let remaining = 0;
        for (let c = 0; c < colCount; c++) {
            for (let r = 0; r < rowCount; r++) {
                const b = bricks[c][r];
                if (b.status === 1) {
                    remaining++;
                    if (ballX > b.x && ballX < b.x + brickWidth && ballY > b.y && ballY < b.y + brickHeight) {
                        ballDy = -ballDy;
                        b.status = 0;
                        score += 10;
                        streak++;
                        scoreEl.textContent = score;
                        streakEl.textContent = streak;
                        playNote(400 + (r * 100) + (streak % 5) * 20);
                    }
                }
            }
        }
        if (remaining === 0) {
            zenToast.textContent = "🌟 Infinite Cascade Refresh! Keep Going!";
            zenToast.style.display = "block";
            setTimeout(() => { zenToast.style.display = "none"; }, 1500);
            initBricks();
        }
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let c = 0; c < colCount; c++) {
            for (let r = 0; r < rowCount; r++) {
                if (bricks[c][r].status === 1) {
                    const bx = c * (brickWidth + brickPadding) + offsetLeft;
                    const by = r * (brickHeight + brickPadding) + offsetTop;
                    bricks[c][r].x = bx;
                    bricks[c][r].y = by;
                    ctx.beginPath();
                    ctx.roundRect(bx, by, brickWidth, brickHeight, 6);
                    ctx.fillStyle = bricks[c][r].color;
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = bricks[c][r].color;
                    ctx.fill();
                    ctx.shadowBlur = 0;
                }
            }
        }

        ctx.beginPath();
        ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
        ctx.fillStyle = "#ffffff";
        ctx.shadowBlur = 12;
        ctx.shadowColor = "#38bdf8";
        ctx.fill();
        ctx.shadowBlur = 0;

        ctx.beginPath();
        ctx.roundRect(paddleX, canvas.height - paddleHeight - 12, paddleWidth, paddleHeight, 8);
        ctx.fillStyle = "#38bdf8";
        ctx.shadowBlur = 14;
        ctx.shadowColor = "#38bdf8";
        ctx.fill();
        ctx.shadowBlur = 0;

        collisionDetection();

        if (ballX + ballDx > canvas.width - ballRadius || ballX + ballDx < ballRadius) {
            ballDx = -ballDx;
            playNote(300);
        }
        if (ballY + ballDy < ballRadius) {
            ballDy = -ballDy;
            playNote(300);
        } else if (ballY + ballDy > canvas.height - paddleHeight - 18) {
            if (ballX > paddleX && ballX < paddleX + paddleWidth) {
                ballDy = -Math.abs(ballDy);
                const hitPos = (ballX - (paddleX + paddleWidth / 2)) / (paddleWidth / 2);
                ballDx = hitPos * 4.5;
                playNote(520);
            } else if (ballY + ballDy > canvas.height - ballRadius) {
                ballX = paddleX + paddleWidth / 2;
                ballY = canvas.height - paddleHeight - 30;
                ballDx = (Math.random() - 0.5) * 6;
                ballDy = -3.5;
                streak = 0;
                streakEl.textContent = "0";
            }
        }

        ballX += ballDx;
        ballY += ballDy;
        requestAnimationFrame(draw);
    }

    initBricks();
    draw();
    </script>
    </body>
    </html>
    """


def get_glow_snake_game():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 15px; font-family: 'Inter', system-ui, sans-serif;
        background: radial-gradient(circle at 50% 10%, #064e3b, #022c22);
        color: white; display: flex; flex-direction: column; align-items: center;
        min-height: 680px; overflow: hidden;
    }
    .header {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; max-width: 580px; margin-bottom: 12px;
        background: rgba(255,255,255,0.06); padding: 10px 18px;
        border-radius: 18px; border: 1px solid rgba(45,212,191,0.2);
    }
    .stat { font-weight: 700; color: #34d399; font-size: 15px; }
    canvas {
        background: rgba(4,47,46,0.85); border: 2px solid rgba(45,212,191,0.3);
        border-radius: 20px; box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        display: block;
    }
    .controls-hint {
        margin-top: 10px; font-size: 13px; color: #a7f3d0;
    }
    </style>
    </head>
    <body>
    <div class="header">
        <div class="stat">🐍 Score: <span id="snakeScore">0</span></div>
        <div class="stat">✨ Joy Orbs: <span id="snakeOrbs">0</span></div>
        <div class="stat">🌿 Chill Wrap Mode</div>
    </div>
    <canvas id="snakeCanvas" width="560" height="460"></canvas>
    <div class="controls-hint">Use Arrow Keys or WASD to guide the Zen Glow Snake. Screen wraps seamlessly!</div>

    <script>
    const canvas = document.getElementById('snakeCanvas');
    const ctx = canvas.getContext('2d');
    const scoreEl = document.getElementById('snakeScore');
    const orbsEl = document.getElementById('snakeOrbs');

    const gridSize = 20;
    const cols = canvas.width / gridSize;
    const rows = canvas.height / gridSize;

    let snake = [{x: 10, y: 10}, {x: 9, y: 10}, {x: 8, y: 10}];
    let dir = {x: 1, y: 0}, nextDir = {x: 1, y: 0};
    let food = {x: 18, y: 12, emoji: "🌸"};
    let score = 0, orbs = 0;
    const foods = ["🌸", "💎", "⭐", "💖", "🍓", "🍀"];

    function spawnFood() {
        food = {
            x: Math.floor(Math.random() * cols),
            y: Math.floor(Math.random() * rows),
            emoji: foods[Math.floor(Math.random() * foods.length)]
        };
    }

    window.addEventListener('keydown', e => {
        if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') {
            if (dir.y === 0) nextDir = {x: 0, y: -1};
        } else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') {
            if (dir.y === 0) nextDir = {x: 0, y: 1};
        } else if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
            if (dir.x === 0) nextDir = {x: -1, y: 0};
        } else if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
            if (dir.x === 0) nextDir = {x: 1, y: 0};
        }
    });

    function update() {
        dir = nextDir;
        let head = {x: snake[0].x + dir.x, y: snake[0].y + dir.y};

        // Endless screen wrap (Relaxing - No wall deaths!)
        if (head.x < 0) head.x = cols - 1;
        if (head.x >= cols) head.x = 0;
        if (head.y < 0) head.y = rows - 1;
        if (head.y >= rows) head.y = 0;

        snake.unshift(head);

        if (head.x === food.x && head.y === food.y) {
            score += 15;
            orbs++;
            scoreEl.textContent = score;
            orbsEl.textContent = orbs;
            spawnFood();
        } else {
            snake.pop();
        }
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw Food
        ctx.font = "16px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(food.emoji, food.x * gridSize + gridSize/2, food.y * gridSize + gridSize/2);

        // Draw Snake
        snake.forEach((seg, i) => {
            ctx.beginPath();
            ctx.roundRect(seg.x * gridSize + 2, seg.y * gridSize + 2, gridSize - 4, gridSize - 4, 6);
            ctx.fillStyle = i === 0 ? "#34d399" : "#10b981";
            ctx.shadowBlur = i === 0 ? 15 : 6;
            ctx.shadowColor = "#34d399";
            ctx.fill();
            ctx.shadowBlur = 0;
        });
    }

    setInterval(() => {
        update();
        draw();
    }, 120);
    </script>
    </body>
    </html>
    """


def get_rhythm_harmony_game():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 15px; font-family: 'Inter', system-ui, sans-serif;
        background: radial-gradient(circle at 50% 10%, #311042, #0b0214);
        color: white; display: flex; flex-direction: column; align-items: center;
        min-height: 680px; overflow: hidden;
    }
    .header {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; max-width: 480px; margin-bottom: 10px;
        background: rgba(255,255,255,0.08); padding: 10px 20px;
        border-radius: 20px; border: 1px solid rgba(244,114,182,0.3);
    }
    .stat { font-weight: 700; color: #f472b6; font-size: 16px; }
    canvas {
        background: rgba(15,23,42,0.85); border: 2px solid rgba(244,114,182,0.3);
        border-radius: 22px; box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        display: block; cursor: pointer;
    }
    .keys-bar {
        display: flex; width: 440px; justify-content: space-around; margin-top: 10px;
    }
    .key-hint {
        background: rgba(244,114,182,0.2); border: 1px solid rgba(244,114,182,0.4);
        padding: 6px 18px; border-radius: 12px; font-weight: 800; font-size: 14px; color: #fbcfe8;
    }
    </style>
    </head>
    <body>
    <div class="header">
        <div class="stat">🎵 Score: <span id="rhythmScore">0</span></div>
        <div class="stat">🔥 Combo: x<span id="rhythmCombo">1</span></div>
    </div>
    <canvas id="rhythmCanvas" width="440" height="520"></canvas>
    <div class="keys-bar">
        <div class="key-hint">D</div>
        <div class="key-hint">F</div>
        <div class="key-hint">J</div>
        <div class="key-hint">K</div>
    </div>

    <script>
    const canvas = document.getElementById('rhythmCanvas');
    const ctx = canvas.getContext('2d');
    const scoreEl = document.getElementById('rhythmScore');
    const comboEl = document.getElementById('rhythmCombo');

    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    const notesFreq = [329.63, 392.00, 440.00, 523.25]; // E4, G4, A4, C5
    const laneColors = ["#f472b6", "#c084fc", "#38bdf8", "#34d399"];

    function playRhythmTone(lane) {
        try {
            if (!audioCtx) audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(notesFreq[lane], audioCtx.currentTime);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.42);
        } catch(e) {}
    }

    let notes = [];
    let score = 0, combo = 1;
    const laneWidth = canvas.width / 4;
    const hitLineY = canvas.height - 70;

    function spawnNote() {
        const lane = Math.floor(Math.random() * 4);
        notes.push({ lane, y: -30, hit: false });
    }

    setInterval(spawnNote, 700);

    function hitLane(lane) {
        playRhythmTone(lane);
        let found = false;
        for (let n of notes) {
            if (n.lane === lane && Math.abs(n.y - hitLineY) < 55 && !n.hit) {
                n.hit = true;
                found = true;
                score += 10 * combo;
                combo = Math.min(combo + 1, 10);
                scoreEl.textContent = score;
                comboEl.textContent = combo;
                break;
            }
        }
        if (!found) {
            combo = 1;
            comboEl.textContent = combo;
        }
    }

    window.addEventListener('keydown', e => {
        if (e.key === 'd' || e.key === 'D') hitLane(0);
        if (e.key === 'f' || e.key === 'F') hitLane(1);
        if (e.key === 'j' || e.key === 'J') hitLane(2);
        if (e.key === 'k' || e.key === 'K') hitLane(3);
    });

    canvas.addEventListener('mousedown', e => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const lane = Math.floor(x / laneWidth);
        hitLane(lane);
    });

    function loop() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw Lanes
        for (let i = 0; i < 4; i++) {
            ctx.strokeStyle = "rgba(255,255,255,0.06)";
            ctx.beginPath();
            ctx.moveTo(i * laneWidth, 0);
            ctx.lineTo(i * laneWidth, canvas.height);
            ctx.stroke();
        }

        // Draw Hit Line
        ctx.beginPath();
        ctx.moveTo(0, hitLineY);
        ctx.lineTo(canvas.width, hitLineY);
        ctx.strokeStyle = "rgba(244,114,182,0.8)";
        ctx.lineWidth = 3;
        ctx.shadowBlur = 10;
        ctx.shadowColor = "#f472b6";
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Draw & Update Notes
        for (let i = notes.length - 1; i >= 0; i--) {
            let n = notes[i];
            n.y += 3.8;

            if (!n.hit) {
                ctx.beginPath();
                ctx.roundRect(n.lane * laneWidth + 10, n.y, laneWidth - 20, 24, 10);
                ctx.fillStyle = laneColors[n.lane];
                ctx.shadowBlur = 12;
                ctx.shadowColor = laneColors[n.lane];
                ctx.fill();
                ctx.shadowBlur = 0;
            }

            if (n.y > canvas.height + 30) {
                notes.splice(i, 1);
            }
        }
        requestAnimationFrame(loop);
    }
    loop();
    </script>
    </body>
    </html>
    """


def get_crystal_ball_oracle():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 25px; font-family: 'Inter', system-ui, sans-serif;
        background: radial-gradient(circle at 50% 20%, #2e1065, #090214);
        color: white; display: flex; flex-direction: column; align-items: center; justify-content: center;
        min-height: 520px; overflow: hidden;
    }
    .orb-container {
        width: 220px; height: 220px; border-radius: 50%;
        background: radial-gradient(circle at 35% 30%, #e0e7ff 0%, #818cf8 35%, #4f46e5 70%, #1e1b4b 100%);
        box-shadow: 0 0 60px rgba(129,140,248,0.6), inset 0 0 30px rgba(255,255,255,0.8);
        display: flex; align-items: center; justify-content: center;
        font-size: 60px; cursor: pointer; transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
    }
    .orb-container:hover { transform: scale(1.1) rotate(5deg); box-shadow: 0 0 80px rgba(168,85,247,0.8); }
    .oracle-box {
        margin-top: 25px; background: rgba(255,255,255,0.08); padding: 18px 30px;
        border-radius: 20px; border: 1px solid rgba(168,85,247,0.4); max-width: 520px;
        text-align: center; backdrop-filter: blur(10px);
    }
    .oracle-text { font-size: 17px; font-weight: 700; color: #e9d5ff; line-height: 1.5; }
    </style>
    </head>
    <body>
    <div style="font-size: 22px; font-weight: 800; color: #c084fc; margin-bottom: 6px;">🔮 Mystic Cosmic Oracle</div>
    <div style="font-size: 13px; color: #cbd5e1; margin-bottom: 20px;">Gaze into the crystal ball and tap to receive today's cosmic guidance</div>
    <div class="orb-container" onclick="askOracle()">
        <span>✨</span>
    </div>
    <div class="oracle-box">
        <div class="oracle-text" id="oracleMsg">“Tap the glowing crystal sphere to unlock your cosmic answer.”</div>
    </div>

    <script>
    const predictions = [
        "🌌 The universe is aligning peace into your thoughts today. Trust your path.",
        "✨ A pleasant surprise will arrive from an unexpected friend or moment.",
        "🌸 Let go of the need to control everything. Peace flows when you surrender tension.",
        "🌿 You already have the strength required to overcome whatever challenges you face.",
        "💖 Treat yourself with extreme gentleness today. You deserve complete rest and kindness.",
        "🌟 A brilliant creative spark will ignite in your mind very soon!"
    ];

    function askOracle() {
        const msg = document.getElementById('oracleMsg');
        msg.textContent = "🔮 Consulting the cosmic stars...";
        setTimeout(() => {
            msg.textContent = predictions[Math.floor(Math.random() * predictions.length)];
        }, 600);
    }
    </script>
    </body>
    </html>
    """


def get_mandala_painter():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; margin: 0; padding: 0; }
    body { background: #030712; color: white; font-family: 'Inter', sans-serif; overflow: hidden; display: flex; flex-direction: column; align-items: center; }
    .toolbar {
        position: absolute; top: 15px; z-index: 10; display: flex; gap: 10px;
        background: rgba(15,23,42,0.8); backdrop-filter: blur(10px); padding: 10px 18px;
        border-radius: 20px; border: 1px solid rgba(255,255,255,0.15); align-items: center;
    }
    .color-btn { width: 26px; height: 26px; border-radius: 50%; border: 2px solid white; cursor: pointer; }
    .btn-tool {
        background: rgba(255,255,255,0.12); color: white; border: none; padding: 6px 14px;
        border-radius: 12px; font-weight: 700; cursor: pointer; font-size: 13px;
    }
    .btn-tool:hover { background: #38bdf8; color: #0f172a; }
    canvas { display: block; width: 100vw; height: 100vh; cursor: crosshair; }
    </style>
    </head>
    <body>
    <div class="toolbar">
        <span style="font-size:13px; font-weight:700; color:#38bdf8;">🎨 Zen Mandala Painter</span>
        <div class="color-btn" style="background:#38bdf8;" onclick="setColor('#38bdf8')"></div>
        <div class="color-btn" style="background:#f43f5e;" onclick="setColor('#f43f5e')"></div>
        <div class="color-btn" style="background:#a855f7;" onclick="setColor('#a855f7')"></div>
        <div class="color-btn" style="background:#22c55e;" onclick="setColor('#22c55e')"></div>
        <div class="color-btn" style="background:#facc15;" onclick="setColor('#facc15')"></div>
        <button class="btn-tool" onclick="clearCanvas()">🧹 Clear</button>
    </div>
    <canvas id="paintCanvas"></canvas>

    <script>
    const canvas = document.getElementById('paintCanvas');
    const ctx = canvas.getContext('2d');
    let w = canvas.width = window.innerWidth;
    let h = canvas.height = window.innerHeight;

    window.onresize = () => {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    };

    let drawing = false, lastX = 0, lastY = 0, color = '#38bdf8', symmetry = 8;

    function setColor(c) { color = c; }
    function clearCanvas() { ctx.fillStyle = '#030712'; ctx.fillRect(0, 0, w, h); }

    clearCanvas();

    function drawSegment(x1, y1, x2, y2) {
        const cx = w / 2, cy = h / 2;
        const angle = (Math.PI * 2) / symmetry;

        for (let i = 0; i < symmetry; i++) {
            ctx.save();
            ctx.translate(cx, cy);
            ctx.rotate(i * angle);

            ctx.beginPath();
            ctx.moveTo(x1 - cx, y1 - cy);
            ctx.lineTo(x2 - cx, y2 - cy);
            ctx.strokeStyle = color;
            ctx.lineWidth = 2.5;
            ctx.lineCap = 'round';
            ctx.shadowBlur = 10;
            ctx.shadowColor = color;
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(-(x1 - cx), y1 - cy);
            ctx.lineTo(-(x2 - cx), y2 - cy);
            ctx.stroke();

            ctx.restore();
        }
    }

    canvas.addEventListener('mousedown', e => {
        drawing = true;
        lastX = e.clientX;
        lastY = e.clientY;
    });

    canvas.addEventListener('mousemove', e => {
        if (!drawing) return;
        drawSegment(lastX, lastY, e.clientX, e.clientY);
        lastX = e.clientX;
        lastY = e.clientY;
    });

    window.addEventListener('mouseup', () => drawing = false);
    </script>
    </body>
    </html>
    """


def get_zen_piano():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 20px; font-family: 'Inter', system-ui, sans-serif;
        background: radial-gradient(circle at 50% 10%, #1e1b4b, #0f172a);
        color: white; display: flex; flex-direction: column; align-items: center; justify-content: center;
        min-height: 520px; overflow: hidden;
    }
    .piano-board {
        display: flex; gap: 10px; max-width: 650px; width: 100%;
        background: rgba(255,255,255,0.06); padding: 25px; border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .key {
        flex: 1; height: 260px; border-radius: 18px;
        background: linear-gradient(180deg, #312e81, #1e1b4b);
        border: 2px solid rgba(255,255,255,0.15); cursor: pointer;
        display: flex; flex-direction: column; justify-content: flex-end; align-items: center;
        padding-bottom: 20px; font-weight: 800; font-size: 16px; color: #cbd5e1;
        transition: transform 0.1s, background 0.1s, box-shadow 0.1s;
    }
    .key:hover { transform: translateY(-4px); border-color: #38bdf8; box-shadow: 0 10px 25px rgba(56,189,248,0.4); }
    .key:active, .key.active { transform: translateY(4px); background: #38bdf8; color: #0f172a; box-shadow: 0 0 30px #38bdf8; }
    </style>
    </head>
    <body>
    <div style="font-size:20px; font-weight:800; color:#38bdf8; margin-bottom:6px;">🎹 Zen Mood Chime Piano</div>
    <div style="font-size:13px; color:#94a3b8; margin-bottom:20px;">Tap keys or press 1-8 on your keyboard for harmonic bells</div>
    <div class="piano-board">
        <div class="key" onclick="playChime(261.63, this)"><span>C4</span></div>
        <div class="key" onclick="playChime(293.66, this)"><span>D4</span></div>
        <div class="key" onclick="playChime(329.63, this)"><span>E4</span></div>
        <div class="key" onclick="playChime(392.00, this)"><span>G4</span></div>
        <div class="key" onclick="playChime(440.00, this)"><span>A4</span></div>
        <div class="key" onclick="playChime(523.25, this)"><span>C5</span></div>
        <div class="key" onclick="playChime(587.33, this)"><span>D5</span></div>
        <div class="key" onclick="playChime(659.25, this)"><span>E5</span></div>
    </div>

    <script>
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function playChime(freq, el) {
        if (el) {
            el.classList.add('active');
            setTimeout(() => el.classList.remove('active'), 200);
        }
        try {
            if (!audioCtx) audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.8);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 1.9);
        } catch(e) {}
    }
    </script>
    </body>
    </html>
    """


def get_koi_pond_game():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { margin:0; padding:0; box-sizing:border-box; user-select:none; }
    body { background:#042f2e; overflow:hidden; font-family:'Inter',sans-serif; }
    #canvas { width:100vw; height:100vh; display:block; cursor:crosshair; }
    .hud {
        position:absolute; top:20px; left:20px; z-index:10;
        background:rgba(4,47,46,0.75); backdrop-filter:blur(10px);
        padding:12px 20px; border-radius:18px; border:1px solid rgba(45,212,191,0.25);
        color:white;
    }
    .hud h3 { margin:0 0 4px; font-size:16px; color:#2dd4bf; }
    .hud p { margin:0; font-size:13px; color:#ccfbf1; }
    </style>
    </head>
    <body>
    <div class="hud">
        <h3>🌸 Zen Koi Pond</h3>
        <p>Touch or click anywhere to ripple water and feed the Koi fish.</p>
    </div>
    <canvas id="canvas"></canvas>

    <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    let w = canvas.width = window.innerWidth;
    let h = canvas.height = window.innerHeight;

    window.onresize = () => {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    };

    class Koi {
        constructor() {
            this.x = Math.random() * w;
            this.y = Math.random() * h;
            this.vx = (Math.random() - 0.5) * 2;
            this.vy = (Math.random() - 0.5) * 2;
            this.size = Math.random() * 15 + 25;
            this.colors = Math.random() > 0.5 ? ['#f97316', '#ffffff'] : ['#ef4444', '#facc15'];
            this.angle = 0;
            this.wiggle = 0;
        }
        update(target) {
            this.wiggle += 0.15;
            if (target) {
                const dx = target.x - this.x;
                const dy = target.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist > 15) {
                    this.vx += (dx / dist) * 0.12;
                    this.vy += (dy / dist) * 0.12;
                }
            } else {
                this.vx += (Math.random() - 0.5) * 0.1;
                this.vy += (Math.random() - 0.5) * 0.1;
            }
            const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
            const maxSpeed = 2.4;
            if (speed > maxSpeed) {
                this.vx = (this.vx / speed) * maxSpeed;
                this.vy = (this.vy / speed) * maxSpeed;
            }
            this.x += this.vx;
            this.y += this.vy;
            this.angle = Math.atan2(this.vy, this.vx);

            if (this.x < -50) this.x = w + 50;
            if (this.x > w + 50) this.x = -50;
            if (this.y < -50) this.y = h + 50;
            if (this.y > h + 50) this.y = -50;
        }
        draw() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.angle);

            ctx.beginPath();
            ctx.fillStyle = this.colors[0];
            const tailWiggle = Math.sin(this.wiggle) * 8;
            ctx.moveTo(-this.size, tailWiggle);
            ctx.lineTo(-this.size * 1.5, tailWiggle * 1.4 + 10);
            ctx.lineTo(-this.size * 1.5, tailWiggle * 1.4 - 10);
            ctx.closePath();
            ctx.fill();

            ctx.beginPath();
            ctx.ellipse(0, 0, this.size, this.size * 0.45, 0, 0, Math.PI * 2);
            ctx.fillStyle = this.colors[0];
            ctx.fill();

            ctx.beginPath();
            ctx.ellipse(this.size * 0.2, 0, this.size * 0.5, this.size * 0.3, 0, 0, Math.PI * 2);
            ctx.fillStyle = this.colors[1];
            ctx.fill();

            ctx.restore();
        }
    }

    const fishList = Array.from({ length: 7 }, () => new Koi());
    let ripples = [];
    let foods = [];

    window.addEventListener('click', e => {
        ripples.push({ x: e.clientX, y: e.clientY, radius: 5, alpha: 1 });
        foods.push({ x: e.clientX, y: e.clientY, life: 120 });
    });

    function loop() {
        ctx.fillStyle = 'rgba(4, 47, 46, 0.35)';
        ctx.fillRect(0, 0, w, h);

        ripples.forEach((r, idx) => {
            r.radius += 1.8;
            r.alpha -= 0.015;
            ctx.beginPath();
            ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(45, 212, 191, ${r.alpha})`;
            ctx.lineWidth = 2.5;
            ctx.stroke();
            if (r.alpha <= 0) ripples.splice(idx, 1);
        });

        foods.forEach((f, idx) => {
            ctx.beginPath();
            ctx.arc(f.x, f.y, 4, 0, Math.PI * 2);
            ctx.fillStyle = '#fef08a';
            ctx.fill();
            f.life--;
            if (f.life <= 0) foods.splice(idx, 1);
        });

        const target = foods.length > 0 ? foods[0] : null;
        fishList.forEach(fish => { fish.update(target); fish.draw(); });
        requestAnimationFrame(loop);
    }
    loop();
    </script>
    </body>
    </html>
    """


def get_ambient_sound_mixer():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; }
    body {
        margin: 0; padding: 25px; font-family: 'Inter', system-ui, sans-serif;
        background: linear-gradient(135deg, #0f172a, #1e1b4b); color: white;
    }
    .grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;
        max-width: 800px; margin: 0 auto;
    }
    .sound-card {
        background: rgba(255,255,255,0.05); padding: 20px; border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1); text-align: center;
        transition: transform 0.2s, background 0.2s;
    }
    .sound-card:hover { background: rgba(255,255,255,0.08); transform: translateY(-3px); }
    .sound-icon { font-size: 38px; margin-bottom: 8px; }
    .sound-name { font-weight: 700; margin-bottom: 12px; font-size: 15px; }
    input[type=range] { width: 100%; accent-color: #38bdf8; cursor: pointer; }
    .master-bar {
        max-width: 800px; margin: 0 auto 20px; display: flex; justify-content: space-between;
        align-items: center; background: rgba(56,189,248,0.1); padding: 14px 24px;
        border-radius: 18px; border: 1px solid rgba(56,189,248,0.3);
    }
    .btn-toggle {
        background: #38bdf8; color: #0f172a; border: none; padding: 10px 22px;
        border-radius: 12px; font-weight: 800; cursor: pointer;
    }
    </style>
    </head>
    <body>
    <div class="master-bar">
        <div style="font-weight:700; font-size:16px;">🎧 Ambient Soundscape & Lo-Fi Lounge</div>
        <button class="btn-toggle" id="masterBtn" onclick="toggleAudio()">▶️ Start Audio</button>
    </div>
    <div class="grid">
        <div class="sound-card">
            <div class="sound-icon">🌧️</div>
            <div class="sound-name">Gentle Rain</div>
            <input type="range" min="0" max="1" step="0.05" value="0.4" oninput="setGain('rain', this.value)">
        </div>
        <div class="sound-card">
            <div class="sound-icon">🔥</div>
            <div class="sound-name">Campfire Crackle</div>
            <input type="range" min="0" max="1" step="0.05" value="0.2" oninput="setGain('fire', this.value)">
        </div>
        <div class="sound-card">
            <div class="sound-icon">🌊</div>
            <div class="sound-name">Ocean Waves</div>
            <input type="range" min="0" max="1" step="0.05" value="0.3" oninput="setGain('waves', this.value)">
        </div>
        <div class="sound-card">
            <div class="sound-icon">🌲</div>
            <div class="sound-name">Forest Birds</div>
            <input type="range" min="0" max="1" step="0.05" value="0.15" oninput="setGain('birds', this.value)">
        </div>
        <div class="sound-card">
            <div class="sound-icon">🎐</div>
            <div class="sound-name">Zen Chimes</div>
            <input type="range" min="0" max="1" step="0.05" value="0.25" oninput="setGain('chimes', this.value)">
        </div>
        <div class="sound-card">
            <div class="sound-icon">☕</div>
            <div class="sound-name">Lo-Fi Warmth</div>
            <input type="range" min="0" max="1" step="0.05" value="0.3" oninput="setGain('lofi', this.value)">
        </div>
    </div>

    <script>
    let isPlaying = false;
    let audioCtx = null;
    let nodes = {};

    function initSynthesizers() {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        const bufferSize = audioCtx.sampleRate * 2;
        const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        let b0=0, b1=0, b2=0;
        for (let i = 0; i < bufferSize; i++) {
            const white = Math.random() * 2 - 1;
            b0 = 0.99886 * b0 + white * 0.0555179;
            b1 = 0.99332 * b1 + white * 0.0750759;
            b2 = 0.96900 * b2 + white * 0.1538520;
            output[i] = (b0 + b1 + b2) * 0.11;
        }
        const rainSource = audioCtx.createBufferSource();
        rainSource.buffer = noiseBuffer;
        rainSource.loop = true;
        
        const rainFilter = audioCtx.createBiquadFilter();
        rainFilter.type = 'lowpass';
        rainFilter.frequency.value = 1000;
        
        const rainGain = audioCtx.createGain();
        rainGain.gain.value = 0.4;
        rainSource.connect(rainFilter).connect(rainGain).connect(audioCtx.destination);
        rainSource.start();
        nodes['rain'] = rainGain;

        const fireGain = audioCtx.createGain();
        fireGain.gain.value = 0.2;
        const fireFilter = audioCtx.createBiquadFilter();
        fireFilter.type = 'bandpass';
        fireFilter.frequency.value = 400;
        rainSource.connect(fireFilter).connect(fireGain).connect(audioCtx.destination);
        nodes['fire'] = fireGain;

        const waveGain = audioCtx.createGain();
        waveGain.gain.value = 0.3;
        const waveFilter = audioCtx.createBiquadFilter();
        waveFilter.type = 'lowpass';
        
        const lfo = audioCtx.createOscillator();
        lfo.frequency.value = 0.12;
        const lfoGain = audioCtx.createGain();
        lfoGain.gain.value = 350;
        lfo.connect(lfoGain);
        lfoGain.connect(waveFilter.frequency);
        waveFilter.frequency.value = 450;
        lfo.start();
        rainSource.connect(waveFilter).connect(waveGain).connect(audioCtx.destination);
        nodes['waves'] = waveGain;

        const lofiGain = audioCtx.createGain();
        lofiGain.gain.value = 0.3;
        [130.81, 196.00, 246.94].forEach(f => {
            const osc = audioCtx.createOscillator();
            osc.frequency.value = f;
            osc.connect(lofiGain);
            osc.start();
        });
        lofiGain.connect(audioCtx.destination);
        nodes['lofi'] = lofiGain;

        const chimeGain = audioCtx.createGain();
        chimeGain.gain.value = 0.25;
        chimeGain.connect(audioCtx.destination);
        nodes['chimes'] = chimeGain;
        setInterval(() => {
            if (isPlaying && nodes['chimes'].gain.value > 0.05) {
                const cFreqs = [523.25, 659.25, 783.99, 1046.50];
                const f = cFreqs[Math.floor(Math.random() * cFreqs.length)];
                const osc = audioCtx.createOscillator();
                const g = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(f, audioCtx.currentTime);
                g.gain.setValueAtTime(nodes['chimes'].gain.value * 0.4, audioCtx.currentTime);
                g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 3.0);
                osc.connect(g).connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 3.1);
            }
        }, 3200);

        const birdGain = audioCtx.createGain();
        birdGain.gain.value = 0.15;
        nodes['birds'] = birdGain;
        setInterval(() => {
            if (isPlaying && nodes['birds'].gain.value > 0.05) {
                const osc = audioCtx.createOscillator();
                const g = audioCtx.createGain();
                osc.type = 'sine';
                const now = audioCtx.currentTime;
                osc.frequency.setValueAtTime(2400, now);
                osc.frequency.exponentialRampToValueAtTime(3200, now + 0.1);
                osc.frequency.exponentialRampToValueAtTime(2600, now + 0.2);
                g.gain.setValueAtTime(nodes['birds'].gain.value * 0.3, now);
                g.gain.exponentialRampToTimeConstant(0.001, now + 0.22);
                osc.connect(g).connect(audioCtx.destination);
                osc.start();
                osc.stop(now + 0.25);
            }
        }, 4500);
    }

    function toggleAudio() {
        const btn = document.getElementById('masterBtn');
        if (!isPlaying) {
            if (!audioCtx) initSynthesizers();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            isPlaying = true;
            btn.textContent = "⏸️ Pause Audio";
            btn.style.background = "#f43f5e";
            btn.style.color = "white";
        } else {
            if (audioCtx) audioCtx.suspend();
            isPlaying = false;
            btn.textContent = "▶️ Start Audio";
            btn.style.background = "#38bdf8";
            btn.style.color = "#0f172a";
        }
    }

    function setGain(name, val) {
        if (nodes[name]) {
            nodes[name].gain.value = parseFloat(val);
        }
    }
    </script>
    </body>
    </html>
    """


def get_virtual_pet_widget(current_mood="Happy"):
    pet_mood_map = {
        "Happy": {"icon": "🐱", "face": "😸", "msg": "Mochi is doing happy wiggles with you! ✨"},
        "Sad": {"icon": "🐱", "face": "🥺", "msg": "Mochi is giving you a warm snuggle & cozy cocoa ☕💙"},
        "Angry": {"icon": "🐱", "face": "🧘", "msg": "Mochi is breathing in... and out... with you 🌿"},
        "Stressed": {"icon": "🐱", "face": "🌸", "msg": "Mochi placed a peaceful flower on your head 🌸"},
        "Neutral": {"icon": "🐱", "face": "🎧", "msg": "Mochi is chilling with headphones listening to lo-fi 🎵"},
    }
    data = pet_mood_map.get(current_mood, pet_mood_map["Happy"])

    return f"""
    <div style="background:linear-gradient(135deg, #1e1b4b, #312e81); border-radius:24px; padding:22px;
                color:white; border:2px solid #818cf8; box-shadow:0 12px 30px rgba(0,0,0,0.25); text-align:center;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:13px; font-weight:700; color:#c7d2fe;">🐾 MOCHI THE MOOD PET</span>
            <span style="background:rgba(255,255,255,0.15); padding:3px 10px; border-radius:20px; font-size:12px;">Mood: {current_mood}</span>
        </div>
        <div id="mochiPet" style="font-size:65px; margin:8px 0; display:inline-block; transition:transform 0.2s; cursor:pointer;" onclick="this.style.transform='scale(1.25) rotate(15deg)'; setTimeout(()=>this.style.transform='scale(1)', 300); document.getElementById('mochiSpeech').textContent='Purrrrr! ❤️ Mochi loves your company!';">
            {data['face']}
        </div>
        <div id="mochiSpeech" style="font-size:14px; color:#e0e7ff; font-weight:600; margin-bottom:12px; min-height:36px;">{data['msg']}</div>
        <div style="display:flex; justify-content:center; gap:8px;">
            <button style="background:#4338ca; color:white; border:none; padding:8px 16px; border-radius:12px; font-weight:700; cursor:pointer; font-size:13px;" onclick="document.getElementById('mochiSpeech').textContent='🍪 Nom Nom! Mochi loved that tasty treat! ✨'; document.getElementById('mochiPet').textContent='😻'; setTimeout(()=>document.getElementById('mochiPet').textContent='{data['face']}', 1500);">🍪 Treat</button>
            <button style="background:#6366f1; color:white; border:none; padding:8px 16px; border-radius:12px; font-weight:700; cursor:pointer; font-size:13px;" onclick="document.getElementById('mochiSpeech').textContent='💖 *Purrrrr* Mochi is purring happily in your lap!'; document.getElementById('mochiPet').textContent='🥰'; setTimeout(()=>document.getElementById('mochiPet').textContent='{data['face']}', 1500);">💖 Pet</button>
            <button style="background:#818cf8; color:#0f172a; border:none; padding:8px 16px; border-radius:12px; font-weight:700; cursor:pointer; font-size:13px;" onclick="document.getElementById('mochiSpeech').textContent='🎾 Mochi did a backflip to catch the ball!'; document.getElementById('mochiPet').textContent='😺'; setTimeout(()=>document.getElementById('mochiPet').textContent='{data['face']}', 1500);">🎾 Play</button>
        </div>
    </div>
    """


def get_fortune_cookie_widget():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 15px; font-family: 'Inter', system-ui, sans-serif;
        background: linear-gradient(135deg, #1e293b, #0f172a); color: white;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        min-height: 260px;
    }
    .cookie {
        font-size: 70px; cursor: pointer; transition: transform 0.2s;
        filter: drop-shadow(0 8px 15px rgba(251,191,36,0.35));
    }
    .cookie:hover { transform: scale(1.15) rotate(-5deg); }
    .scroll {
        display: none; background: #fef08a; color: #713f12; padding: 14px 22px;
        border-radius: 12px; margin-top: 15px; font-weight: 700; font-size: 15px;
        max-width: 450px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        animation: dropIn 0.3s ease-out;
    }
    @keyframes dropIn { from { opacity:0; transform:translateY(-10px); } to { opacity:1; transform:translateY(0); } }
    </style>
    </head>
    <body>
    <div class="cookie" id="cookieIcon" onclick="crackCookie()">🥠</div>
    <div style="font-size:13px; color:#94a3b8; margin-top:6px;" id="hint">Click the Golden Cookie to crack it open!</div>
    <div class="scroll" id="fortuneScroll"></div>

    <script>
    const fortunes = [
        "✨ Today brings unexpected joy and calm clarity.",
        "🌟 You are much stronger than the storm you weathered.",
        "🌿 Slow down. The universe has your back today.",
        "💙 Someone truly appreciates your kind presence.",
        "🌈 A beautiful new perspective is arriving soon.",
        "💫 Small gentle steps create huge transformations."
    ];

    function crackCookie() {
        const icon = document.getElementById('cookieIcon');
        const scroll = document.getElementById('fortuneScroll');
        const hint = document.getElementById('hint');
        icon.textContent = "💥";
        setTimeout(() => {
            icon.textContent = "✨🥠✨";
            const quote = fortunes[Math.floor(Math.random() * fortunes.length)];
            scroll.textContent = quote;
            scroll.style.display = 'block';
            hint.textContent = "🥠 Fortune unlocked for today!";
        }, 180);
    }
    </script>
    </body>
    </html>
    """


def get_zen_darts_game():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 15px; font-family: 'Inter', system-ui, sans-serif;
        background: radial-gradient(circle at 50% 10%, #1e1b4b, #090d16);
        color: white; display: flex; flex-direction: column; align-items: center;
        min-height: 680px; overflow: hidden;
    }
    .header {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; max-width: 620px; margin-bottom: 10px;
        background: rgba(255,255,255,0.06); padding: 10px 18px;
        border-radius: 18px; border: 1px solid rgba(255,255,255,0.1);
    }
    .stat { font-weight: 700; color: #f43f5e; font-size: 15px; }
    canvas {
        background: rgba(15,23,42,0.85); border: 2px solid rgba(244,63,94,0.3);
        border-radius: 22px; box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        cursor: crosshair; display: block;
    }
    .hint { margin-top: 10px; font-size: 13px; color: #cbd5e1; }
    </style>
    </head>
    <body>
    <div class="header">
        <div class="stat">🎯 Score: <span id="dartScore">0</span></div>
        <div class="stat">⭐ Bullseyes: <span id="dartBullseyes">0</span></div>
        <div class="stat" style="color:#38bdf8;">🌸 Zen Lotus Target</div>
    </div>
    <canvas id="dartCanvas" width="600" height="500"></canvas>
    <div class="hint">Aim and click anywhere to throw glowing darts at the floating Lotus target!</div>

    <script>
    const canvas = document.getElementById('dartCanvas');
    const ctx = canvas.getContext('2d');
    const scoreEl = document.getElementById('dartScore');
    const bullseyesEl = document.getElementById('dartBullseyes');

    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function playDartSound(isBullseye = false) {
        try {
            if (!audioCtx) audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = isBullseye ? 'triangle' : 'sine';
            const freq = isBullseye ? 880 : 520;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + (isBullseye ? 0.4 : 0.2));
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + (isBullseye ? 0.45 : 0.22));
        } catch(e) {}
    }

    let targetX = 300, targetY = 160, targetVx = 2.2, targetVy = 0.8;
    let darts = [], hits = [], score = 0, bullseyes = 0;

    canvas.addEventListener('click', e => {
        const rect = canvas.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const clickY = e.clientY - rect.top;

        // Animate dart throw from bottom
        darts.push({
            startX: 300, startY: 490,
            endX: clickX, endY: clickY,
            curX: 300, curY: 490,
            progress: 0,
            color: '#f43f5e'
        });
    });

    function drawTarget() {
        // Outer rings
        const rings = [
            { r: 90, color: 'rgba(244,63,94,0.15)', stroke: '#f43f5e' },
            { r: 65, color: 'rgba(56,189,248,0.2)', stroke: '#38bdf8' },
            { r: 40, color: 'rgba(250,204,21,0.25)', stroke: '#facc15' },
            { r: 18, color: '#f43f5e', stroke: '#ffffff' }
        ];

        rings.forEach(ring => {
            ctx.beginPath();
            ctx.arc(targetX, targetY, ring.r, 0, Math.PI * 2);
            ctx.fillStyle = ring.color;
            ctx.fill();
            ctx.strokeStyle = ring.stroke;
            ctx.lineWidth = 2.5;
            ctx.stroke();
        });

        // Center lotus emoji
        ctx.font = "20px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText("🌸", targetX, targetY);
    }

    function loop() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Move target smoothly
        targetX += targetVx;
        targetY += targetVy;
        if (targetX < 120 || targetX > canvas.width - 120) targetVx = -targetVx;
        if (targetY < 80 || targetY > 240) targetVy = -targetVy;

        drawTarget();

        // Update darts
        for (let i = darts.length - 1; i >= 0; i--) {
            let d = darts[i];
            d.progress += 0.12;
            d.curX = d.startX + (d.endX - d.startX) * d.progress;
            d.curY = d.startY + (d.endY - d.startY) * d.progress;

            ctx.beginPath();
            ctx.arc(d.curX, d.curY, 6 * (1.2 - d.progress * 0.4), 0, Math.PI * 2);
            ctx.fillStyle = "#ffffff";
            ctx.shadowBlur = 10;
            ctx.shadowColor = "#f43f5e";
            ctx.fill();
            ctx.shadowBlur = 0;

            if (d.progress >= 1) {
                // Check distance to target
                const dist = Math.sqrt((d.endX - targetX)**2 + (d.endY - targetY)**2);
                if (dist < 18) {
                    score += 50;
                    bullseyes++;
                    playDartSound(true);
                    hits.push({ x: d.endX, y: d.endY, text: "🌸 BULLSEYE! +50", alpha: 1 });
                } else if (dist < 40) {
                    score += 25;
                    playDartSound(false);
                    hits.push({ x: d.endX, y: d.endY, text: "✨ +25", alpha: 1 });
                } else if (dist < 65) {
                    score += 15;
                    playDartSound(false);
                    hits.push({ x: d.endX, y: d.endY, text: "+15", alpha: 1 });
                } else if (dist < 90) {
                    score += 5;
                    playDartSound(false);
                    hits.push({ x: d.endX, y: d.endY, text: "+5", alpha: 1 });
                }
                scoreEl.textContent = score;
                bullseyesEl.textContent = bullseyes;
                darts.splice(i, 1);
            }
        }

        // Draw hit feedback
        for (let i = hits.length - 1; i >= 0; i--) {
            let h = hits[i];
            ctx.font = "bold 16px Inter, sans-serif";
            ctx.fillStyle = `rgba(254, 240, 138, ${h.alpha})`;
            ctx.fillText(h.text, h.x, h.y);
            h.y -= 1;
            h.alpha -= 0.025;
            if (h.alpha <= 0) hits.splice(i, 1);
        }

        requestAnimationFrame(loop);
    }
    loop();
    </script>
    </body>
    </html>
    """


def get_mood_tarot_widget():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; }
    body {
        margin: 0; padding: 20px; font-family: 'Inter', system-ui, sans-serif;
        background: radial-gradient(circle at 50% 10%, #2e1065, #0f051d);
        color: white; display: flex; flex-direction: column; align-items: center; justify-content: center;
        min-height: 600px;
    }
    .title { font-size: 24px; font-weight: 800; color: #c084fc; margin-bottom: 4px; }
    .subtitle { font-size: 13px; color: #cbd5e1; margin-bottom: 24px; }
    .cards-row { display: flex; gap: 20px; justify-content: center; max-width: 780px; width: 100%; }
    .tarot-slot { flex: 1; display: flex; flex-direction: column; align-items: center; }
    .slot-label { font-size: 13px; font-weight: 700; color: #e9d5ff; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
    .card {
        width: 100%; aspect-ratio: 2/3.2; perspective: 1000px; cursor: pointer;
    }
    .card-inner {
        width: 100%; height: 100%; position: relative;
        transform-style: preserve-3d; transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        border-radius: 20px; box-shadow: 0 12px 35px rgba(0,0,0,0.5);
    }
    .card.flipped .card-inner { transform: rotateY(180deg); }
    .card-front, .card-back {
        position: absolute; inset: 0; backface-visibility: hidden;
        border-radius: 20px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; padding: 18px; text-align: center;
        border: 2px solid rgba(192,132,252,0.4);
    }
    .card-front {
        background: linear-gradient(135deg, #3b0764, #1e1b4b);
        box-shadow: inset 0 0 25px rgba(192,132,252,0.2);
    }
    .card-back {
        background: linear-gradient(135deg, #4c1d95, #1e1b4b);
        transform: rotateY(180deg); border-color: #facc15;
    }
    .btn-reset {
        margin-top: 25px; background: linear-gradient(135deg, #a855f7, #6366f1);
        color: white; border: none; padding: 12px 28px; border-radius: 20px;
        font-weight: 800; font-size: 14px; cursor: pointer; box-shadow: 0 6px 20px rgba(168,85,247,0.4);
    }
    .btn-reset:hover { transform: scale(1.05); }
    </style>
    </head>
    <body>
    <div class="title">🃏 Mystic Mind & Soul Tarot</div>
    <div class="subtitle">Click each of the 3 sacred cards to unveil wisdom for your Mind, Heart, and Spirit</div>
    <div class="cards-row">
        <div class="tarot-slot">
            <div class="slot-label">🧠 Mind</div>
            <div class="card" id="card0" onclick="flipTarot(0)">
                <div class="card-inner">
                    <div class="card-front"><div style="font-size:42px;">🔮</div><div style="font-size:12px; margin-top:8px; opacity:.7;">Tap to Reveal</div></div>
                    <div class="card-back" id="back0"></div>
                </div>
            </div>
        </div>
        <div class="tarot-slot">
            <div class="slot-label">💖 Heart</div>
            <div class="card" id="card1" onclick="flipTarot(1)">
                <div class="card-inner">
                    <div class="card-front"><div style="font-size:42px;">✨</div><div style="font-size:12px; margin-top:8px; opacity:.7;">Tap to Reveal</div></div>
                    <div class="card-back" id="back1"></div>
                </div>
            </div>
        </div>
        <div class="tarot-slot">
            <div class="slot-label">🌟 Spirit</div>
            <div class="card" id="card2" onclick="flipTarot(2)">
                <div class="card-inner">
                    <div class="card-front"><div style="font-size:42px;">🌌</div><div style="font-size:12px; margin-top:8px; opacity:.7;">Tap to Reveal</div></div>
                    <div class="card-back" id="back2"></div>
                </div>
            </div>
        </div>
    </div>
    <button class="btn-reset" onclick="initTarot()">🔄 Reshuffle Deck</button>

    <script>
    const deck = [
        { name: "The Sun", icon: "☀️", msg: "Radiant clarity and warmth illuminate your thoughts." },
        { name: "The Star", icon: "⭐", msg: "Renewed hope, calm peace, and deep spiritual healing." },
        { name: "The Moon", icon: "🌙", msg: "Trust your intuition. Peace awaits beyond fear." },
        { name: "The Empress", icon: "🌸", msg: "Nurture yourself with kindness and rest." },
        { name: "Strength", icon: "🦁", msg: "Soft gentleness is your greatest inner power." },
        { name: "The Hermit", icon: "🕯️", msg: "Quiet moments of contemplation bring immense wisdom." },
        { name: "The Magician", icon: "🪄", msg: "You have all the creative tools needed to thrive." },
        { name: "Temperance", icon: "🌊", msg: "Harmonious balance and flow return to your spirit." }
    ];

    function initTarot() {
        const shuffled = [...deck].sort(() => Math.random() - 0.5);
        for (let i = 0; i < 3; i++) {
            const cardEl = document.getElementById('card' + i);
            const backEl = document.getElementById('back' + i);
            cardEl.classList.remove('flipped');
            backEl.innerHTML = `
                <div style="font-size:36px; margin-bottom:4px;">${shuffled[i].icon}</div>
                <div style="font-weight:800; font-size:15px; color:#fef08a; margin-bottom:6px;">${shuffled[i].name}</div>
                <div style="font-size:12px; color:#e0e7ff; line-height:1.4;">${shuffled[i].msg}</div>
            `;
        }
    }

    function flipTarot(idx) {
        document.getElementById('card' + idx).classList.add('flipped');
    }

    initTarot();
    </script>
    </body>
    </html>
    """


def get_zen_sand_garden():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { box-sizing: border-box; user-select: none; margin: 0; padding: 0; }
    body { background: #1c1917; color: white; font-family: 'Inter', sans-serif; overflow: hidden; display: flex; flex-direction: column; align-items: center; }
    .toolbar {
        position: absolute; top: 15px; z-index: 10; display: flex; gap: 10px;
        background: rgba(41,37,36,0.85); backdrop-filter: blur(10px); padding: 10px 18px;
        border-radius: 20px; border: 1px solid rgba(255,255,255,0.15); align-items: center;
    }
    .btn-tool {
        background: rgba(255,255,255,0.1); color: #f5f5f4; border: none; padding: 6px 14px;
        border-radius: 12px; font-weight: 700; cursor: pointer; font-size: 13px;
    }
    .btn-tool.active, .btn-tool:hover { background: #d97706; color: white; }
    canvas { display: block; width: 100vw; height: 100vh; cursor: crosshair; }
    </style>
    </head>
    <body>
    <div class="toolbar">
        <span style="font-size:13px; font-weight:700; color:#fbbf24;">🪨 Japanese Zen Sand Garden</span>
        <button class="btn-tool active" id="rakeBtn" onclick="setMode('rake')">🌾 Bamboo Rake</button>
        <button class="btn-tool" id="stoneBtn" onclick="setMode('stone')">🪨 River Stone</button>
        <button class="btn-tool" id="sakuraBtn" onclick="setMode('sakura')">🌸 Sakura Petal</button>
        <button class="btn-tool" onclick="resetSand()">🧹 Smooth Sand</button>
    </div>
    <canvas id="sandCanvas"></canvas>

    <script>
    const canvas = document.getElementById('sandCanvas');
    const ctx = canvas.getContext('2d');
    let w = canvas.width = window.innerWidth;
    let h = canvas.height = window.innerHeight;

    window.onresize = () => {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
        resetSand();
    };

    let mode = 'rake', isDown = false, lastX = 0, lastY = 0;

    function setMode(m) {
        mode = m;
        document.querySelectorAll('.btn-tool').forEach(b => b.classList.remove('active'));
        if (m === 'rake') document.getElementById('rakeBtn').classList.add('active');
        if (m === 'stone') document.getElementById('stoneBtn').classList.add('active');
        if (m === 'sakura') document.getElementById('sakuraBtn').classList.add('active');
    }

    function resetSand() {
        ctx.fillStyle = '#e7dfcf';
        ctx.fillRect(0, 0, w, h);

        // Gentle sand noise pattern
        for (let i = 0; i < 4000; i++) {
            ctx.fillStyle = Math.random() > 0.5 ? 'rgba(0,0,0,0.03)' : 'rgba(255,255,255,0.05)';
            ctx.fillRect(Math.random() * w, Math.random() * h, 2, 2);
        }
    }

    resetSand();

    function drawRakeLine(x1, y1, x2, y2) {
        const offsets = [-14, -7, 0, 7, 14];
        offsets.forEach(off => {
            ctx.beginPath();
            ctx.moveTo(x1 + off, y1 + off);
            ctx.lineTo(x2 + off, y2 + off);
            ctx.strokeStyle = '#c4b59d';
            ctx.lineWidth = 3.5;
            ctx.lineCap = 'round';
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(x1 + off + 1, y1 + off + 1);
            ctx.lineTo(x2 + off + 1, y2 + off + 1);
            ctx.strokeStyle = '#f8f4eb';
            ctx.lineWidth = 1.5;
            ctx.lineCap = 'round';
            ctx.stroke();
        });
    }

    canvas.addEventListener('mousedown', e => {
        isDown = true;
        lastX = e.clientX;
        lastY = e.clientY;

        if (mode === 'stone') {
            ctx.save();
            ctx.beginPath();
            ctx.ellipse(e.clientX, e.clientY, 28, 20, Math.random() * Math.PI, 0, Math.PI * 2);
            ctx.fillStyle = '#44403c';
            ctx.shadowBlur = 12;
            ctx.shadowColor = 'rgba(0,0,0,0.4)';
            ctx.fill();
            ctx.restore();
        } else if (mode === 'sakura') {
            ctx.font = "24px sans-serif";
            ctx.fillText("🌸", e.clientX - 12, e.clientY + 8);
        }
    });

    canvas.addEventListener('mousemove', e => {
        if (!isDown || mode !== 'rake') return;
        drawRakeLine(lastX, lastY, e.clientX, e.clientY);
        lastX = e.clientX;
        lastY = e.clientY;
    });

    window.addEventListener('mouseup', () => isDown = false);
    </script>
    </body>
    </html>
    """


def get_fireworks_zen():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    * { margin:0; padding:0; box-sizing:border-box; user-select:none; }
    body { background:#030712; overflow:hidden; font-family:'Inter',sans-serif; color:white; }
    #canvas { width:100vw; height:100vh; display:block; cursor:pointer; }
    .hud {
        position:absolute; top:20px; left:20px; z-index:10;
        background:rgba(15,23,42,0.75); backdrop-filter:blur(10px);
        padding:12px 20px; border-radius:18px; border:1px solid rgba(255,255,255,0.1);
    }
    .hud h3 { margin:0 0 4px; font-size:16px; color:#f43f5e; }
    .hud p { margin:0; font-size:13px; color:#94a3b8; }
    </style>
    </head>
    <body>
    <div class="hud">
        <h3>🎆 Midnight Zen Fireworks</h3>
        <p>Click anywhere in the starry night to launch sparkling celebration bursts.</p>
    </div>
    <canvas id="canvas"></canvas>

    <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    let w = canvas.width = window.innerWidth;
    let h = canvas.height = window.innerHeight;

    window.onresize = () => {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    };

    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function playBurstSound() {
        try {
            if (!audioCtx) audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            const f = 150 + Math.random() * 200;
            osc.frequency.setValueAtTime(f, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.5);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.55);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.6);
        } catch(e) {}
    }

    let particles = [];
    const colorSets = [
        ['#ff6b81', '#feca57', '#ff9ff3', '#54a0ff'],
        ['#1dd1a1', '#10ac84', '#00d2d3', '#54a0ff'],
        ['#ffd32a', '#ff3f34', '#ff5e57', '#ffa801']
    ];

    class Spark {
        constructor(x, y, colors) {
            this.x = x;
            this.y = y;
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 6 + 2;
            this.vx = Math.cos(angle) * speed;
            this.vy = Math.sin(angle) * speed;
            this.radius = Math.random() * 2.5 + 1.5;
            this.color = colors[Math.floor(Math.random() * colors.length)];
            this.alpha = 1;
            this.decay = Math.random() * 0.015 + 0.01;
        }
        update() {
            this.x += this.vx;
            this.y += this.vy;
            this.vy += 0.06; // Gravity
            this.vx *= 0.98;
            this.alpha -= this.decay;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = Math.max(0, this.alpha);
            ctx.shadowBlur = 10;
            ctx.shadowColor = this.color;
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.globalAlpha = 1;
        }
    }

    window.addEventListener('click', e => {
        playBurstSound();
        const colors = colorSets[Math.floor(Math.random() * colorSets.length)];
        for (let i = 0; i < 65; i++) {
            particles.push(new Spark(e.clientX, e.clientY, colors));
        }
    });

    function loop() {
        ctx.fillStyle = 'rgba(3, 7, 18, 0.2)';
        ctx.fillRect(0, 0, w, h);

        for (let i = particles.length - 1; i >= 0; i--) {
            let p = particles[i];
            p.update();
            p.draw();
            if (p.alpha <= 0) particles.splice(i, 1);
        }
        requestAnimationFrame(loop);
    }
    loop();
    </script>
    </body>
    </html>
    """

