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
    return {left: value.left, right: value.right, top: value.top + scrollY, bottom: value.bottom + scrollY,
      width: value.width, height: value.height};
  };
  const hidden = element => {
    for (let node = element; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (node.hidden || node.inert || node.getAttribute('aria-hidden') === 'true' ||
          style.display === 'none' || ['hidden', 'collapse'].includes(style.visibility) || Number(style.opacity) === 0) return true;
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
  const panelPairs = (options.panel_pairs || []).map(({first, second}) => {
    const firstNodes = typeof first === 'string' && first.trim() ? document.querySelectorAll(first) : [];
    const secondNodes = typeof second === 'string' && second.trim() ? document.querySelectorAll(second) : [];
    const result = {first, second, first_matches: firstNodes.length, second_matches: secondNodes.length};
    if (firstNodes.length === 1 && secondNodes.length === 1) {
      const a = firstNodes[0], b = secondNodes[0];
      result.independent = !a.contains(b) && !b.contains(a);
      if (!hidden(a)) result.first_rect = rect(a);
      if (!hidden(b)) result.second_rect = rect(b);
    }
    return result;
  });
  const coverIds = [...document.querySelectorAll('[data-epk-cover-player]')]
    .map(node => node.getAttribute('data-epk-cover-player')).filter(id => /^[\w-]{11}$/.test(id));
  const unique = (root, selector) => {
    if (!selector) return null;
    const matches = root.querySelectorAll(selector);
    return matches.length === 1 ? matches[0] : null;
  };
  const visibleRect = (node, inspectText = false) => {
    if (!node || hidden(node)) return null;
    const box = node.getBoundingClientRect();
    if (!box.width || !box.height) return null;
    const boxes = [box];
    if (inspectText) {
      const range = document.createRange();
      range.selectNodeContents(node);
      boxes.push(...[...range.getClientRects()].filter(rect => rect.width > 1));
    }
    if (boxes.some(rect => rect.left < -1 || rect.right > viewport + 1)) return null;
    for (let parent = node; parent && parent !== document.body; parent = parent.parentElement) {
      const style = getComputedStyle(parent);
      const clipping = parent.getBoundingClientRect();
      if (['hidden', 'clip'].includes(style.overflowX) &&
          boxes.some(rect => rect.left < clipping.left - 1 || rect.right > clipping.right + 1)) return null;
      if (['hidden', 'clip'].includes(style.overflowY) &&
          boxes.some(rect => rect.top < clipping.top - 1 || rect.bottom > clipping.bottom + 1)) return null;
    }
    return rect(node);
  };
  const youtubeStates = (options.youtube_reveal || []).map(spec => {
    const player = unique(document, spec.player);
    const frames = player?.querySelectorAll(spec.frame || '[data-epk-video-slot] iframe');
    const frame = frames?.length === 1 ? frames[0] : null;
    const opener = player && unique(player, spec.opener || '[data-epk-video-play]');
    const poster = player && unique(player, spec.poster || 'img');
    const close = player && unique(player, spec.close || '[data-epk-video-close]');
    const following = unique(document, spec.following);
    const copy = Object.fromEntries((spec.copy || []).map(selector => {
      const target = unique(document, selector);
      return [selector, visibleRect(target, true)];
    }));
    let videoId = player?.getAttribute('data-epk-cover-player') || spec.video_id || null;
    if (frame) {
      const url = new URL(frame.getAttribute('src') || '', location.href);
      videoId = /^(www\.)?youtube(?:-nocookie)?\.com$/.test(url.hostname)
        ? url.pathname.match(/^\/embed\/([\w-]{11})$/)?.[1] : null;
    }
    return {player: spec.player, video_id: videoId, viewport_width: innerWidth,
      horizontal_overflow: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) > viewport + 1,
      frame_count: frames?.length ?? null, poster: visibleRect(poster), opener: visibleRect(opener),
      frame: visibleRect(frame), close: visibleRect(close), focus_on_opener: !!opener && opener === document.activeElement,
      copy, following_selector: spec.following, following: visibleRect(following)};
  });
  return {schema: 'epk.layout-observation.v2', measured_width: innerWidth, measured_height: innerHeight,
    ready_state: document.readyState, client_width: viewport,
    scroll_width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
    overflow: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) > viewport + 1,
    content_overflow: contentOverflow, text_overflow: textOverflow, clipped_text: clippedText,
    scrolling_descendants: scrollingDescendants, offscreen_focus_links: offscreenFocusLinks, alignments,
    panel_pairs: panelPairs, youtube_cover_ids: coverIds, youtube_reveal_states: youtubeStates,
    visible_images: [...document.images].filter(element => !hidden(element) && element.getBoundingClientRect().top < innerHeight && element.getBoundingClientRect().bottom > 0)
      .map(element => ({selector: path(element), complete: element.complete, natural_width: element.naturalWidth}))};
}
