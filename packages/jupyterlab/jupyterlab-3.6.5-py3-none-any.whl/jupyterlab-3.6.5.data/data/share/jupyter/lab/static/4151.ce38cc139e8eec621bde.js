(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[4151],{64151:(e,s,t)=>{"use strict";t.r(s);t.d(s,{WebsocketProvider:()=>Q,messageAuth:()=>N,messageAwareness:()=>G,messageQueryAwareness:()=>D,messageSync:()=>q});var n=t(20073);var c=t(72382);var o=t(48307);var a=t(65679);var i=t(62794);const r=new Map;class d{constructor(e){this.room=e;this.onmessage=null;i.z((s=>s.key===e&&this.onmessage!==null&&this.onmessage({data:a.Gh(s.newValue||"")})))}postMessage(e){i.X.setItem(this.room,a.s3(a.eh(e)))}}const l=typeof BroadcastChannel==="undefined"?d:BroadcastChannel;const h=e=>c.Yu(r,e,(()=>{const s=o.Ue();const t=new l(e);t.onmessage=e=>s.forEach((s=>s(e.data,"broadcastchannel")));return{bc:t,subs:s}}));const u=(e,s)=>{h(e).subs.add(s);return s};const f=(e,s)=>{const t=h(e);const n=t.subs.delete(s);if(n&&t.subs.size===0){t.bc.close();r.delete(e)}return n};const w=(e,s,t=null)=>{const n=h(e);n.bc.postMessage(s);n.subs.forEach((e=>e(s,t)))};var m=t(20817);var b=t(88534);var p=t(64485);const y=0;const g=1;const _=2;const v=(e,s)=>{b.uE(e,y);const t=n.encodeStateVector(s);b.mP(e,t)};const E=(e,s,t)=>{b.uE(e,g);b.mP(e,n.encodeStateAsUpdate(s,t))};const k=(e,s,t)=>E(s,t,p.HN(e));const C=(e,s,t)=>{try{n.applyUpdate(s,p.HN(e),t)}catch(c){console.error("Caught error while handling a Yjs update",c)}};const I=(e,s)=>{b.uE(e,_);b.mP(e,s)};const U=C;const M=(e,s,t,n)=>{const c=p.yg(e);switch(c){case y:k(e,s,t);break;case g:C(e,t,n);break;case _:U(e,t,n);break;default:throw new Error("Unknown message type")}return c};const S=0;const H=(e,s)=>{encoding.writeVarUint(e,S);encoding.writeVarString(e,s)};const P=(e,s,t)=>{switch(p.yg(e)){case S:t(s,p.kf(e))}};var B=t(1057);var R=t(58290);var x=t(14247);var A=t(59735);const L=e=>{const s={};const t=e.split("?");const n=t[t.length-1].split("&");for(var c=0;c<n.length;c++){const e=n[c];if(e.length>0){const t=e.split("=");s[decodeURIComponent(t[0])]=decodeURIComponent(t[1]||"")}}return s};const V=e=>A.UI(e,((e,s)=>`${encodeURIComponent(s)}=${encodeURIComponent(e)}`)).join("&");var W=t(34155);const q=0;const D=3;const G=1;const N=2;const T=[];T[q]=(e,s,t,n,c)=>{b.uE(e,q);const o=M(s,e,t.doc,t);if(n&&o===g&&!t.synced){t.synced=true}};T[D]=(e,s,t,n,c)=>{b.uE(e,G);b.mP(e,B.xq(t.awareness,Array.from(t.awareness.getStates().keys())))};T[G]=(e,s,t,n,c)=>{B.oy(t.awareness,p.HN(s),t)};T[N]=(e,s,t,n,c)=>{P(s,t.doc,((e,s)=>$(t,s)))};const j=3e4;const $=(e,s)=>console.warn(`Permission denied to access ${e.url}.\n${s}`);const Z=(e,s,t)=>{const n=p.l1(s);const c=b.Mf();const o=p.yg(n);const a=e.messageHandlers[o];if(a){a(c,n,e,t,o)}else{console.error("Unable to compute message")}return c};const z=e=>{if(e.shouldConnect&&e.ws===null){const s=new e._WS(e.url);s.binaryType="arraybuffer";e.ws=s;e.wsconnecting=true;e.wsconnected=false;e.synced=false;s.onmessage=t=>{e.wsLastMessageReceived=m.ZG();const n=Z(e,new Uint8Array(t.data),true);if(b.kE(n)>1){s.send(b._f(n))}};s.onerror=s=>{e.emit("connection-error",[s,e])};s.onclose=s=>{e.emit("connection-close",[s,e]);e.ws=null;e.wsconnecting=false;if(e.wsconnected){e.wsconnected=false;e.synced=false;B.Ag(e.awareness,Array.from(e.awareness.getStates().keys()).filter((s=>s!==e.doc.clientID)),e);e.emit("status",[{status:"disconnected"}])}else{e.wsUnsuccessfulReconnects++}setTimeout(z,x.VV(x.sQ(2,e.wsUnsuccessfulReconnects)*100,e.maxBackoffTime),e)};s.onopen=()=>{e.wsLastMessageReceived=m.ZG();e.wsconnecting=false;e.wsconnected=true;e.wsUnsuccessfulReconnects=0;e.emit("status",[{status:"connected"}]);const t=b.Mf();b.uE(t,q);v(t,e.doc);s.send(b._f(t));if(e.awareness.getLocalState()!==null){const t=b.Mf();b.uE(t,G);b.mP(t,B.xq(e.awareness,[e.doc.clientID]));s.send(b._f(t))}};e.emit("status",[{status:"connecting"}])}};const O=(e,s)=>{const t=e.ws;if(e.wsconnected&&t&&t.readyState===t.OPEN){t.send(s)}if(e.bcconnected){w(e.bcChannel,s,e)}};class Q extends R.y{constructor(e,s,t,{connect:n=true,awareness:c=new B.GL(t),params:o={},WebSocketPolyfill:a=WebSocket,resyncInterval:i=-1,maxBackoffTime:r=2500,disableBc:d=false}={}){super();while(e[e.length-1]==="/"){e=e.slice(0,e.length-1)}const l=V(o);this.maxBackoffTime=r;this.bcChannel=e+"/"+s;this.url=e+"/"+s+(l.length===0?"":"?"+l);this.roomname=s;this.doc=t;this._WS=a;this.awareness=c;this.wsconnected=false;this.wsconnecting=false;this.bcconnected=false;this.disableBc=d;this.wsUnsuccessfulReconnects=0;this.messageHandlers=T.slice();this._synced=false;this.ws=null;this.wsLastMessageReceived=0;this.shouldConnect=n;this._resyncInterval=0;if(i>0){this._resyncInterval=setInterval((()=>{if(this.ws&&this.ws.readyState===WebSocket.OPEN){const e=b.Mf();b.uE(e,q);v(e,t);this.ws.send(b._f(e))}}),i)}this._bcSubscriber=(e,s)=>{if(s!==this){const s=Z(this,new Uint8Array(e),false);if(b.kE(s)>1){w(this.bcChannel,b._f(s),this)}}};this._updateHandler=(e,s)=>{if(s!==this){const s=b.Mf();b.uE(s,q);I(s,e);O(this,b._f(s))}};this.doc.on("update",this._updateHandler);this._awarenessUpdateHandler=({added:e,updated:s,removed:t},n)=>{const o=e.concat(s).concat(t);const a=b.Mf();b.uE(a,G);b.mP(a,B.xq(c,o));O(this,b._f(a))};this._unloadHandler=()=>{B.Ag(this.awareness,[t.clientID],"window unload")};if(typeof window!=="undefined"){window.addEventListener("unload",this._unloadHandler)}else if(typeof W!=="undefined"){W.on("exit",this._unloadHandler)}c.on("update",this._awarenessUpdateHandler);this._checkInterval=setInterval((()=>{if(this.wsconnected&&j<m.ZG()-this.wsLastMessageReceived){this.ws.close()}}),j/10);if(n){this.connect()}}get synced(){return this._synced}set synced(e){if(this._synced!==e){this._synced=e;this.emit("synced",[e]);this.emit("sync",[e])}}destroy(){if(this._resyncInterval!==0){clearInterval(this._resyncInterval)}clearInterval(this._checkInterval);this.disconnect();if(typeof window!=="undefined"){window.removeEventListener("unload",this._unloadHandler)}else if(typeof W!=="undefined"){W.off("exit",this._unloadHandler)}this.awareness.off("update",this._awarenessUpdateHandler);this.doc.off("update",this._updateHandler);super.destroy()}connectBc(){if(this.disableBc){return}if(!this.bcconnected){u(this.bcChannel,this._bcSubscriber);this.bcconnected=true}const e=b.Mf();b.uE(e,q);v(e,this.doc);w(this.bcChannel,b._f(e),this);const s=b.Mf();b.uE(s,q);E(s,this.doc);w(this.bcChannel,b._f(s),this);const t=b.Mf();b.uE(t,D);w(this.bcChannel,b._f(t),this);const n=b.Mf();b.uE(n,G);b.mP(n,B.xq(this.awareness,[this.doc.clientID]));w(this.bcChannel,b._f(n),this)}disconnectBc(){const e=b.Mf();b.uE(e,G);b.mP(e,B.xq(this.awareness,[this.doc.clientID],new Map));O(this,b._f(e));if(this.bcconnected){f(this.bcChannel,this._bcSubscriber);this.bcconnected=false}}disconnect(){this.shouldConnect=false;this.disconnectBc();if(this.ws!==null){this.ws.close()}}connect(){this.shouldConnect=true;if(!this.wsconnected&&this.ws===null){z(this);this.connectBc()}}}}}]);
//# sourceMappingURL=4151.ce38cc139e8eec621bde.js.map?v=ce38cc139e8eec621bde