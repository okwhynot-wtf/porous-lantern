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
