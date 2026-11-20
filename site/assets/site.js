document.querySelectorAll("table").forEach((table) => {
  const wrapper = document.createElement("div");
  wrapper.className = "table-scroll";
  wrapper.tabIndex = 0;
  wrapper.setAttribute("role", "region");
  wrapper.setAttribute("aria-label", "Scrollable data table");
  table.before(wrapper);
  wrapper.append(table);
});

document.querySelectorAll("nav a").forEach((link) => {
  if (link.href === window.location.href.split("#")[0]) {
    link.setAttribute("aria-current", "page");
  }
});

const joinViews = {
  trimmed: ["pair-trimmed", "Trimmed: crossing extensions are removed from each original piece. Complete smaller Lanterns survive within the retained geometry."],
  original: ["pair-original", "Original: the complete neighbouring pieces interleave across the central mirror plane. Some points are shared; other crossing branches are distinct."],
  reassigned: ["pair-reassigned", "Reassigned: no geometry is removed. Colour assigns every point to its side of the plane. The whole original fractal stays unchanged, while the newly divided parts differ from the original pieces."],
  removed: ["removed", "Removed extensions only: the parts discarded by the local cut. These include entire miniature Lanterns absent from every other original piece."]
};
document.querySelectorAll("[data-join]").forEach((button) => {
  button.addEventListener("click", () => {
    const [file, caption] = joinViews[button.dataset.join];
    const image = document.getElementById("join-image");
    image.src = "assets/joins/" + file + ".png";
    image.alt = caption;
    document.getElementById("join-caption").textContent = caption;
    document.querySelectorAll("[data-join]").forEach((other) => {
      other.setAttribute("aria-pressed", String(other === button));
    });
  });
});

const film = document.getElementById("hero-film");
const toggle = document.querySelector(".film-toggle");
if (film && toggle) {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const reflectPlayback = () => {
    toggle.textContent = film.paused ? "Play film" : "Pause film";
  };
  toggle.hidden = false;
  toggle.addEventListener("click", () => {
    if (film.paused) film.play().catch(reflectPlayback);
    else film.pause();
  });
  film.addEventListener("play", reflectPlayback);
  film.addEventListener("pause", reflectPlayback);
  film.addEventListener("ended", reflectPlayback);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) film.pause();
  });
  reducedMotion.addEventListener("change", () => {
    if (reducedMotion.matches) film.pause();
  });
  // Keep the still poster until the viewer chooses playback when motion is reduced.
  if (!reducedMotion.matches) film.play().catch(reflectPlayback);
}
