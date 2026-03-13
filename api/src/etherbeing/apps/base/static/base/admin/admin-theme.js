(function () {
  function bootCursorField() {
    var body = document.body;
    if (!body || document.getElementById("etherbeing-admin-cursor")) {
      return;
    }

    var canvas = document.createElement("canvas");
    canvas.id = "etherbeing-admin-cursor";
    body.prepend(canvas);
    var context = canvas.getContext("2d");
    if (!context) {
      return;
    }

    var pointer = {
      x: window.innerWidth * 0.5,
      y: window.innerHeight * 0.5,
      tx: window.innerWidth * 0.5,
      ty: window.innerHeight * 0.5,
    };
    var orbs = [];
    for (var index = 0; index < 18; index += 1) {
      orbs.push({
        radius: 120 - index * 4,
        hue: 220 + index * 8,
        alpha: 0.12 - index * 0.004,
        drift: 0.2 + index * 0.02,
      });
    }

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }

    function render() {
      pointer.x += (pointer.tx - pointer.x) * 0.12;
      pointer.y += (pointer.ty - pointer.y) * 0.12;
      context.clearRect(0, 0, canvas.width, canvas.height);

      for (var i = 0; i < orbs.length; i += 1) {
        var orb = orbs[i];
        var x = pointer.x + Math.cos(Date.now() * 0.0003 * orb.drift + i) * (18 + i * 3);
        var y = pointer.y + Math.sin(Date.now() * 0.0004 * orb.drift + i) * (14 + i * 2);
        var gradient = context.createRadialGradient(x, y, 0, x, y, orb.radius);
        gradient.addColorStop(0, "hsla(" + orb.hue + ", 100%, 72%, " + orb.alpha + ")");
        gradient.addColorStop(0.45, "hsla(" + (orb.hue + 48) + ", 100%, 70%, " + orb.alpha * 0.65 + ")");
        gradient.addColorStop(1, "hsla(" + (orb.hue + 88) + ", 100%, 60%, 0)");
        context.fillStyle = gradient;
        context.beginPath();
        context.arc(x, y, orb.radius, 0, Math.PI * 2);
        context.fill();
      }

      requestAnimationFrame(render);
    }

    window.addEventListener("resize", resize);
    window.addEventListener("mousemove", function (event) {
      pointer.tx = event.clientX;
      pointer.ty = event.clientY;
    });
    window.addEventListener("touchmove", function (event) {
      if (event.touches[0]) {
        pointer.tx = event.touches[0].clientX;
        pointer.ty = event.touches[0].clientY;
      }
    }, { passive: true });

    resize();
    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootCursorField);
  } else {
    bootCursorField();
  }
})();
