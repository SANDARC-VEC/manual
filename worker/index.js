/**
 * Redirect-fixing shim in front of static asset serving.
 *
 * The manual is published at https://vec.sandarc.org/manual/, but the
 * /manual prefix is stripped before requests reach this Worker — the
 * built site sits at the root of the Worker's own URL space. Static
 * asset serving (html_handling: auto-trailing-slash) answers a
 * slash-less page URL like /start-a-team/Accrediting-a-VE with a
 * redirect whose Location is the root-relative worker-space path
 * (/start-a-team/Accrediting-a-VE/). Relayed as-is to the browser,
 * that Location escapes the /manual prefix and lands on a
 * vec.sandarc.org 404.
 *
 * So the Worker runs first (assets.run_worker_first) and rewrites
 * every same-origin redirect Location into a relative reference.
 * Browsers resolve relative Locations against the public URL the
 * visitor actually requested, so the mount prefix is preserved
 * whatever it is. Non-redirect responses pass through untouched.
 */

/**
 * Relative path that leads from `fromPath` to `toPath` when resolved
 * the way browsers resolve a relative URL (against `fromPath` minus
 * its last segment). Both arguments are absolute pathnames.
 */
function relativePath(fromPath, toPath) {
  const from = fromPath.split("/").slice(1, -1);
  const to = toPath.split("/").slice(1);
  let common = 0;
  while (
    common < from.length &&
    common < to.length - 1 &&
    from[common] === to[common]
  ) {
    common += 1;
  }
  const rel =
    "../".repeat(from.length - common) + to.slice(common).join("/");
  return rel === "" ? "./" : rel;
}

export default {
  async fetch(request, env) {
    const response = await env.ASSETS.fetch(request);
    const location = response.headers.get("Location");
    if (!location || response.status < 300 || response.status >= 400) {
      return response;
    }

    const requestUrl = new URL(request.url);
    const target = new URL(location, requestUrl);
    if (target.origin !== requestUrl.origin) {
      // A redirect off-site (none expected) is not ours to rewrite.
      return response;
    }

    const rewritten = new Response(response.body, response);
    rewritten.headers.set(
      "Location",
      relativePath(requestUrl.pathname, target.pathname) +
        target.search +
        target.hash
    );
    return rewritten;
  },
};
