!(function () {
  "use strict";
  gsap.registerPlugin(ScrollTrigger, SplitText);
  let t = document.querySelectorAll(".fade");
  t.forEach((t) => {
    gsap
      .timeline({
        scrollTrigger: { trigger: t, start: "top 90%", markers: !1 },
      })
      .to(t, { duration: 1.5, delay: 0.5, opacity: 1 });
  });
  let a = document.querySelectorAll(".fade-slide");
  a.forEach((t) => {
    let a = 80,
      e = { duration: 1.3, delay: 0.5, opacity: 0, ease: "power2.out" };
    t.hasAttribute("data-cs-slide-amount") &&
      (a = t.getAttribute("data-cs-slide-amount")),
      t.hasAttribute("data-cs-opacity") &&
        (e.opacity = t.getAttribute("data-cs-opacity")),
      t.hasAttribute("data-cs-ease") &&
        (e.ease = t.getAttribute("data-cs-ease")),
      t.hasAttribute("data-cs-duration") &&
        (e.duration = t.getAttribute("data-cs-duration")),
      t.hasAttribute("data-cs-delay") &&
        (e.delay = t.getAttribute("data-cs-delay")),
      t.classList.contains("right") && (e.x = a),
      t.classList.contains("left") && (e.x = -a),
      t.classList.contains("top") && (e.y = -a),
      t.classList.contains("bottom") && (e.y = a);
    gsap
      .timeline({
        scrollTrigger: { trigger: t, start: "top 90%", markers: !1 },
      })
      .from(t, e);
  });
  let e = document.querySelectorAll(".split_chars");
  e.forEach((t) => {
    let a = !0,
      e = {
        duration: 1.3,
        delay: 0.5,
        autoAlpha: 0,
        stagger: 0.15,
        ease: "power2.out",
      },
      r = { trigger: t, start: "top 90%", markers: !1 };
    t.hasAttribute("data-cs-duration") &&
      (e.duration = t.getAttribute("data-cs-duration")),
      t.hasAttribute("data-cs-delay") &&
        (e.delay = t.getAttribute("data-cs-delay")),
      t.hasAttribute("data-cs-ease") &&
        (e.ease = t.getAttribute("data-cs-ease")),
      t.hasAttribute("data-cs-stagger") &&
        (e.stagger = t.getAttribute("data-cs-stagger")),
      t.hasAttribute("data-cs-translate-x") &&
        (e.x = t.getAttribute("data-cs-translate-x")),
      t.hasAttribute("data-cs-translate-y") &&
        (e.y = t.getAttribute("data-cs-translate-y")),
      t.hasAttribute("data-cs-translate-x") ||
        t.hasAttribute("data-cs-translate-x") ||
        (e.x = 100),
      t.hasAttribute("data-cs-scroll-trigger") &&
        (a = t.getAttribute("data-cs-scroll-trigger")),
      t.hasAttribute("data-cs-trigger-start") &&
        (r.start = t.getAttribute("data-cs-trigger-start")),
      a && (e.scrollTrigger = r);
    let s = new SplitText(t, {
      type: "chars, words",
      tag: "span",
      charsClass: "d-inline-block",
    });
    gsap.from(s.chars, e);
  });
  let r = document.querySelectorAll(".move-line-3d");
  r.forEach((t) => {
    let a = "top 90%",
      e = {
        duration: 1,
        delay: 0.3,
        opacity: 0,
        rotationX: -80,
        force3D: !0,
        transformOrigin: "top center -50",
        stagger: 0.1,
      };
    t.hasAttribute("data-cs-start") && (a = t.getAttribute("data-cs-start")),
      t.hasAttribute("data-cs-duration") &&
        (e.duration = t.getAttribute("data-cs-duration")),
      t.hasAttribute("data-cs-delay") &&
        (e.delay = t.getAttribute("data-cs-delay")),
      t.hasAttribute("data-cs-opacity") &&
        (e.opacity = t.getAttribute("data-cs-opacity")),
      t.hasAttribute("data-cs-stagger") &&
        (e.stagger = t.getAttribute("data-cs-stagger")),
      t.hasAttribute("data-cs-rotate") &&
        (e.rotationX = t.getAttribute("data-cs-rotate")),
      t.hasAttribute("data-cs-origin") &&
        (e.transformOrigin = t.getAttribute("data-cs-origin"));
    let r = gsap.timeline({
        scrollTrigger: {
          trigger: t,
          start: a,
          duration: e.duration,
          scrub: !1,
          markers: !1,
        },
      }),
      s = new SplitText(t, { type: "lines" }).split({ type: "lines" });
    gsap.set(t, { perspective: 400 }), r.from(s.lines, e);
  });
  let s = document.querySelectorAll(".cursor");
  s.forEach((t) => {
    let a = { duration: 0.5, ease: "power3" };
    t.hasAttribute("data-cs-duration") &&
      (a.duration = parseFloat(t.getAttribute("data-cs-duration"))),
      t.hasAttribute("data-cs-ease") &&
        (a.ease = parseFloat(t.getAttribute("data-cs-ease"))),
      gsap.set(t, { xPercent: -50, yPercent: -50 });
    let e = gsap.quickTo(t, "x", a),
      r = gsap.quickTo(t, "y", a);
    window.addEventListener("mousemove", (t) => {
      e(t.clientX), r(t.clientY);
    });
  });
})();
