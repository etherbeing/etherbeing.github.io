(function () {
  function bootSidebarSizing() {
    var sidebar = document.getElementById("nav-sidebar");
    var contentStart = document.getElementById("content-start");
    if (!sidebar || !contentStart) {
      return;
    }

    function syncSidebarHeight() {
      var contentHeight = contentStart.getBoundingClientRect().height;
      if (!contentHeight) {
        sidebar.style.removeProperty("max-height");
        return;
      }
      sidebar.style.maxHeight = Math.ceil(contentHeight) + "px";
    }

    syncSidebarHeight();
    window.addEventListener("resize", syncSidebarHeight);

    if (typeof ResizeObserver !== "undefined") {
      var observer = new ResizeObserver(syncSidebarHeight);
      observer.observe(contentStart);
    }
  }

  function bootSidebarToggle() {
    var sidebar = document.getElementById("nav-sidebar");
    var main = document.getElementById("main");
    if (!sidebar || !main || document.querySelector(".etherbeing-sidebar-toggle")) {
      return;
    }

    var button = document.createElement("button");
    button.type = "button";
    button.className = "etherbeing-sidebar-toggle";
    button.setAttribute("aria-label", "Hide sidebar");
    button.setAttribute("aria-pressed", "false");
    button.innerHTML = (
      '<span class="etherbeing-eye-icon" aria-hidden="true">' +
      '<svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">' +
      '<path class="etherbeing-eye-shape" d="M1.5 12S5.5 5 12 5s10.5 7 10.5 7-4 7-10.5 7S1.5 12 1.5 12Z"></path>' +
      '<circle class="etherbeing-eye-pupil" cx="12" cy="12" r="3.2"></circle>' +
      '<path class="etherbeing-eye-slash" d="M4 20 20 4"></path>' +
      '</svg>' +
      "</span>"
    );

    function setHidden(isHidden) {
      main.classList.toggle("etherbeing-sidebar-hidden", isHidden);
      if (isHidden) {
        main.appendChild(button);
      } else {
        sidebar.appendChild(button);
      }
      button.setAttribute("aria-label", isHidden ? "Show sidebar" : "Hide sidebar");
      button.setAttribute("aria-pressed", isHidden ? "true" : "false");
      try {
        window.localStorage.setItem("etherbeing-admin-sidebar-hidden", isHidden ? "1" : "0");
      } catch (error) {
        void error;
      }
    }

    var stored = null;
    try {
      stored = window.localStorage.getItem("etherbeing-admin-sidebar-hidden");
    } catch (error) {
      stored = null;
    }
    sidebar.appendChild(button);
    setHidden(stored === "1");

    button.addEventListener("click", function () {
      setHidden(!main.classList.contains("etherbeing-sidebar-hidden"));
    });
  }

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
    document.addEventListener("DOMContentLoaded", function () {
      bootCursorField();
      bootSidebarSizing();
      bootSidebarToggle();
    });
  } else {
    bootCursorField();
    bootSidebarSizing();
    bootSidebarToggle();
  }
})();
