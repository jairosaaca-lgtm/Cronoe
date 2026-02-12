const STORAGE_KEY = "cronoe-scoreboard-state";

const clockEl = document.getElementById("matchClock");
const periodLabel = document.getElementById("periodLabel");
const addedTimeBox = document.getElementById("addedTimeBox");

const startBtn = document.getElementById("startBtn");
const pauseBtn = document.getElementById("pauseBtn");
const resumeBtn = document.getElementById("resumeBtn");
const resetBtn = document.getElementById("resetBtn");

const targetMinuteSelect = document.getElementById("targetMinute");
const addedMinutesInput = document.getElementById("addedMinutes");
const showAddedBtn = document.getElementById("showAddedBtn");
const hideAddedBtn = document.getElementById("hideAddedBtn");

const homeNameInput = document.getElementById("homeName");
const awayNameInput = document.getElementById("awayName");
const homeScoreInput = document.getElementById("homeScore");
const awayScoreInput = document.getElementById("awayScore");

const primaryColorInput = document.getElementById("primaryColor");
const secondaryColorInput = document.getElementById("secondaryColor");
const textColorInput = document.getElementById("textColor");
const baseColorInput = document.getElementById("baseColor");
const gradientPresetSelect = document.getElementById("gradientPreset");
const fontPresetSelect = document.getElementById("fontPreset");
const surfacePresetSelect = document.getElementById("surfacePreset");

const fontsByPreset = {
  inter: '"Inter", system-ui, sans-serif',
  barlow: '"Barlow", "Inter", system-ui, sans-serif',
  oswald: '"Oswald", "Inter", system-ui, sans-serif',
  rajdhani: '"Rajdhani", "Inter", system-ui, sans-serif',
};

const themeByGradient = {
  ocean: { primary: "#19c2ff", secondary: "#8b5cf6", base: "#081021", text: "#eff4ff" },
  sunset: { primary: "#fb7185", secondary: "#f59e0b", base: "#21100c", text: "#fff3e9" },
  neon: { primary: "#22d3ee", secondary: "#a3e635", base: "#05080c", text: "#ebfff9" },
  mono: { primary: "#c7cedf", secondary: "#8e9ab1", base: "#101215", text: "#f5f7fb" },
};

const surfaceByPreset = {
  glass: { alpha: 0.84, blur: 14 },
  flat: { alpha: 0.94, blur: 0 },
  minimal: { alpha: 0.98, blur: 0 },
};

const state = {
  isRunning: false,
  elapsedMs: 0,
  startTs: null,
  targetMinute: 90,
  addedMinutes: 0,
  showAdded: false,
  periodLabel: "2T",
  theme: {
    primary: "#19c2ff",
    secondary: "#8b5cf6",
    text: "#eff4ff",
    base: "#081021",
    gradientPreset: "ocean",
    fontPreset: "inter",
    surfacePreset: "glass",
  },
};

function formatClock(ms) {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function applyTheme() {
  const root = document.documentElement;
  const font = fontsByPreset[state.theme.fontPreset] || fontsByPreset.inter;
  const surface = surfaceByPreset[state.theme.surfacePreset] || surfaceByPreset.glass;

  root.style.setProperty("--primary", state.theme.primary);
  root.style.setProperty("--secondary", state.theme.secondary);
  root.style.setProperty("--text", state.theme.text);
  root.style.setProperty("--base", state.theme.base);
  root.style.setProperty("--font-main", font);
  root.style.setProperty("--font-score", font);
  root.style.setProperty("--surface-alpha", String(surface.alpha));
  root.style.setProperty("--card-blur", `${surface.blur}px`);

  primaryColorInput.value = state.theme.primary;
  secondaryColorInput.value = state.theme.secondary;
  textColorInput.value = state.theme.text;
  baseColorInput.value = state.theme.base;
  gradientPresetSelect.value = state.theme.gradientPreset;
  fontPresetSelect.value = state.theme.fontPreset;
  surfacePresetSelect.value = state.theme.surfacePreset;
}

function saveState() {
  const payload = {
    ...state,
    startTs: state.isRunning ? Date.now() - state.elapsedMs : null,
    homeName: homeNameInput.value,
    awayName: awayNameInput.value,
    homeScore: homeScoreInput.value,
    awayScore: awayScoreInput.value,
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;

    const saved = JSON.parse(raw);
    state.isRunning = Boolean(saved.isRunning);
    state.elapsedMs = Number(saved.elapsedMs || 0);
    state.targetMinute = Number(saved.targetMinute || 90);
    state.addedMinutes = Number(saved.addedMinutes || 0);
    state.showAdded = Boolean(saved.showAdded);
    state.periodLabel = saved.periodLabel || "2T";

    if (saved.theme) {
      state.theme = {
        ...state.theme,
        ...saved.theme,
      };
    }

    homeNameInput.value = saved.homeName || "LOCAL";
    awayNameInput.value = saved.awayName || "VISITA";
    homeScoreInput.value = saved.homeScore || "0";
    awayScoreInput.value = saved.awayScore || "0";

    if (state.isRunning && saved.startTs) {
      state.startTs = saved.startTs;
      state.elapsedMs = Date.now() - saved.startTs;
    }
  } catch {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function updateAddedBoxVisibility() {
  const targetMs = state.targetMinute * 60 * 1000;
  const reachTarget = state.elapsedMs >= targetMs;
  const shouldShow = state.showAdded || (reachTarget && state.addedMinutes > 0);

  addedTimeBox.textContent = `+${state.addedMinutes}`;
  addedTimeBox.classList.toggle("hidden", !shouldShow);
}

function render() {
  clockEl.textContent = formatClock(state.elapsedMs);
  periodLabel.textContent = state.periodLabel;
  targetMinuteSelect.value = String(state.targetMinute);
  addedMinutesInput.value = String(state.addedMinutes);
  updateAddedBoxVisibility();
  applyTheme();
}

function setThemeFromPreset(preset) {
  const next = themeByGradient[preset];
  if (!next) return;
  state.theme.gradientPreset = preset;
  state.theme.primary = next.primary;
  state.theme.secondary = next.secondary;
  state.theme.base = next.base;
  state.theme.text = next.text;
}

function tick() {
  if (!state.isRunning || state.startTs === null) return;
  state.elapsedMs = Date.now() - state.startTs;
  render();
  saveState();
}

setInterval(tick, 250);

startBtn.addEventListener("click", () => {
  state.elapsedMs = 0;
  state.startTs = Date.now();
  state.isRunning = true;
  saveState();
  render();
});

pauseBtn.addEventListener("click", () => {
  if (!state.isRunning || state.startTs === null) return;
  state.elapsedMs = Date.now() - state.startTs;
  state.isRunning = false;
  state.startTs = null;
  saveState();
  render();
});

resumeBtn.addEventListener("click", () => {
  if (state.isRunning) return;
  state.startTs = Date.now() - state.elapsedMs;
  state.isRunning = true;
  saveState();
  render();
});

resetBtn.addEventListener("click", () => {
  state.isRunning = false;
  state.elapsedMs = 0;
  state.startTs = null;
  state.addedMinutes = 0;
  state.showAdded = false;
  state.targetMinute = 90;
  saveState();
  render();
});

targetMinuteSelect.addEventListener("change", () => {
  state.targetMinute = Number(targetMinuteSelect.value);
  state.periodLabel = state.targetMinute === 45 ? "1T" : "2T";
  saveState();
  render();
});

addedMinutesInput.addEventListener("input", () => {
  state.addedMinutes = Math.max(0, Number(addedMinutesInput.value || 0));
  saveState();
  render();
});

showAddedBtn.addEventListener("click", () => {
  state.showAdded = true;
  saveState();
  render();
});

hideAddedBtn.addEventListener("click", () => {
  state.showAdded = false;
  saveState();
  render();
});

gradientPresetSelect.addEventListener("change", () => {
  setThemeFromPreset(gradientPresetSelect.value);
  saveState();
  render();
});

fontPresetSelect.addEventListener("change", () => {
  state.theme.fontPreset = fontPresetSelect.value;
  saveState();
  render();
});

surfacePresetSelect.addEventListener("change", () => {
  state.theme.surfacePreset = surfacePresetSelect.value;
  saveState();
  render();
});

primaryColorInput.addEventListener("input", () => {
  state.theme.primary = primaryColorInput.value;
  saveState();
  render();
});

secondaryColorInput.addEventListener("input", () => {
  state.theme.secondary = secondaryColorInput.value;
  saveState();
  render();
});

textColorInput.addEventListener("input", () => {
  state.theme.text = textColorInput.value;
  saveState();
  render();
});

baseColorInput.addEventListener("input", () => {
  state.theme.base = baseColorInput.value;
  saveState();
  render();
});

[homeNameInput, awayNameInput, homeScoreInput, awayScoreInput].forEach((el) => {
  el.addEventListener("input", saveState);
});

window.addEventListener("beforeunload", saveState);

loadState();
render();
