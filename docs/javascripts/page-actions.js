/*
  "Copy as Markdown" and menu behaviour for the AI page actions control
  (overrides/partials/page-actions.html, styled in docs/stylesheets/
  extra.css under "9 — PAGE ACTIONS"). The assistant links in that control
  are plain links and work without this script.

  Copying fetches the page's Markdown export (written by the llms-source
  plugin) and cleans it up for pasting into a chat: the revision stamp
  moves to a footer and relative links become absolute public URLs.

  Safari only allows a clipboard write while the click that asked for it
  is still being handled, so awaiting the fetch first and then calling
  writeText() fails there with NotAllowedError. Instead the write starts
  synchronously with a ClipboardItem whose content is a promise that
  resolves once the fetch completes. The Markdown is also prefetched when
  the pointer or focus first reaches the control, so that promise is
  usually settled already.

  navigation.instant swaps the page content without reloading this
  script, and each page renders the control twice (beside the title and in
  the meta row; CSS shows one). So every listener is delegated from
  document, and everything is scoped to the control that was used.
*/
(function () {
  const COPIED = 'Copied page as Markdown';
  const MISSING = 'Markdown version not available';
  const FAILED = "Couldn't copy the page";

  // The export starts with "<!-- rev: <short sha> -->" (source_revision
  // in mkdocs.yml).
  const STAMP = /^<!-- rev: (\S+) -->\r?\n/;
  // Inline link and image targets, and reference definitions. <...>
  // targets are left alone.
  const INLINE_TARGET = /(\]\()([^\s()<>]+)/g;
  const REFERENCE_TARGET = /^( {0,3}\[[^\]\n]+\]:[ \t]*)([^\s<>]+)/gm;
  // Targets that are already absolute: a scheme (https:, mailto:, tel:),
  // protocol-relative, or a fragment within the page.
  const ABSOLUTE = /^(?:[a-z][a-z\d+.-]*:|\/\/|#)/i;
  // A translation's source (Page.es.md) has no page URL of its own.
  const TRANSLATION = /\.[a-z]{2}\.md$/;

  const cache = new Map();
  const prefetched = new WeakSet();

  // data-page-actions-md and -page are public URLs built from site_url.
  // Fetch from wherever this page is actually served (mkdocs serve, a
  // preview deploy) instead, by climbing from the current page to the
  // directory both URLs share.
  function servedUrl(mdUrl, pageUrl) {
    let shared = 0;
    while (shared < mdUrl.length && mdUrl[shared] === pageUrl[shared]) shared++;
    shared = mdUrl.lastIndexOf('/', shared - 1) + 1;
    const depth = pageUrl.slice(shared).split('/').length - 1;
    return new URL('../'.repeat(depth) + mdUrl.slice(shared), location.href).href;
  }

  // One request per URL; a failed one is forgotten so a later try refetches.
  function fetchMarkdown(url) {
    if (!cache.has(url)) {
      const request = fetch(url).then((response) => {
        if (!response.ok) throw new Error(`${response.status} ${url}`);
        return response.text();
      });
      request.catch(() => cache.delete(url));
      cache.set(url, request);
    }
    return cache.get(url);
  }

  // Resolve a relative target the way MkDocs does with use_directory_urls:
  // Page.md -> Page/, index.md -> its directory, fragments kept.
  function resolveTarget(target, mdUrl) {
    if (ABSOLUTE.test(target)) return target;
    const url = new URL(target, mdUrl);
    if (url.pathname.endsWith('.md') && !TRANSLATION.test(url.pathname)) {
      url.pathname = url.pathname.replace(/(?:\/index)?\.md$/, '/');
    }
    return url.href;
  }

  function prepareMarkdown(text, mdUrl, pageUrl) {
    const stamp = text.match(STAMP);
    const resolve = (match, before, target) => before + resolveTarget(target, mdUrl);
    const body = text
      .replace(STAMP, '')
      .replace(INLINE_TARGET, resolve)
      .replace(REFERENCE_TARGET, resolve)
      .trim();
    const footer = [`Source: ${pageUrl}`, `Markdown: ${mdUrl}`];
    if (stamp) footer.push(`Revision: ${stamp[1]}`);
    return `${body}\n\n---\n\n${footer.join('\n')}\n`;
  }

  function loadMarkdown(control) {
    const { pageActionsMd: mdUrl, pageActionsPage: pageUrl } = control.dataset;
    return fetchMarkdown(servedUrl(mdUrl, pageUrl))
      .then((text) => prepareMarkdown(text, mdUrl, pageUrl));
  }

  // Material's toast is not a live region, so the control's visually
  // hidden status span is what screen readers announce. It is cleared
  // first so the same message is announced again on a second copy.
  function announce(control, message) {
    if (window.alert$) window.alert$.next(message);
    const status = control.querySelector('.page-actions__status');
    status.textContent = '';
    setTimeout(() => { status.textContent = message; }, 100);
  }

  function copy(control) {
    const markdown = loadMarkdown(control);
    let written;
    if (window.ClipboardItem && navigator.clipboard.write) {
      written = navigator.clipboard.write([new ClipboardItem({
        'text/plain': markdown.then((text) => new Blob([text], { type: 'text/plain' })),
      })]);
    } else {
      written = markdown.then((text) => navigator.clipboard.writeText(text));
    }
    written.then(
      () => announce(control, COPIED),
      () => markdown.then(() => announce(control, FAILED), () => announce(control, MISSING)),
    );
  }

  // Closing the menu hides whatever had focus inside it, so focus goes
  // back to the summary that opened it.
  function closeMenu(menu) {
    const hadFocus = menu.contains(document.activeElement);
    menu.open = false;
    if (hadFocus) menu.querySelector('summary').focus();
  }

  // The copy button is rendered hidden, so it stays out of the menu
  // without JavaScript and without the Clipboard API (an insecure context
  // or an old browser). Show it on every page where copying can work.
  if (navigator.clipboard) {
    const showCopy = () => {
      document.querySelectorAll('[data-page-actions-copy]').forEach((button) => {
        button.hidden = false;
      });
    };
    if (window.document$) window.document$.subscribe(showCopy);
    else showCopy();

    const prefetch = (event) => {
      const control = event.target.closest('.page-actions');
      if (!control || prefetched.has(control)) return;
      prefetched.add(control);
      // A failure here is reported if the reader actually copies.
      loadMarkdown(control).catch(() => {});
    };
    document.addEventListener('pointerover', prefetch);
    document.addEventListener('focusin', prefetch);
  }

  // Choosing a menu item or clicking anywhere outside closes the menu.
  document.addEventListener('click', (event) => {
    const item = event.target.closest('.page-actions__panel > *');
    if (item && item.matches('[data-page-actions-copy]')) {
      copy(item.closest('.page-actions'));
    }
    document.querySelectorAll('.page-actions__menu[open]').forEach((menu) => {
      if (item || !menu.contains(event.target)) closeMenu(menu);
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    document.querySelectorAll('.page-actions__menu[open]').forEach(closeMenu);
  });
})();
