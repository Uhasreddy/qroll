// Shared helpers. window.QROLL_API is set in config.js (written by infra/deploy.sh).
const API = (window.QROLL_API || "").replace(/\/$/, "");

async function api(path, { method = "GET", body, pin } = {}) {
  const headers = {};
  if (body) headers["Content-Type"] = "application/json";
  if (pin) headers["X-Organizer-Pin"] = pin;
  let res;
  try {
    res = await fetch(API + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  } catch (e) {
    return { status: 0, data: { error: "Network error: cannot reach the QRoll API." } };
  }
  let data = {};
  try { data = await res.json(); } catch (e) { /* empty body */ }
  return { status: res.status, data };
}

function showMsg(el, text, kind = "err") {
  el.textContent = text;
  el.className = `msg show ${kind}`;
}
function hideMsg(el) { el.className = "msg"; }

function fmtTime(epoch) {
  return new Date(epoch * 1000).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

function pinKey(id) { return `qroll-pin-${id}`; }
function savePin(id, pin) { try { sessionStorage.setItem(pinKey(id), pin); } catch (e) {} }
function loadPin(id) { try { return sessionStorage.getItem(pinKey(id)) || ""; } catch (e) { return ""; } }

function param(name) { return new URLSearchParams(location.search).get(name) || ""; }

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
