// The public site lives under vec.sandarc.org/manual/, but the /manual
// prefix is stripped before requests reach this Worker, so the static
// asset router sees prefix-less paths. Its trailing-slash 307s are built
// from those stripped paths (e.g. /es -> Location: /es/), which sends
// browsers to the Django app at the domain root instead of back into the
// manual. Re-prefix root-relative redirect Locations before they leave.
const PUBLIC_PREFIX = "/manual";

export default {
  async fetch(request, env) {
    const response = await env.ASSETS.fetch(request);

    const isRedirect = response.status >= 300 && response.status < 400;
    const location = response.headers.get("Location");
    if (
      !isRedirect ||
      location === null ||
      !location.startsWith("/") ||
      location.startsWith("//") ||
      location.startsWith(`${PUBLIC_PREFIX}/`)
    ) {
      return response;
    }

    const headers = new Headers(response.headers);
    headers.set("Location", PUBLIC_PREFIX + location);
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
