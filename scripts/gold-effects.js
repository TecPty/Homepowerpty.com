/**
 * HomePower PTY — Gold Background Effect
 * Canvas-based floating gold orbs + light particles
 * Mimics the look of warm gold light reflected on glass/metal
 */
(function () {
    const canvas = document.createElement('canvas');
    canvas.id = 'gold-bg-canvas';
    document.body.prepend(canvas);

    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // ─── Gold Orbs ────────────────────────────────────────────
    const ORBS = 5;
    const orbs = [];

    function randBetween(a, b) {
        return a + Math.random() * (b - a);
    }

    for (let i = 0; i < ORBS; i++) {
        orbs.push({
            x: randBetween(0.1, 0.9),      // fractional 0-1
            y: randBetween(0.0, 1.0),
            r: randBetween(200, 400),       // radius px
            alpha: randBetween(0.04, 0.10),
            speedX: randBetween(-0.00008, 0.00008),
            speedY: randBetween(-0.00005, 0.00005),
            breathSpeed: randBetween(0.003, 0.006),
            breathPhase: randBetween(0, Math.PI * 2),
            color: [
                `rgba(201,168,76,`,
                `rgba(180,150,60,`,
                `rgba(220,190,100,`,
            ][Math.floor(Math.random() * 3)]
        });
    }

    // ─── Light Particles ──────────────────────────────────────
    const PARTICLES = 30;
    const particles = [];

    for (let i = 0; i < PARTICLES; i++) {
        particles.push({
            x: Math.random(),
            y: Math.random(),
            size: randBetween(1, 3),
            alpha: randBetween(0.1, 0.5),
            speedX: randBetween(-0.0002, 0.0002),
            speedY: randBetween(-0.0003, -0.0001), // drift up
            twinkleSpeed: randBetween(0.01, 0.025),
            twinklePhase: randBetween(0, Math.PI * 2),
        });
    }

    // ─── Render loop ──────────────────────────────────────────
    let frame = 0;

    function draw() {
        frame++;
        const W = canvas.width;
        const H = canvas.height;

        // Clear with the brand dark background
        ctx.clearRect(0, 0, W, H);
        ctx.fillStyle = '#111111';
        ctx.fillRect(0, 0, W, H);

        // Draw orbs
        orbs.forEach(orb => {
            // Move
            orb.x += orb.speedX;
            orb.y += orb.speedY;

            // Wrap around
            if (orb.x < -0.3) orb.x = 1.3;
            if (orb.x > 1.3)  orb.x = -0.3;
            if (orb.y < -0.3) orb.y = 1.3;
            if (orb.y > 1.3)  orb.y = -0.3;

            // Breathing alpha
            const breath = Math.sin(frame * orb.breathSpeed + orb.breathPhase);
            const alpha = orb.alpha + breath * 0.04;

            const grd = ctx.createRadialGradient(
                orb.x * W, orb.y * H, 0,
                orb.x * W, orb.y * H, orb.r
            );
            grd.addColorStop(0, orb.color + Math.min(alpha, 0.15) + ')');
            grd.addColorStop(0.5, orb.color + Math.min(alpha * 0.4, 0.08) + ')');
            grd.addColorStop(1, 'rgba(0,0,0,0)');

            ctx.fillStyle = grd;
            ctx.beginPath();
            ctx.arc(orb.x * W, orb.y * H, orb.r, 0, Math.PI * 2);
            ctx.fill();
        });

        // Draw particles
        particles.forEach(p => {
            p.x += p.speedX;
            p.y += p.speedY;

            // Wrap
            if (p.y < -0.05) p.y = 1.05;
            if (p.x < 0) p.x = 1;
            if (p.x > 1) p.x = 0;

            // Twinkle
            const twinkle = (Math.sin(frame * p.twinkleSpeed + p.twinklePhase) + 1) / 2;
            const alpha = p.alpha * twinkle;

            ctx.beginPath();
            ctx.arc(p.x * W, p.y * H, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(201, 168, 76, ${alpha})`;
            ctx.fill();
        });

        requestAnimationFrame(draw);
    }

    draw();
})();
