(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[8843],{46820:(e,r,c)=>{"use strict";c.d(r,{Z:()=>s});var n=c(94015);var o=c.n(n);var a=c(23645);var t=c.n(a);var i=t()(o());i.push([e.id,".cm-s-abcdef.CodeMirror { background: #0f0f0f; color: #defdef; }\n.cm-s-abcdef div.CodeMirror-selected { background: #515151; }\n.cm-s-abcdef .CodeMirror-line::selection, .cm-s-abcdef .CodeMirror-line > span::selection, .cm-s-abcdef .CodeMirror-line > span > span::selection { background: rgba(56, 56, 56, 0.99); }\n.cm-s-abcdef .CodeMirror-line::-moz-selection, .cm-s-abcdef .CodeMirror-line > span::-moz-selection, .cm-s-abcdef .CodeMirror-line > span > span::-moz-selection { background: rgba(56, 56, 56, 0.99); }\n.cm-s-abcdef .CodeMirror-gutters { background: #555; border-right: 2px solid #314151; }\n.cm-s-abcdef .CodeMirror-guttermarker { color: #222; }\n.cm-s-abcdef .CodeMirror-guttermarker-subtle { color: azure; }\n.cm-s-abcdef .CodeMirror-linenumber { color: #FFFFFF; }\n.cm-s-abcdef .CodeMirror-cursor { border-left: 1px solid #00FF00; }\n\n.cm-s-abcdef span.cm-keyword { color: darkgoldenrod; font-weight: bold; }\n.cm-s-abcdef span.cm-atom { color: #77F; }\n.cm-s-abcdef span.cm-number { color: violet; }\n.cm-s-abcdef span.cm-def { color: #fffabc; }\n.cm-s-abcdef span.cm-variable { color: #abcdef; }\n.cm-s-abcdef span.cm-variable-2 { color: #cacbcc; }\n.cm-s-abcdef span.cm-variable-3, .cm-s-abcdef span.cm-type { color: #def; }\n.cm-s-abcdef span.cm-property { color: #fedcba; }\n.cm-s-abcdef span.cm-operator { color: #ff0; }\n.cm-s-abcdef span.cm-comment { color: #7a7b7c; font-style: italic;}\n.cm-s-abcdef span.cm-string { color: #2b4; }\n.cm-s-abcdef span.cm-meta { color: #C9F; }\n.cm-s-abcdef span.cm-qualifier { color: #FFF700; }\n.cm-s-abcdef span.cm-builtin { color: #30aabc; }\n.cm-s-abcdef span.cm-bracket { color: #8a8a8a; }\n.cm-s-abcdef span.cm-tag { color: #FFDD44; }\n.cm-s-abcdef span.cm-attribute { color: #DDFF00; }\n.cm-s-abcdef span.cm-error { color: #FF0000; }\n.cm-s-abcdef span.cm-header { color: aquamarine; font-weight: bold; }\n.cm-s-abcdef span.cm-link { color: blueviolet; }\n\n.cm-s-abcdef .CodeMirror-activeline-background { background: #314151; }\n","",{version:3,sources:["webpack://./node_modules/codemirror/theme/abcdef.css"],names:[],mappings:"AAAA,0BAA0B,mBAAmB,EAAE,cAAc,EAAE;AAC/D,uCAAuC,mBAAmB,EAAE;AAC5D,oJAAoJ,kCAAkC,EAAE;AACxL,mKAAmK,kCAAkC,EAAE;AACvM,mCAAmC,gBAAgB,EAAE,+BAA+B,EAAE;AACtF,wCAAwC,WAAW,EAAE;AACrD,+CAA+C,YAAY,EAAE;AAC7D,sCAAsC,cAAc,EAAE;AACtD,kCAAkC,8BAA8B,EAAE;;AAElE,+BAA+B,oBAAoB,EAAE,iBAAiB,EAAE;AACxE,4BAA4B,WAAW,EAAE;AACzC,8BAA8B,aAAa,EAAE;AAC7C,2BAA2B,cAAc,EAAE;AAC3C,gCAAgC,cAAc,EAAE;AAChD,kCAAkC,cAAc,EAAE;AAClD,6DAA6D,WAAW,EAAE;AAC1E,gCAAgC,cAAc,EAAE;AAChD,gCAAgC,WAAW,EAAE;AAC7C,+BAA+B,cAAc,EAAE,kBAAkB,CAAC;AAClE,8BAA8B,WAAW,EAAE;AAC3C,4BAA4B,WAAW,EAAE;AACzC,iCAAiC,cAAc,EAAE;AACjD,+BAA+B,cAAc,EAAE;AAC/C,+BAA+B,cAAc,EAAE;AAC/C,2BAA2B,cAAc,EAAE;AAC3C,iCAAiC,cAAc,EAAE;AACjD,6BAA6B,cAAc,EAAE;AAC7C,8BAA8B,iBAAiB,EAAE,iBAAiB,EAAE;AACpE,4BAA4B,iBAAiB,EAAE;;AAE/C,iDAAiD,mBAAmB,EAAE",sourcesContent:[".cm-s-abcdef.CodeMirror { background: #0f0f0f; color: #defdef; }\n.cm-s-abcdef div.CodeMirror-selected { background: #515151; }\n.cm-s-abcdef .CodeMirror-line::selection, .cm-s-abcdef .CodeMirror-line > span::selection, .cm-s-abcdef .CodeMirror-line > span > span::selection { background: rgba(56, 56, 56, 0.99); }\n.cm-s-abcdef .CodeMirror-line::-moz-selection, .cm-s-abcdef .CodeMirror-line > span::-moz-selection, .cm-s-abcdef .CodeMirror-line > span > span::-moz-selection { background: rgba(56, 56, 56, 0.99); }\n.cm-s-abcdef .CodeMirror-gutters { background: #555; border-right: 2px solid #314151; }\n.cm-s-abcdef .CodeMirror-guttermarker { color: #222; }\n.cm-s-abcdef .CodeMirror-guttermarker-subtle { color: azure; }\n.cm-s-abcdef .CodeMirror-linenumber { color: #FFFFFF; }\n.cm-s-abcdef .CodeMirror-cursor { border-left: 1px solid #00FF00; }\n\n.cm-s-abcdef span.cm-keyword { color: darkgoldenrod; font-weight: bold; }\n.cm-s-abcdef span.cm-atom { color: #77F; }\n.cm-s-abcdef span.cm-number { color: violet; }\n.cm-s-abcdef span.cm-def { color: #fffabc; }\n.cm-s-abcdef span.cm-variable { color: #abcdef; }\n.cm-s-abcdef span.cm-variable-2 { color: #cacbcc; }\n.cm-s-abcdef span.cm-variable-3, .cm-s-abcdef span.cm-type { color: #def; }\n.cm-s-abcdef span.cm-property { color: #fedcba; }\n.cm-s-abcdef span.cm-operator { color: #ff0; }\n.cm-s-abcdef span.cm-comment { color: #7a7b7c; font-style: italic;}\n.cm-s-abcdef span.cm-string { color: #2b4; }\n.cm-s-abcdef span.cm-meta { color: #C9F; }\n.cm-s-abcdef span.cm-qualifier { color: #FFF700; }\n.cm-s-abcdef span.cm-builtin { color: #30aabc; }\n.cm-s-abcdef span.cm-bracket { color: #8a8a8a; }\n.cm-s-abcdef span.cm-tag { color: #FFDD44; }\n.cm-s-abcdef span.cm-attribute { color: #DDFF00; }\n.cm-s-abcdef span.cm-error { color: #FF0000; }\n.cm-s-abcdef span.cm-header { color: aquamarine; font-weight: bold; }\n.cm-s-abcdef span.cm-link { color: blueviolet; }\n\n.cm-s-abcdef .CodeMirror-activeline-background { background: #314151; }\n"],sourceRoot:""}]);const s=i},23645:e=>{"use strict";e.exports=function(e){var r=[];r.toString=function r(){return this.map((function(r){var c=e(r);if(r[2]){return"@media ".concat(r[2]," {").concat(c,"}")}return c})).join("")};r.i=function(e,c,n){if(typeof e==="string"){e=[[null,e,""]]}var o={};if(n){for(var a=0;a<this.length;a++){var t=this[a][0];if(t!=null){o[t]=true}}}for(var i=0;i<e.length;i++){var s=[].concat(e[i]);if(n&&o[s[0]]){continue}if(c){if(!s[2]){s[2]=c}else{s[2]="".concat(c," and ").concat(s[2])}}r.push(s)}};return r}},94015:e=>{"use strict";function r(e,r){return t(e)||a(e,r)||n(e,r)||c()}function c(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function n(e,r){if(!e)return;if(typeof e==="string")return o(e,r);var c=Object.prototype.toString.call(e).slice(8,-1);if(c==="Object"&&e.constructor)c=e.constructor.name;if(c==="Map"||c==="Set")return Array.from(e);if(c==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(c))return o(e,r)}function o(e,r){if(r==null||r>e.length)r=e.length;for(var c=0,n=new Array(r);c<r;c++){n[c]=e[c]}return n}function a(e,r){var c=e&&(typeof Symbol!=="undefined"&&e[Symbol.iterator]||e["@@iterator"]);if(c==null)return;var n=[];var o=true;var a=false;var t,i;try{for(c=c.call(e);!(o=(t=c.next()).done);o=true){n.push(t.value);if(r&&n.length===r)break}}catch(s){a=true;i=s}finally{try{if(!o&&c["return"]!=null)c["return"]()}finally{if(a)throw i}}return n}function t(e){if(Array.isArray(e))return e}e.exports=function e(c){var n=r(c,4),o=n[1],a=n[3];if(typeof btoa==="function"){var t=btoa(unescape(encodeURIComponent(JSON.stringify(a))));var i="sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(t);var s="/*# ".concat(i," */");var A=a.sources.map((function(e){return"/*# sourceURL=".concat(a.sourceRoot||"").concat(e," */")}));return[o].concat(A).concat([s]).join("\n")}return[o].join("\n")}},18843:(e,r,c)=>{"use strict";c.r(r);c.d(r,{default:()=>s});var n=c(93379);var o=c.n(n);var a=c(46820);var t={};t.insert="head";t.singleton=false;var i=o()(a.Z,t);const s=a.Z.locals||{}},93379:(e,r,c)=>{"use strict";var n=function e(){var r;return function e(){if(typeof r==="undefined"){r=Boolean(window&&document&&document.all&&!window.atob)}return r}}();var o=function e(){var r={};return function e(c){if(typeof r[c]==="undefined"){var n=document.querySelector(c);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement){try{n=n.contentDocument.head}catch(o){n=null}}r[c]=n}return r[c]}}();var a=[];function t(e){var r=-1;for(var c=0;c<a.length;c++){if(a[c].identifier===e){r=c;break}}return r}function i(e,r){var c={};var n=[];for(var o=0;o<e.length;o++){var i=e[o];var s=r.base?i[0]+r.base:i[0];var A=c[s]||0;var f="".concat(s," ").concat(A);c[s]=A+1;var d=t(f);var l={css:i[1],media:i[2],sourceMap:i[3]};if(d!==-1){a[d].references++;a[d].updater(l)}else{a.push({identifier:f,updater:b(l,r),references:1})}n.push(f)}return n}function s(e){var r=document.createElement("style");var n=e.attributes||{};if(typeof n.nonce==="undefined"){var a=true?c.nc:0;if(a){n.nonce=a}}Object.keys(n).forEach((function(e){r.setAttribute(e,n[e])}));if(typeof e.insert==="function"){e.insert(r)}else{var t=o(e.insert||"head");if(!t){throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.")}t.appendChild(r)}return r}function A(e){if(e.parentNode===null){return false}e.parentNode.removeChild(e)}var f=function e(){var r=[];return function e(c,n){r[c]=n;return r.filter(Boolean).join("\n")}}();function d(e,r,c,n){var o=c?"":n.media?"@media ".concat(n.media," {").concat(n.css,"}"):n.css;if(e.styleSheet){e.styleSheet.cssText=f(r,o)}else{var a=document.createTextNode(o);var t=e.childNodes;if(t[r]){e.removeChild(t[r])}if(t.length){e.insertBefore(a,t[r])}else{e.appendChild(a)}}}function l(e,r,c){var n=c.css;var o=c.media;var a=c.sourceMap;if(o){e.setAttribute("media",o)}else{e.removeAttribute("media")}if(a&&typeof btoa!=="undefined"){n+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(a))))," */")}if(e.styleSheet){e.styleSheet.cssText=n}else{while(e.firstChild){e.removeChild(e.firstChild)}e.appendChild(document.createTextNode(n))}}var m=null;var u=0;function b(e,r){var c;var n;var o;if(r.singleton){var a=u++;c=m||(m=s(r));n=d.bind(null,c,a,false);o=d.bind(null,c,a,true)}else{c=s(r);n=l.bind(null,c,r);o=function e(){A(c)}}n(e);return function r(c){if(c){if(c.css===e.css&&c.media===e.media&&c.sourceMap===e.sourceMap){return}n(e=c)}else{o()}}}e.exports=function(e,r){r=r||{};if(!r.singleton&&typeof r.singleton!=="boolean"){r.singleton=n()}e=e||[];var c=i(e,r);return function e(n){n=n||[];if(Object.prototype.toString.call(n)!=="[object Array]"){return}for(var o=0;o<c.length;o++){var s=c[o];var A=t(s);a[A].references--}var f=i(n,r);for(var d=0;d<c.length;d++){var l=c[d];var m=t(l);if(a[m].references===0){a[m].updater();a.splice(m,1)}}c=f}}}}]);
//# sourceMappingURL=8843.35ec0f0b1f61c25e0401.js.map?v=35ec0f0b1f61c25e0401