/*! For license information please see 7294.f71c2889fedcd71bd1ee.js.LICENSE.txt */
(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[7294],{27418:e=>{"use strict";var t=Object.getOwnPropertySymbols;var r=Object.prototype.hasOwnProperty;var n=Object.prototype.propertyIsEnumerable;function o(e){if(e===null||e===undefined){throw new TypeError("Object.assign cannot be called with null or undefined")}return Object(e)}function u(){try{if(!Object.assign){return false}var e=new String("abc");e[5]="de";if(Object.getOwnPropertyNames(e)[0]==="5"){return false}var t={};for(var r=0;r<10;r++){t["_"+String.fromCharCode(r)]=r}var n=Object.getOwnPropertyNames(t).map((function(e){return t[e]}));if(n.join("")!=="0123456789"){return false}var o={};"abcdefghijklmnopqrst".split("").forEach((function(e){o[e]=e}));if(Object.keys(Object.assign({},o)).join("")!=="abcdefghijklmnopqrst"){return false}return true}catch(u){return false}}e.exports=u()?Object.assign:function(e,u){var a;var i=o(e);var f;for(var c=1;c<arguments.length;c++){a=Object(arguments[c]);for(var l in a){if(r.call(a,l)){i[l]=a[l]}}if(t){f=t(a);for(var s=0;s<f.length;s++){if(n.call(a,f[s])){i[f[s]]=a[f[s]]}}}}return i}},72408:(e,t,r)=>{"use strict";var n=r(27418),o=60103,u=60106;t.Fragment=60107;t.StrictMode=60108;t.Profiler=60114;var a=60109,i=60110,f=60112;t.Suspense=60113;var c=60115,l=60116;if("function"===typeof Symbol&&Symbol.for){var s=Symbol.for;o=s("react.element");u=s("react.portal");t.Fragment=s("react.fragment");t.StrictMode=s("react.strict_mode");t.Profiler=s("react.profiler");a=s("react.provider");i=s("react.context");f=s("react.forward_ref");t.Suspense=s("react.suspense");c=s("react.memo");l=s("react.lazy")}var p="function"===typeof Symbol&&Symbol.iterator;function y(e){if(null===e||"object"!==typeof e)return null;e=p&&e[p]||e["@@iterator"];return"function"===typeof e?e:null}function d(e){for(var t="https://reactjs.org/docs/error-decoder.html?invariant="+e,r=1;r<arguments.length;r++)t+="&args[]="+encodeURIComponent(arguments[r]);return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}var v={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},h={};function _(e,t,r){this.props=e;this.context=t;this.refs=h;this.updater=r||v}_.prototype.isReactComponent={};_.prototype.setState=function(e,t){if("object"!==typeof e&&"function"!==typeof e&&null!=e)throw Error(d(85));this.updater.enqueueSetState(this,e,t,"setState")};_.prototype.forceUpdate=function(e){this.updater.enqueueForceUpdate(this,e,"forceUpdate")};function b(){}b.prototype=_.prototype;function m(e,t,r){this.props=e;this.context=t;this.refs=h;this.updater=r||v}var g=m.prototype=new b;g.constructor=m;n(g,_.prototype);g.isPureReactComponent=!0;var w={current:null},j=Object.prototype.hasOwnProperty,k={key:!0,ref:!0,__self:!0,__source:!0};function O(e,t,r){var n,u={},a=null,i=null;if(null!=t)for(n in void 0!==t.ref&&(i=t.ref),void 0!==t.key&&(a=""+t.key),t)j.call(t,n)&&!k.hasOwnProperty(n)&&(u[n]=t[n]);var f=arguments.length-2;if(1===f)u.children=r;else if(1<f){for(var c=Array(f),l=0;l<f;l++)c[l]=arguments[l+2];u.children=c}if(e&&e.defaultProps)for(n in f=e.defaultProps,f)void 0===u[n]&&(u[n]=f[n]);return{$$typeof:o,type:e,key:a,ref:i,props:u,_owner:w.current}}function S(e,t){return{$$typeof:o,type:e.type,key:t,ref:e.ref,props:e.props,_owner:e._owner}}function C(e){return"object"===typeof e&&null!==e&&e.$$typeof===o}function $(e){var t={"=":"=0",":":"=2"};return"$"+e.replace(/[=:]/g,(function(e){return t[e]}))}var E=/\/+/g;function R(e,t){return"object"===typeof e&&null!==e&&null!=e.key?$(""+e.key):t.toString(36)}function P(e,t,r,n,a){var i=typeof e;if("undefined"===i||"boolean"===i)e=null;var f=!1;if(null===e)f=!0;else switch(i){case"string":case"number":f=!0;break;case"object":switch(e.$$typeof){case o:case u:f=!0}}if(f)return f=e,a=a(f),e=""===n?"."+R(f,0):n,Array.isArray(a)?(r="",null!=e&&(r=e.replace(E,"$&/")+"/"),P(a,t,r,"",(function(e){return e}))):null!=a&&(C(a)&&(a=S(a,r+(!a.key||f&&f.key===a.key?"":(""+a.key).replace(E,"$&/")+"/")+e)),t.push(a)),1;f=0;n=""===n?".":n+":";if(Array.isArray(e))for(var c=0;c<e.length;c++){i=e[c];var l=n+R(i,c);f+=P(i,t,r,l,a)}else if(l=y(e),"function"===typeof l)for(e=l.call(e),c=0;!(i=e.next()).done;)i=i.value,l=n+R(i,c++),f+=P(i,t,r,l,a);else if("object"===i)throw t=""+e,Error(d(31,"[object Object]"===t?"object with keys {"+Object.keys(e).join(", ")+"}":t));return f}function x(e,t,r){if(null==e)return e;var n=[],o=0;P(e,n,"","",(function(e){return t.call(r,e,o++)}));return n}function A(e){if(-1===e._status){var t=e._result;t=t();e._status=0;e._result=t;t.then((function(t){0===e._status&&(t=t.default,e._status=1,e._result=t)}),(function(t){0===e._status&&(e._status=2,e._result=t)}))}if(1===e._status)return e._result;throw e._result}var I={current:null};function q(){var e=I.current;if(null===e)throw Error(d(321));return e}var U={ReactCurrentDispatcher:I,ReactCurrentBatchConfig:{transition:0},ReactCurrentOwner:w,IsSomeRendererActing:{current:!1},assign:n};t.Children={map:x,forEach:function(e,t,r){x(e,(function(){t.apply(this,arguments)}),r)},count:function(e){var t=0;x(e,(function(){t++}));return t},toArray:function(e){return x(e,(function(e){return e}))||[]},only:function(e){if(!C(e))throw Error(d(143));return e}};t.Component=_;t.PureComponent=m;t.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED=U;t.cloneElement=function(e,t,r){if(null===e||void 0===e)throw Error(d(267,e));var u=n({},e.props),a=e.key,i=e.ref,f=e._owner;if(null!=t){void 0!==t.ref&&(i=t.ref,f=w.current);void 0!==t.key&&(a=""+t.key);if(e.type&&e.type.defaultProps)var c=e.type.defaultProps;for(l in t)j.call(t,l)&&!k.hasOwnProperty(l)&&(u[l]=void 0===t[l]&&void 0!==c?c[l]:t[l])}var l=arguments.length-2;if(1===l)u.children=r;else if(1<l){c=Array(l);for(var s=0;s<l;s++)c[s]=arguments[s+2];u.children=c}return{$$typeof:o,type:e.type,key:a,ref:i,props:u,_owner:f}};t.createContext=function(e,t){void 0===t&&(t=null);e={$$typeof:i,_calculateChangedBits:t,_currentValue:e,_currentValue2:e,_threadCount:0,Provider:null,Consumer:null};e.Provider={$$typeof:a,_context:e};return e.Consumer=e};t.createElement=O;t.createFactory=function(e){var t=O.bind(null,e);t.type=e;return t};t.createRef=function(){return{current:null}};t.forwardRef=function(e){return{$$typeof:f,render:e}};t.isValidElement=C;t.lazy=function(e){return{$$typeof:l,_payload:{_status:-1,_result:e},_init:A}};t.memo=function(e,t){return{$$typeof:c,type:e,compare:void 0===t?null:t}};t.useCallback=function(e,t){return q().useCallback(e,t)};t.useContext=function(e,t){return q().useContext(e,t)};t.useDebugValue=function(){};t.useEffect=function(e,t){return q().useEffect(e,t)};t.useImperativeHandle=function(e,t,r){return q().useImperativeHandle(e,t,r)};t.useLayoutEffect=function(e,t){return q().useLayoutEffect(e,t)};t.useMemo=function(e,t){return q().useMemo(e,t)};t.useReducer=function(e,t,r){return q().useReducer(e,t,r)};t.useRef=function(e){return q().useRef(e)};t.useState=function(e){return q().useState(e)};t.version="17.0.2"},67294:(e,t,r)=>{"use strict";if(true){e.exports=r(72408)}else{}}}]);
//# sourceMappingURL=7294.f71c2889fedcd71bd1ee.js.map?v=f71c2889fedcd71bd1ee