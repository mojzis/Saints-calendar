// Renders today, the next 7 days and a month grid from days.json.
const MONTHS = ["leden", "únor", "březen", "duben", "květen", "červen",
  "červenec", "srpen", "září", "říjen", "listopad", "prosinec"];
const fmtLong = new Intl.DateTimeFormat("cs-CZ", { weekday: "long", day: "numeric", month: "long" });
const fmtWd = new Intl.DateTimeFormat("cs-CZ", { weekday: "short" });

const key = (d) => String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
const sameDay = (a, b) => key(a) === key(b) && a.getFullYear() === b.getFullYear();

function el(tag, attrs = {}, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v; else e.setAttribute(k, v);
  }
  for (const k of kids) if (k != null) e.append(k);
  return e;
}

// Lines describing one day: saints, then holiday.
function describe(info, { titleTag = "span" } = {}) {
  const out = [];
  for (const s of info.saints || []) {
    out.push(el(titleTag, { class: "s" }, s.title + " ", el("span", { class: "rank " + s.rank }, s.rank)));
  }
  if (info.holiday) out.push(el("span", { class: "s holiday" }, info.holiday));
  if (!out.length) out.push(el("span", { class: "n" }, "—"));
  return out;
}

function renderToday(days, today) {
  const info = days[key(today)] || {};
  const box = document.getElementById("today");
  box.replaceChildren();
  const image = (info.saints || []).find((s) => s.image);
  if (image) {
    box.classList.add("has-image");
    box.append(el("img", { src: image.image, alt: image.title }));
  }
  const text = el("div", {}, el("div", { class: "date" }, "Dnes je " + fmtLong.format(today)));
  if (info.saints) {
    text.append(el("div", { class: "label" }, info.saints.length > 1 ? "Dnešní světci" : "Dnešní světec"));
    for (const s of info.saints) {
      text.append(el("div", { class: "saint" },
        el("h1", {}, s.title), el("span", { class: "rank " + s.rank }, s.rank)));
    }
  } else if (info.holiday) {
    text.append(el("h1", { class: "holiday" }, info.holiday));
  } else {
    text.append(el("h1", {}, "Dnes bez památky světce"));
  }
  if (info.saints && info.holiday) text.append(el("div", { class: "names holiday" }, info.holiday));
  box.append(text);
}

function renderWeek(days, today) {
  const list = document.getElementById("week");
  list.replaceChildren();
  for (let i = 1; i <= 7; i++) {
    const d = addDays(today, i);
    list.append(el("li", {},
      el("div", { class: "d" }, el("b", {}, d.getDate() + ". " + (d.getMonth() + 1) + "."), fmtWd.format(d)),
      el("div", {}, ...describe(days[key(d)] || {}))));
  }
}

function makeMonth(days, today) {
  let year = today.getFullYear();
  let month = today.getMonth();
  let selected = today;
  const grid = document.getElementById("grid");
  const detail = document.getElementById("detail");

  function showDetail(d) {
    selected = d;
    detail.replaceChildren(
      el("div", { class: "label" }, fmtLong.format(d)),
      ...describe(days[key(d)] || {}));
  }

  function render() {
    document.getElementById("month-title").textContent = MONTHS[month] + " " + year;
    grid.replaceChildren(...["po", "út", "st", "čt", "pá", "so", "ne"].map((w) => el("div", { class: "wd" }, w)));
    const first = new Date(year, month, 1);
    const lead = (first.getDay() + 6) % 7; // Monday first
    for (let i = 0; i < lead; i++) grid.append(el("button", { class: "empty", tabindex: "-1", "aria-hidden": "true" }));
    const count = new Date(year, month + 1, 0).getDate();
    for (let n = 1; n <= count; n++) {
      const d = new Date(year, month, n);
      const info = days[key(d)] || {};
      const cls = [sameDay(d, today) && "is-today", sameDay(d, selected) && "selected"].filter(Boolean).join(" ");
      const top = (info.saints || [])[0];
      const btn = el("button", { class: cls, "aria-label": fmtLong.format(d) },
        el("span", { class: "num" }, String(n)),
        top ? el("span", { class: "cs " + top.rank }, top.title) :
          info.holiday ? el("span", { class: "cs svátek" }, info.holiday) : null,
        top || info.holiday ? el("span", { class: "dot" }) : null);
      btn.addEventListener("click", () => {
        grid.querySelector(".selected")?.classList.remove("selected");
        btn.classList.add("selected");
        showDetail(d);
      });
      grid.append(btn);
    }
  }

  function shift(delta) {
    month += delta;
    if (month < 0) { month = 11; year--; }
    if (month > 11) { month = 0; year++; }
    render();
  }
  document.getElementById("prev").addEventListener("click", () => shift(-1));
  document.getElementById("next").addEventListener("click", () => shift(1));
  render();
  showDetail(today);
}

fetch("days.json")
  .then((r) => r.json())
  .then((days) => {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    renderToday(days, today);
    renderWeek(days, today);
    makeMonth(days, today);
  })
  .catch(() => {
    document.getElementById("today").textContent = "Data se nepodařilo načíst.";
  });
