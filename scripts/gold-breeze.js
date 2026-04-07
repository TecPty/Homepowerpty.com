/* Gold Breeze Background Animation */
(function() {
    const lerp = (a, b, t) => a + (b - a) * t;
    const rand = (min, max) => Math.random() * (max - min) + min;
    const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

    let mouse = { x: 0, y: 0 };
    let smoothMouse = { x: 0, y: 0 };

    document.addEventListener('mousemove', e => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    const PC = document.getElementById('particle-canvas');
    if (!PC) return;
    const pCtx = PC.getContext('2d', { alpha: true });
    let W, H;

    function resize() {
        if (PC.parentElement) {
            W = PC.width = PC.parentElement.clientWidth;
            H = PC.height = PC.parentElement.clientHeight;
        } else {
            W = PC.width = window.innerWidth;
            H = PC.height = window.innerHeight;
        }
    }
    resize();
    window.addEventListener('resize', resize);

    const LANES = [
        { baseY: 0.18, freq: 0.9, amp: 0.08, speed: 0.00026775, phase: rand(0, Math.PI * 2) },
        { baseY: 0.32, freq: 1.1, amp: 0.11, speed: 0.0002142, phase: rand(0, Math.PI * 2) },
        { baseY: 0.50, freq: 0.75, amp: 0.09, speed: 0.000306, phase: rand(0, Math.PI * 2) },
        { baseY: 0.65, freq: 1.3, amp: 0.12, speed: 0.0002448, phase: rand(0, Math.PI * 2) },
        { baseY: 0.80, freq: 0.85, amp: 0.07, speed: 0.0002907, phase: rand(0, Math.PI * 2) },
    ];

    function laneY(lane, progress, t) {
        const ph = lane.phase + t * lane.speed * 1000;
        const my = smoothMouse.y / H - 0.5;
        const wave = Math.sin(ph + progress * lane.freq * Math.PI * 2) * lane.amp * H;
        const wave2 = Math.sin(ph * 1.4 + progress * Math.PI * 3) * lane.amp * 0.3 * H;
        const mouseNudge = my * 0.06 * H * Math.sin(progress * Math.PI);
        return lane.baseY * H + wave + wave2 + mouseNudge;
    }

    class Particle {
        constructor(init) { this.init(init); }
        init(randX) {
            this.lane = LANES[Math.floor(rand(0, LANES.length))];
            this.progress = randX ? rand(0, 1) : rand(-0.02, 0.04);
            this.speed = rand(0.0006885, 0.00153);
            this.size = rand(0.8, 2.5);
            this.life = 0;
            this.maxLife = rand(0.35, 1);
            this.offset = rand(-55, 55);
            this.bright = rand(0.5, 1.0);
            this.twPhase = rand(0, Math.PI * 2);
            this.twSpeed = rand(0.025, 0.07);
        }
        update(t) {
            this.progress += this.speed;
            this.life += this.speed / this.maxLife;
            this.twPhase += this.twSpeed;
            if (this.progress > 1.06) this.init(false);
        }
        draw(t) {
            const x = this.progress * W;
            const y = laneY(this.lane, this.progress, t) + this.offset;
            const twinkle = 0.45 + 0.55 * Math.sin(this.twPhase);
            const fade = Math.sin(clamp(this.life, 0, 1) * Math.PI);
            const alpha = clamp(fade * twinkle * this.bright, 0, 0.8);
            if (alpha < 0.01) return;

            pCtx.save();
            pCtx.globalAlpha = alpha;
            pCtx.globalCompositeOperation = 'screen';

            const r = this.size * 6;
            const grd = pCtx.createRadialGradient(x, y, 0, x, y, r);
            grd.addColorStop(0, 'rgba(255,240,180,1)');
            grd.addColorStop(0.3, 'rgba(212,160,23,0.5)');
            grd.addColorStop(1, 'rgba(139,105,20,0)');
            pCtx.beginPath();
            pCtx.arc(x, y, r, 0, Math.PI * 2);
            pCtx.fillStyle = grd;
            pCtx.fill();

            pCtx.beginPath();
            pCtx.arc(x, y, this.size * 0.75, 0, Math.PI * 2);
            pCtx.fillStyle = `rgba(255,255,220,${alpha})`;
            pCtx.fill();
            pCtx.restore();
        }
    }

    class Mote {
        constructor() { this.reset(true); }
        reset(init) {
            this.x = rand(0, W || window.innerWidth);
            this.y = init ? rand(0, H || window.innerHeight) : rand(0, H);
            this.vx = rand(0.0918, 0.34425);
            this.vy = rand(-0.0612, 0.0612);
            this.size = rand(0.4, 1.4);
            this.alpha = rand(0.08, 0.32);
            this.color = Math.random() > 0.5 ? '#D4A017' : '#FFD700';
        }
        update() {
            this.x += this.vx;
            this.y += this.vy + Math.sin(this.x * 0.005) * 0.15;
            if (this.x > W + 10) {
                this.reset(false);
                this.x = -5;
            }
        }
        draw() {
            pCtx.save();
            pCtx.globalAlpha = this.alpha;
            pCtx.globalCompositeOperation = 'screen';
            pCtx.fillStyle = this.color;
            pCtx.beginPath();
            pCtx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            pCtx.fill();
            pCtx.restore();
        }
    }

    const particles = Array.from({ length: 150 }, () => new Particle(true));
    const motes = Array.from({ length: 80 }, () => new Mote());

    let startTime = null;

    function loop(ts) {
        if (!startTime) startTime = ts;
        const t = (ts - startTime) * 0.001;

        smoothMouse.x = lerp(smoothMouse.x, mouse.x, 0.04);
        smoothMouse.y = lerp(smoothMouse.y, mouse.y, 0.04);
        
        pCtx.clearRect(0, 0, W, H);

        const bgGrd = pCtx.createRadialGradient(
            smoothMouse.x, smoothMouse.y, 0,
            smoothMouse.x, smoothMouse.y, W * 0.35
        );
        bgGrd.addColorStop(0, 'rgba(212,160,23,0.02)');
        bgGrd.addColorStop(1, 'rgba(0,0,0,0)');
        pCtx.fillStyle = bgGrd;
        pCtx.fillRect(0, 0, W, H);

        motes.forEach(m => { m.update(); m.draw(); });
        particles.forEach(p => { p.update(t); p.draw(t); });

        requestAnimationFrame(loop);
    }

    requestAnimationFrame(loop);
})();
