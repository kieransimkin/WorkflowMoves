(function(){
  "use strict";
  if(document.documentElement.dataset.epkCoverOwner)return;
  document.documentElement.dataset.epkCoverOwner="2";
  function mountWidescreenHeroes(){
    var effects=window.DanceMovesEffects;
    if(!effects?.layoutReveal)return;
    document.querySelectorAll("[data-epk-widescreen-hero]").forEach(function(root){
      effects.layoutReveal({
        id:"epk-widescreen-"+root.dataset.epkCoverPlayer,
        root:root,
        openEvent:"epk-cover-video-revealed",
        closeEvent:"epk-cover-video-closing",
        initiallyExpanded:root.classList.contains("is-revealed"),
        durationMilliseconds:480
      });
    });
  }
  if(window.DanceMovesEffects)mountWidescreenHeroes();
  else document.addEventListener("dance-moves-effects-ready",mountWidescreenHeroes,{once:true});
  function close(root,focus){
    (root._epkStableParents||[]).forEach(function(parent){parent.classList.remove("epk-video-stable");});
    root._epkStableParents=[];
    var slot=root.querySelector("[data-epk-video-slot]"),play=root.querySelector("[data-epk-video-play]"),button=root.querySelector("[data-epk-video-close]");
    var frame=slot.querySelector("iframe");
    if(frame){root.dispatchEvent(new CustomEvent("epk-cover-video-closing",{bubbles:true,detail:{iframe:frame}}));frame.remove();}
    root.classList.remove("is-revealed");slot.hidden=true;play.hidden=false;
    if(button)button.hidden=true;
    if(focus)play.focus();
  }
  document.addEventListener("click",function(event){
    if(event.defaultPrevented||event.button!==0||event.ctrlKey||event.metaKey||event.altKey||event.shiftKey)return;
    if(!event.target.closest)return;
    var button=event.target.closest("[data-epk-video-play],[data-epk-video-close]");
    var root=event.target.closest("[data-epk-cover-player]");
    if(!root)return;
    if(!button){
      if(root.classList.contains("is-revealed"))return;
      var interactive=event.target.closest("a,button,input,select,textarea,[role=button]");
      if(interactive){if(root.contains(interactive))return;}
      button=root.querySelector("[data-epk-video-play]");
    }
    if(!button)return;
    event.preventDefault();event.stopPropagation();
    if(button.hasAttribute("data-epk-video-close")){close(root,true);return;}
    var slot=root.querySelector("[data-epk-video-slot]");
    if(slot.querySelector("iframe"))return;
    var template=root.querySelector("template[data-epk-video-template]");
    if(!template)return;
    var original=template.content.querySelector("iframe");
    if(!original)return;
    var frame=original.cloneNode(true),url=new URL(frame.getAttribute("src"));
    if(url.protocol!=="https:")return;
    if(!/^www\.youtube(?:-nocookie)?\.com$/.test(url.hostname))return;
    url.searchParams.set("autoplay","1");url.searchParams.set("playsinline","1");url.searchParams.set("enablejsapi","1");url.searchParams.set("origin",location.origin);
    frame.src=url.href;frame.loading="eager";
    var allow=frame.getAttribute("allow")||"";
    if(!/(^|;)\s*autoplay(?:\s|;|$)/.test(allow))frame.setAttribute("allow",allow+(allow?"; ":"")+"autoplay");
    root._epkStableParents=[];
    for(var parent=root.parentElement;parent!==document.body;parent=parent.parentElement){
      if(!parent)break;
      if(getComputedStyle(parent).transform!=="none"){parent.classList.add("epk-video-stable");root._epkStableParents.push(parent);}
    }
    slot.appendChild(frame);slot.hidden=false;root.classList.add("is-revealed");button.hidden=true;
    var closeButton=root.querySelector("[data-epk-video-close]");
    if(closeButton)closeButton.hidden=false;
    root.dispatchEvent(new CustomEvent("epk-cover-video-revealed",{bubbles:true,detail:{iframe:frame}}));
    frame.focus();
  });
  window.addEventListener("pagehide",function(){document.querySelectorAll("[data-epk-cover-player].is-revealed").forEach(function(root){close(root,false);});});
}());
