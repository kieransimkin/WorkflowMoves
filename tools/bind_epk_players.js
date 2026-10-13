(function(){"use strict";
var configNode=document.querySelector("script[data-epk-player-bindings]");if(!configNode)return;
var config=JSON.parse(configNode.textContent),owners=new Map(),masterReference;
function videoId(frame){try{var url=new URL(frame.getAttribute("src"),document.baseURI);return /^www\.youtube(?:-nocookie)?\.com$/.test(url.hostname)&&url.pathname.indexOf("/embed/")===0?url.pathname.split("/").pop():null;}catch(error){return null;}}
function nativeUrl(player){return player.currentSrc||player.src||player.querySelector("source")?.src||"";}
function start(){var dm=window.DanceMoves;if(!dm?.registerYouTube||!dm?.registerPlayer)return;
var nativeMaster=Array.from(document.querySelectorAll("audio")).find(function(player){return config.master.urls.includes(nativeUrl(player));});
masterReference={id:config.master.id,duration:config.master.duration};if(nativeMaster)masterReference.element=nativeMaster;
function bind(element){if(owners.has(element))return;var id=element.tagName==="IFRAME"?videoId(element):nativeUrl(element);var record=config.players.find(function(item){return item.id===id;});if(!record)return;
var settings={master:masterReference,masterVerified:true,offset:record.offset,duration:record.duration,playerStart:record.playerStart||0};
try{var owner=record.kind==="youtube"?dm.registerYouTube(Object.assign(settings,{iframe:element})):dm.registerPlayer(Object.assign(settings,{player:element}));owners.set(element,owner);element.dataset.epkPlaybackBinding="bound";if(owner.ready)owner.ready.catch(function(error){element.dataset.epkPlaybackBinding="unavailable";element.dataset.epkPlaybackError=String(error.message||error);});}catch(error){element.dataset.epkPlaybackBinding="unavailable";element.dataset.epkPlaybackError=String(error.message||error);}}
var observer=typeof IntersectionObserver==="function"?new IntersectionObserver(function(entries){entries.forEach(function(entry){if(entry.isIntersecting){observer.unobserve(entry.target);bind(entry.target);}});},{rootMargin:"300px"}):null;
document.querySelectorAll("iframe,video").forEach(function(element){if(element.tagName==="IFRAME"&&observer){observer.observe(element);element.dataset.epkPlaybackBinding="deferred-until-visible";}else bind(element);});
document.querySelectorAll("audio").forEach(function(player){if(player===nativeMaster||!config.master.urls.includes(nativeUrl(player)))return;try{var owner=dm.registerPlayer({master:masterReference,player:player,masterVerified:true,offset:0,duration:config.master.duration});owners.set(player,owner);player.dataset.epkPlaybackBinding="bound";}catch(error){player.dataset.epkPlaybackBinding="unavailable";player.dataset.epkPlaybackError=String(error.message||error);}});
document.addEventListener("epk-cover-video-revealed",function(event){if(event.detail?.iframe)bind(event.detail.iframe);});
document.addEventListener("epk-cover-video-closing",function(event){var frame=event.detail?.iframe,owner=owners.get(frame);if(owner){owner.teardown();owners.delete(frame);}});
window.addEventListener("pagehide",function(){owners.forEach(function(owner,element){if(!element.isConnected){owner.teardown();owners.delete(element);}});});
document.documentElement.dataset.epkPlaybackBindings="registered";
}
if(window.DanceMoves?.ready)window.DanceMoves.ready.then(start);else document.addEventListener("dance-moves-ready",start,{once:true});
}());
