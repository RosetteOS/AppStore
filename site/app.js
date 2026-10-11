/**
 * Rosette App Store Interactive Frontend Logic
 */

// Embedded fallback catalog in case fetch is offline / local file preview
const FALLBACK_CATALOG = {
  "apps": [
    {
      "id": "mainsail",
      "name": "Mainsail Web Interface",
      "category": "web_ui",
      "icon": "mainsail",
      "description": "Default rich web interface for Klipper and Moonraker with extensive customization and multi-camera support.",
      "author": "Mainsail Crew",
      "version": "2.12.0",
      "is_builtin": true,
      "builtin_path": "/usr/share/mainsail",
      "config_target": "macros/mainsail.cfg",
      "website": "https://mainsail.xyz",
      "source_url": "https://github.com/mainsail-crew/mainsail"
    },
    {
      "id": "fluidd",
      "name": "Fluidd Web Interface",
      "category": "web_ui",
      "icon": "fluidd",
      "description": "Clean, responsive and lightweight web interface for Klipper with real-time status and powerful toolpath visualization.",
      "author": "Fluidd Core Team",
      "version": "1.37.6",
      "is_builtin": false,
      "download_url": "https://raw.githubusercontent.com/RosetteOS/AppStore/main/packages/fluidd-v1.37.6.zip",
      "sha256": "9fe5bcd4a443f4cccd20cef222e70cc334a874070b21d116097a28405b0ed456",
      "install_path": "/usr/data/rosetteos/apps/fluidd",
      "config_url": "https://raw.githubusercontent.com/RosetteOS/AppStore/main/configs/fluidd.cfg",
      "config_target": "macros/fluidd.cfg",
      "website": "https://fluidd.xyz",
      "source_url": "https://github.com/fluidd-core/fluidd"
    },
    {
      "id": "guppyscreen",
      "name": "GuppyScreen Touch UI",
      "category": "touch_ui",
      "icon": "guppyscreen",
      "description": "Default ultra-fast native LVGL-based touchscreen interface optimized for Ingenic X2000 MIPS.",
      "author": "Rosette & GuppyScreen Team",
      "version": "1.0.0",
      "is_builtin": true,
      "builtin_path": "/opt/guppyscreen/guppyscreen",
      "source_url": "https://github.com/RosetteOS/GuppyScreen"
    },
    {
      "id": "helixscreen",
      "name": "HelixScreen Touch UI",
      "category": "touch_ui",
      "icon": "helixscreen",
      "description": "Modern, lightweight, and customizable touchscreen interface for Klipper built for high performance and touch gestures.",
      "author": "Preston Brown",
      "version": "1.0.2",
      "is_builtin": false,
      "download_url": "https://raw.githubusercontent.com/RosetteOS/AppStore/main/packages/helixscreen-k1-v1.0.2.tar.gz",
      "sha256": "d1b068f5218982ae6a7f6af839b54919683d9fe7f667c12a52bf34dd5c3e0564",
      "install_path": "/usr/data/rosetteos/apps/helixscreen",
      "executable": "bin/helix-screen",
      "website": "https://helixscreen.org",
      "source_url": "https://github.com/prestonbrown/helixscreen"
    },
    {
      "id": "timelapse",
      "name": "Moonraker Timelapse",
      "category": "plugin",
      "icon": "timelapse",
      "description": "Capture automated frame timelapses and renders during 3D prints using FFmpeg and Moonraker.",
      "author": "mainsail-crew",
      "version": "0.0.12",
      "is_builtin": false,
      "download_url": "https://raw.githubusercontent.com/RosetteOS/AppStore/main/packages/timelapse-v0.0.12.zip",
      "sha256": "7b65e5e6aa4f1aaff426633d86389871c5722ac5c80ec05587887cae4d3a9374",
      "install_path": "/usr/data/rosetteos/apps/timelapse",
      "moonraker_component": "component/timelapse.py",
      "config_url": "https://raw.githubusercontent.com/RosetteOS/AppStore/main/configs/timelapse.cfg",
      "config_target": "macros/timelapse.cfg",
      "klipper_include": true,
      "website": "https://github.com/mainsail-crew/moonraker-timelapse",
      "source_url": "https://github.com/mainsail-crew/moonraker-timelapse"
    },
    {
      "id": "mobileraker",
      "name": "Mobileraker Companion",
      "category": "plugin",
      "icon": "mobileraker",
      "description": "Companion service for Mobileraker mobile app (iOS & Android) enabling real-time push notifications for print status, progress, M117, and errors.",
      "author": "Patrick Schmidt (Clon1998)",
      "version": "0.5.0",
      "is_builtin": false,
      "download_url": "https://raw.githubusercontent.com/RosetteOS/AppStore/main/packages/mobileraker-v0.5.0.zip",
      "sha256": "b9d6b3ad11c7eed4fbe577f887dc8fcd4c2d1058a27b3ef276bd6a8335c72d5d",
      "install_path": "/usr/data/rosetteos/apps/mobileraker",
      "config_url": "https://raw.githubusercontent.com/RosetteOS/AppStore/main/configs/mobileraker.conf",
      "config_target": "mobileraker.conf",
      "website": "https://github.com/Clon1998/mobileraker",
      "source_url": "https://github.com/Clon1998/mobileraker_companion"
    },
    {
      "id": "spoolman",
      "name": "Spoolman",
      "category": "plugin",
      "icon": "spoolman",
      "description": "Filament spool management service with native Moonraker, Mainsail, and Fluidd integration. Tracks weights, usage, and material parameters.",
      "author": "Donkie",
      "version": "0.18.0",
      "is_builtin": false,
      "download_url": "https://raw.githubusercontent.com/RosetteOS/AppStore/main/packages/spoolman-v0.18.0.zip",
      "sha256": "58d1b5368aee6474ffa37d504b56d8a10ba2b0dd89cf0d711e92369fdc41c878",
      "install_path": "/usr/data/rosetteos/apps/spoolman",
      "website": "https://github.com/Donkie/Spoolman",
      "source_url": "https://github.com/Donkie/Spoolman"
    },
    {
      "id": "octoapp",
      "name": "OctoApp Companion",
      "category": "plugin",
      "icon": "octoapp",
      "icon_url": "https://raw.githubusercontent.com/RosetteOS/AppStore/main/icons/octoapp.png",
      "description": "Companion service for OctoApp mobile app (iOS & Android) with real-time push notifications, print progress, webcam streaming, and remote control for Moonraker/Klipper.",
      "author": "Christian Würthner (crysxd)",
      "version": "3.2.4-rosetteos.2",
      "is_builtin": false,
      "download_url": "https://raw.githubusercontent.com/RosetteOS/AppStore/main/packages/octoapp-v3.2.4-rosetteos.2.zip",
      "sha256": "ce20da477e87a01d56a49a3e28032e2a5695c2644fe55c9e5ab6ca6dce6d9c4e",
      "install_path": "/usr/data/rosetteos/apps/octoapp",
      "cleanup_config_files": [
        "octoapp.conf",
        "octoapp-moonraker.cfg"
      ],
      "website": "https://octoapp.eu",
      "source_url": "https://github.com/crysxd/OctoApp-Plugin"
    }
  ]
};

// SVG Icons Registry
const ICONS = {
  web: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>`,
  monitor: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>`,
  puzzle: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19.439 7.85c0-1.57.802-2.54 2.137-2.54.385 0 .736.064 1.05.188L22.626 2H18.5a2.5 2.5 0 0 0-2.5 2.5v.939c0 1.57-.97 2.373-2.54 2.373s-2.54-.803-2.54-2.373V4.5A2.5 2.5 0 0 0 8.42 2H4.294l-.001 3.498c.314-.124.665-.188 1.05-.188 1.335 0 2.137.97 2.137 2.54s-.802 2.54-2.137 2.54c-.385 0-.736-.064-1.05-.188L4.293 14H8.5a2.5 2.5 0 0 0 2.5-2.5v-.939c0-1.57.97-2.373 2.54-2.373s2.54.803 2.54 2.373v.939A2.5 2.5 0 0 0 18.58 14h4.126l.001-3.498c-.314.124-.665.188-1.05.188-1.335 0-2.137-.97-2.137-2.54z"></path></svg>`,
  wrench: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>`,
  camera: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>`,
  bell: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>`,
  spool: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="3.5"></circle><line x1="12" y1="2" x2="12" y2="8.5"></line><line x1="12" y1="15.5" x2="12" y2="22"></line><line x1="2" y1="12" x2="8.5" y2="12"></line><line x1="15.5" y1="12" x2="22" y2="12"></line></svg>`,
  smartphone: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>`,
  external: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>`,
  github: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>`
};

function getCategoryIcon(cat, id) {
  if (id === "timelapse") return ICONS.camera;
  if (id === "mobileraker") return ICONS.bell;
  if (id === "spoolman") return ICONS.spool;
  if (id === "octoapp") return ICONS.smartphone;
  if (cat === "web_ui") return ICONS.web;
  if (cat === "touch_ui") return ICONS.monitor;
  if (cat === "plugin") return ICONS.puzzle;
  if (cat === "tool") return ICONS.wrench;
  return ICONS.puzzle;
}

function getAppIconMarkup(app) {
  const fallback = getCategoryIcon(app.category, app.id);
  const iconUrl = app.icon_url || `https://raw.githubusercontent.com/RosetteOS/AppStore/main/icons/${encodeURIComponent(app.id)}.png`;
  let parsedUrl;
  try {
    parsedUrl = new URL(iconUrl, window.location.href);
  } catch (err) {
    return fallback;
  }
  if (parsedUrl.protocol !== "https:" && parsedUrl.protocol !== "http:") return fallback;

  const safeUrl = parsedUrl.href.replace(/&/g, "&amp;").replace(/"/g, "&quot;");
  return `<img class="app-logo" src="${safeUrl}" alt="" loading="lazy" decoding="async" onerror="this.hidden=true;this.nextElementSibling.hidden=false"><span class="app-logo-fallback" hidden>${fallback}</span>`;
}

function getCategoryName(cat) {
  const map = {
    web_ui: "Web UI",
    touch_ui: "Touch UI",
    plugin: "Plugin",
    tool: "System Tool"
  };
  return map[cat] || cat;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

let catalogApps = [];
let currentCategory = "all";
let searchQuery = "";

async function loadCatalog() {
  try {
    const res = await fetch("apps.json");
    if (!res.ok) throw new Error("Network response was not ok");
    const data = await res.json();
    catalogApps = data.apps || [];
  } catch (err) {
    console.warn("Using embedded fallback catalog:", err);
    catalogApps = FALLBACK_CATALOG.apps;
  }
  updateStats();
  render();
}

function updateStats() {
  const countAll = catalogApps.length;
  const countWeb = catalogApps.filter(a => a.category === "web_ui").length;
  const countTouch = catalogApps.filter(a => a.category === "touch_ui").length;
  const countPlugin = catalogApps.filter(a => a.category === "plugin").length;
  const countTool = catalogApps.filter(a => a.category === "tool").length;

  document.getElementById("stat-apps-count").textContent = countAll;
  document.getElementById("count-all").textContent = countAll;
  document.getElementById("count-web_ui").textContent = countWeb;
  document.getElementById("count-touch_ui").textContent = countTouch;
  document.getElementById("count-plugin").textContent = countPlugin;
  document.getElementById("count-tool").textContent = countTool;
}

function getInstallCommand(app) {
  if (app.is_builtin) {
    if (app.category === "web_ui") return `rosetteos-app set-active-web ${app.id}`;
    if (app.category === "touch_ui") return `rosetteos-app set-active-touch ${app.id}`;
    return `# ${app.name} is pre-installed in base firmware`;
  }
  return `rosetteos-app install ${app.id}`;
}

function render() {
  const grid = document.getElementById("apps-grid");
  const empty = document.getElementById("empty-state");

  const filtered = catalogApps.filter(app => {
    const matchesCat = currentCategory === "all" || app.category === currentCategory;
    const q = searchQuery.toLowerCase().trim();
    const matchesSearch = !q || 
      app.name.toLowerCase().includes(q) || 
      app.id.toLowerCase().includes(q) || 
      app.description.toLowerCase().includes(q) || 
      (app.author && app.author.toLowerCase().includes(q));

    return matchesCat && matchesSearch;
  });

  if (filtered.length === 0) {
    grid.style.display = "none";
    empty.style.display = "block";
    return;
  }

  grid.style.display = "grid";
  empty.style.display = "none";

  grid.innerHTML = filtered.map(app => {
    const iconMarkup = getAppIconMarkup(app);
    const catName = getCategoryName(app.category);
    const installCmd = getInstallCommand(app);

    return `
      <div class="app-card" data-app-id="${app.id}">
        <div>
          <div class="card-top">
            <div class="app-icon-wrap">
              ${iconMarkup}
            </div>
            <div class="app-title-area">
              <h3 class="app-name">${app.name}</h3>
              <div class="app-author">by ${app.author || "Community"}</div>
              <div class="app-badges">
                <span class="badge badge-${app.category}">${catName}</span>
                ${app.is_builtin ? '<span class="badge badge-builtin">Built-in</span>' : ''}
                <span class="badge badge-version">v${app.version}</span>
              </div>
            </div>
          </div>

          <p class="app-desc">${app.description}</p>
        </div>

        <div>
          <div class="card-install-box">
            <code>${installCmd}</code>
            <button class="copy-btn" onclick="copyCommand('${installCmd}', this)" title="Copy command">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            </button>
          </div>

          <div class="card-actions">
            <button class="details-btn" onclick="openModal('${app.id}')">
              View Details &rarr;
            </button>
            <div class="card-links">
              ${app.website ? `<a href="${app.website}" target="_blank" rel="noopener noreferrer" class="card-link-icon" title="Website">${ICONS.external}</a>` : ''}
              ${app.source_url ? `<a href="${app.source_url}" target="_blank" rel="noopener noreferrer" class="card-link-icon" title="Source Code">${ICONS.github}</a>` : ''}
            </div>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// Category filter clicks
document.getElementById("category-filters").addEventListener("click", (e) => {
  const pill = e.target.closest(".cat-pill");
  if (!pill) return;

  document.querySelectorAll(".cat-pill").forEach(p => p.classList.remove("active"));
  pill.classList.add("active");

  currentCategory = pill.dataset.category;
  render();
});

// Search input handling
const searchInput = document.getElementById("search-input");
const clearSearchBtn = document.getElementById("clear-search");

searchInput.addEventListener("input", (e) => {
  searchQuery = e.target.value;
  clearSearchBtn.style.display = searchQuery ? "block" : "none";
  render();
});

clearSearchBtn.addEventListener("click", () => {
  searchInput.value = "";
  searchQuery = "";
  clearSearchBtn.style.display = "none";
  searchInput.focus();
  render();
});

// Keyboard shortcut '/' to search
window.addEventListener("keydown", (e) => {
  if (e.key === "/" && document.activeElement !== searchInput) {
    e.preventDefault();
    searchInput.focus();
  } else if (e.key === "Escape") {
    closeModal();
  }
});

function resetFilters() {
  currentCategory = "all";
  searchQuery = "";
  searchInput.value = "";
  clearSearchBtn.style.display = "none";
  document.querySelectorAll(".cat-pill").forEach(p => {
    p.classList.toggle("active", p.dataset.category === "all");
  });
  render();
}

// Copy to Clipboard
function copyCommand(text, btnElement) {
  navigator.clipboard.writeText(text).then(() => {
    showToast("Copied to clipboard: " + text);
    if (btnElement) {
      const origHtml = btnElement.innerHTML;
      btnElement.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="#2ea043" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width: 18px; height: 18px;">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      `;
      setTimeout(() => {
        btnElement.innerHTML = origHtml;
      }, 1500);
    }
  }).catch(err => {
    console.error("Clipboard copy failed:", err);
  });
}

function showToast(msg) {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 2200);
}

// Modal management
function openModal(appId) {
  const app = catalogApps.find(a => a.id === appId);
  if (!app) return;

  const modal = document.getElementById("app-modal");
  document.getElementById("modal-icon").innerHTML = getAppIconMarkup(app);
  document.getElementById("modal-name").textContent = app.name;
  document.getElementById("modal-author").textContent = "by " + (app.author || "Community");
  document.getElementById("modal-version").textContent = "v" + app.version;
  document.getElementById("modal-category").textContent = getCategoryName(app.category);
  document.getElementById("modal-category").className = `badge badge-${app.category}`;
  document.getElementById("modal-desc").textContent = app.description;

  const installCmd = getInstallCommand(app);
  document.getElementById("modal-cmd").textContent = installCmd;
  document.getElementById("modal-copy-btn").onclick = () => copyCommand(installCmd);

  document.getElementById("modal-install-path").textContent = app.install_path || (app.is_builtin ? "(Built-in firmware root)" : "-");
  document.getElementById("modal-config-target").textContent = app.config_target || "-";
  document.getElementById("modal-component").textContent = app.moonraker_component || "-";
  document.getElementById("modal-sha").textContent = app.sha256 ? `${app.sha256.substring(0, 16)}...` : (app.is_builtin ? "(Base firmware)" : "-");

  const changelogSection = document.getElementById("modal-changelog-section");
  const changelogContainer = document.getElementById("modal-changelog");
  if (changelogSection && changelogContainer) {
    const cl = app.changelog;
    if (Array.isArray(cl) && cl.length > 0) {
      changelogContainer.innerHTML = cl.map(entry => {
        if (typeof entry === "string") {
          return `<div class="changelog-entry"><ul class="changelog-items"><li>${escapeHtml(entry)}</li></ul></div>`;
        }
        const ver = escapeHtml(entry.version || app.version || "");
        const date = entry.date ? `<span class="changelog-date">${escapeHtml(entry.date)}</span>` : "";
        const items = Array.isArray(entry.changes) ? entry.changes : (entry.changes ? [entry.changes] : []);
        const itemsHtml = items.map(item => `<li>${escapeHtml(String(item))}</li>`).join("");
        return `
          <div class="changelog-entry">
            <div class="changelog-header">
              <span class="badge badge-version">v${ver}</span>
              ${date}
            </div>
            <ul class="changelog-items">${itemsHtml}</ul>
          </div>
        `;
      }).join("");
      changelogSection.style.display = "block";
    } else if (typeof cl === "string" && cl.trim()) {
      changelogContainer.innerHTML = `<div class="changelog-entry"><p>${escapeHtml(cl)}</p></div>`;
      changelogSection.style.display = "block";
    } else {
      changelogContainer.innerHTML = "";
      changelogSection.style.display = "none";
    }
  }

  const linksContainer = document.getElementById("modal-links");
  let linksHtml = "";
  if (app.website) {
    linksHtml += `<a href="${app.website}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline">${ICONS.external} Website</a>`;
  }
  if (app.source_url) {
    linksHtml += `<a href="${app.source_url}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline">${ICONS.github} Source Code</a>`;
  }
  if (app.download_url) {
    linksHtml += `<a href="${app.download_url}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline">Direct Download (.zip)</a>`;
  }
  linksContainer.innerHTML = linksHtml;

  modal.style.display = "flex";
  document.body.style.overflow = "hidden";
}

function closeModal() {
  const modal = document.getElementById("app-modal");
  modal.style.display = "none";
  document.body.style.overflow = "auto";
}

document.getElementById("app-modal").addEventListener("click", (e) => {
  if (e.target.id === "app-modal") {
    closeModal();
  }
});

// Init on load
document.addEventListener("DOMContentLoaded", () => {
  loadCatalog();
});
