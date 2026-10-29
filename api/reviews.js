/**
 * TW&CO Premium â€” Google Business Profile Reviews (Vercel serverless)
 * Requires authorized, verified business profile and Google API access.
 * No sample reviews are returned: without credentials, frontend shows a transparent fallback.
 */
const snapshot = require("../assets/avaliacoes-verificadas.json");
let cache = { expires: 0, payload: null };
const REQUIRED = ["GBP_CLIENT_ID", "GBP_CLIENT_SECRET", "GBP_REFRESH_TOKEN", "GBP_ACCOUNT_ID", "GBP_LOCATION_ID"];
function fail(res, code, status) { return res.status(code).json({ status, reviews: [] }); }
async function getOAuthToken() {
  const form = new URLSearchParams({
    client_id: process.env.GBP_CLIENT_ID,
    client_secret: process.env.GBP_CLIENT_SECRET,
    refresh_token: process.env.GBP_REFRESH_TOKEN,
    grant_type: "refresh_token"
  });
  const response = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: form
  });
  if (!response.ok) throw new Error("Google OAuth unavailable");
  const json = await response.json();
  if (!json.access_token) throw new Error("OAuth returned no token");
  return json.access_token;
}
async function getAllReviews(token) {
  const account = String(process.env.GBP_ACCOUNT_ID).replace(/\D/g, "");
  const location = String(process.env.GBP_LOCATION_ID).replace(/\D/g, "");
  if (!account || !location) throw new Error("invalid GBP IDs");
  const base = `https://mybusiness.googleapis.com/v4/ac¶»§q«^