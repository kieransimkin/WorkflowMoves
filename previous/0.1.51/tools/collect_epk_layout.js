(options = {}) => {
  const viewport = document.documentElement.clientWidth;
  const pixels = value => +((value || '0').match(/^-?\d*\.?\d+/)?.[0] || 0);
  const path = element => {
    if (element.id) return '#' + element.id;
    const classes = typeof element.className === 'string' ? element.className.trim().split(/\s+/).filter(Boolean).slice(0, 3) : [];
    return element.tagName.toLowerCase() + classes.map(value => '.' + value).join('');
  };
  const rect = element => {
    const value = element.getBoundingClientRect();
    return {left: value.left, right: value.right, top: value.top + scrollY, width: value.width, height: value.height};
  };
  const hidden = element => {
    for (let node = element; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (node.hasAttribute('hidden') || node.getAttribute('aria-hidden') === 'true' || style.display === 'none' || style.visibility === 'hidden') return true;
    }
    return false;
  };
  const scrolling = element => {
    for (let node = element.parentElement; node && node !== document.body; node = node.parentElement) {
      if (['auto', 'scroll'].includes(getComputedStyle(node).overflowX) && node.scrollWidth > node.clientWidth + 1) return node;
    }
    return null;
  };
  const item = element => ({selector: path(element), text: element.textContent.trim().slice(0, 100), rect: rect(element)});
  const content = [...document.querySelectorAll('h1,h2,h3,p,li,pre,table,audio,video,iframe,button,a,summary')]
    .filter(element => !hidden(element) && element.getBoundingClientRect().width > 0 && element.getBoundingClientRect().height > 0);
  const contentOverflow = [], textOverflow = [], clippedText = [], scrollingDescendants = [], offscreenFocusLinks = [];
  for (const element of content) {
    const bounds = element.getBoundingClientRect();
    const scrollParent = scrolling(element);
    const outside = bounds.left < -1 || bounds.right > viewport + 1;
    if (outside && element.tagName === 'A' && bounds.right < -1000 && element.getAttribute('href')?.startsWith('#')) {
      offscreenFocusLinks.push(item(element));
      continue;
    }
    if (outside && scrollParent) scrollingDescendants.push({...item(element), container: path(scrollParent)});
    else if (outside) contentOverflow.push(item(element));
    if (!/^H[1-3]$/.test(element.tagName) && element.tagName !== 'P') continue;
    const range = document.createRange();
    range.selectNodeContents(element);
    const textRects = [...range.getClientRects()].filter(value => value.width > 1);
    if (textRects.some(value => value.left < -1 || value.right > viewport + 1)) {
      if (scrollParent) scrollingDescendants.push({...item(element), container: path(scrollParent)});
      else textOverflow.push(item(element));
    }
    for (let node = element; node && node !== document.body; node = node.parentElement) {
      const style = getComputedStyle(node), bounds = node.getBoundingClientRect();
      if (['hidden', 'clip'].includes(style.overflowX) && textRects.some(value => value.left < bounds.left - 1 || value.right > bounds.right + 1)) {
        clippedText.push({...item(element), clipping_ancestor: path(node)});
        break;
      }
    }
  }
  const alignments = (options.alignments || []).map(spec => {
    const targets = [...document.querySelectorAll(spec.selector)], containers = [...document.querySelectorAll(spec.container)];
    const result = {selector: spec.selector, expected: spec.expected || 'center', tolerance: spec.tolerance ?? 2, matches: targets.length, container_matches: containers.length};
    if (targets.length === 1 && containers.length === 1) {
      result.target = rect(targets[0]);
      const box = rect(containers[0]), style = getComputedStyle(containers[0]);
      result.container = {left: box.left + pixels(style.borderLeftWidth) + pixels(style.paddingLeft),
        right: box.right - pixels(style.borderRightWidth) - pixels(style.paddingRight)};
    }
    return result;
  });
  return {schema: 'epk.layout-observation.v1', measured_width: innerWidth, measured_height: innerHeight,
    ready_state: document.readyState, client_width: viewport,
    scroll_width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
    overflow: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) > viewport + 1,
    content_overflow: contentOverflow, text_overflow: textOverflow, clipped_text: clippedText,
    scrolling_descendants: scrollingDescendants, offscreen_focus_links: offscreenFocusLinks, alignments,
    visible_images: [...document.images].filter(element => !hidden(element) && element.getBoundingClientRect().top < innerHeight && element.getBoundingClientRect().bottom > 0)
      .map(element => ({selector: path(element), complete: element.complete, natural_width: element.naturalWidth}))};
}
