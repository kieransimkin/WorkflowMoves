(function(){
  'use strict';
  function mount(){
    if(window.EpkNativeVideoSurface){if(!window.EpkNativeVideoSurface.snapshot().disposed)return;}
    var config=document.querySelector('script[data-epk-native-surface]');
    if(!config)return;
    var sources=JSON.parse(config.textContent).sources;
    var videos=Array.from(document.querySelectorAll('video[controls]')).filter(function(video){return sources.indexOf(video.getAttribute('src')||video.querySelector('source')?.getAttribute('src'))!==-1;});
    var removers=[],disposed=false,activations=0,rejected=0;
    videos.forEach(function(video){
      var touch=null,lastTouch=null;
      function toggle(event){
        event.preventDefault();activations++;
        if(video.paused||video.ended){
          delete video.dataset.epkSurfacePlayError;
          var result=video.play();
          if(result){if(typeof result.catch==='function')result.catch(function(error){rejected++;video.dataset.epkSurfacePlayError=String(error.name||'PlaybackError');});}
        }else video.pause();
      }
      function activate(event){
        if(event.target!==video||event.defaultPrevented||event.button!==0||event.detail>1||event.ctrlKey||event.metaKey||event.altKey||event.shiftKey)return;
        if(event.pointerType==='touch')return;
        if(event.sourceCapabilities){if(event.sourceCapabilities.firesTouchEvents)return;}
        if(lastTouch){if(750>event.timeStamp-lastTouch.time){if(12>Math.hypot(event.clientX-lastTouch.x,event.clientY-lastTouch.y))return;}}
        toggle(event);
      }
      function down(event){
        if(event.pointerType!=='touch')return;
        if(event.target!==video||event.isPrimary===false||event.defaultPrevented){touch=null;return;}
        touch={id:event.pointerId,x:event.clientX,y:event.clientY,time:event.timeStamp};
      }
      function move(event){if(touch){if(event.pointerId===touch.id){if(Math.hypot(event.clientX-touch.x,event.clientY-touch.y)>8)touch=null;}}}
      function cancel(){touch=null;}
      function up(event){
        var start=touch;touch=null;
        if(!start||event.pointerId!==start.id||event.target!==video||event.defaultPrevented||event.timeStamp-start.time>650||Math.hypot(event.clientX-start.x,event.clientY-start.y)>8)return;
        lastTouch={x:event.clientX,y:event.clientY,time:event.timeStamp};toggle(event);
      }
      video.addEventListener('click',activate);video.addEventListener('pointerdown',down);video.addEventListener('pointermove',move);video.addEventListener('pointerup',up);video.addEventListener('pointercancel',cancel);
      removers.push(function(){video.removeEventListener('click',activate);video.removeEventListener('pointerdown',down);video.removeEventListener('pointermove',move);video.removeEventListener('pointerup',up);video.removeEventListener('pointercancel',cancel);});
    });
    function teardown(){if(disposed)return;disposed=true;removers.splice(0).forEach(function(remove){remove();});}
    window.EpkNativeVideoSurface=Object.freeze({teardown:teardown,snapshot:function(){return {disposed:disposed,videos:videos.length,activations:activations,rejected:rejected};}});
  }
  window.addEventListener('pagehide',function(){if(window.EpkNativeVideoSurface)window.EpkNativeVideoSurface.teardown();});
  window.addEventListener('pageshow',mount);mount();
}());
