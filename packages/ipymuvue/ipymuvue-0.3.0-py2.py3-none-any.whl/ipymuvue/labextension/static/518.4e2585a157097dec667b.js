"use strict";(self.webpackChunkipymuvue=self.webpackChunkipymuvue||[]).push([[518],{518:(t,e,r)=>{r.r(e),r.d(e,{VueWidgetModel:()=>c,VueWidgetView:()=>mr});var n=r(465),o=r(297),i=r(549);t=r.hmd(t);const a=r(565).i8;class c extends n.DOMWidgetModel{defaults(){return{...super.defaults(),_model_name:"VueWidgetModel",_view_name:"VueWidgetView",_model_module:"ipymuvue",_view_module:"ipymuvue",_model_module_version:`~${a}`,_view_module_version:`~${a}`,_VueWidget__type:"VueWidget",_VueWidget__template:"<div>…</div>",_VueWidget__methods:[],_VueWidget__components:{},_VueWidget__assets:{},_VueWidget__children:{}}}get reactiveState(){const t=["layout",...Object.keys(this.defaults())];return Object.fromEntries(this.keys().filter((e=>!t.includes(e))).map((t=>[t,this.get(t)])))}get methods(){var t=this;const e=this.get("_VueWidget__methods");return Object.fromEntries(e.map((e=>[e,function(){for(var r=arguments.length,n=new Array(r),o=0;o<r;o++)n[o]=arguments[o];return t.callback(e,n||[])}])))}callback(t,e){this.send({method:t,args:e},this.callbacks())}}class u{constructor(t){this.FS=t}async provision(t,e){const r=this.FS.analyzePath(t,!0),n={replaced:!1,abspath:r.path};if(r.exists){if(u.equal(this.FS.readFile(t),e.buffer))return n;n.replaced=!0}return this.FS.writeFile(t,new Uint8Array(e.buffer),{encoding:"binary"}),n}static equal(t,e){if(t.byteLength!==e.byteLength)return!1;const r=new Uint8Array(t),n=new Uint8Array(e);return r.every(((t,e)=>t===n[e]))}}class s{constructor(t,e,r){this.name=t,this.url=e,this.integrity=r}get object(){return(async()=>{const t=window;return"function"==typeof t.requirejs?await this.loadRequireJS(t.requirejs):await this.loadBrowser()})()}async loadRequireJS(t){if(!this.url.endsWith(".js"))throw Error("url must end with .js to be loaded through RequireJS");return t.config({paths:{[this.name]:this.url.substring(0,this.url.length-3)},onNodeCreated:function(t,e,r,n){r===this.name&&(this.integrity&&(t.integrity=this.integrity),t.crossOrigin="anonymous")}}),await new Promise(((e,r)=>{t([this.name],(function(t){e(t)}),(function(t){r(t)}))}))}async loadBrowser(){const t=document.createElement("script"),e=new Promise(((e,r)=>{t.addEventListener("load",(()=>e())),t.addEventListener("error",(()=>r()))}));return t.async=!0,t.src=this.url,this.integrity&&(t.integrity=this.integrity),t.crossOrigin="anonymous",document.head.appendChild(t),await e,window}}var l=Object.freeze({__proto__:null,Vue:o,withArity:function(t,e){if(2===e){function r(e,r){return t(e,r)}return r}throw Error("not implemented")},getValue:function(t){return t.value}});const f="https://cdn.jsdelivr.net/pyodide/v0.21.0a3/full";class p{static instance=null;static provisioned=new Set;async provisionAssets(t){const e=await this.pyodide,r=await this.modules,n=new u(e.FS);let o=!1;for(const[e,r]of Object.entries(t)){const t=await n.provision(e,r);p.provisioned.add(t.abspath),t.replaced&&(console.info(`replaced modified asset ${e}`),console.warn(`will reload all modules because ${e} changed`),o=!0)}if(o)for(const[t,n]of Object.values(r))p.provisioned.has(n.__file__)&&(console.debug(`resetting ${n}`),e.pyimport("sys").modules.delete(t))}get modules(){return(async()=>{const t={},e=(await this.pyodide).pyimport("sys");for(const[r,n]of e.modules.items())"__file__"in n&&(t[n.__file__]=[r,n]);return t})()}get pyodide(){return null==p.instance&&(p.instance=(async()=>{const t=(await new s("pyodide",`${f}/pyodide.js`).object).loadPyodide,e=await t({indexURL:`${f}/`});return e.registerJsModule("ipymuvue_utils",l),e})()),p.instance}}var d,h,y=Function.prototype.toString,b="object"==typeof Reflect&&null!==Reflect&&Reflect.apply;if("function"==typeof b&&"function"==typeof Object.defineProperty)try{d=Object.defineProperty({},"length",{get:function(){throw h}}),h={},b((function(){throw 42}),null,d)}catch(t){t!==h&&(b=null)}else b=null;var v=/^\s*class\b/,_=function(t){try{var e=y.call(t);return v.test(e)}catch(t){return!1}},g=Object.prototype.toString,j="function"==typeof Symbol&&!!Symbol.toStringTag,m="object"==typeof document&&void 0===document.all&&void 0!==document.all?document.all:{},w=b?function(t){if(t===m)return!0;if(!t)return!1;if("function"!=typeof t&&"object"!=typeof t)return!1;if("function"==typeof t&&!t.prototype)return!0;try{b(t,null,d)}catch(t){if(t!==h)return!1}return!_(t)}:function(t){if(t===m)return!0;if(!t)return!1;if("function"!=typeof t&&"object"!=typeof t)return!1;if("function"==typeof t&&!t.prototype)return!0;if(j)return function(t){try{return!_(t)&&(y.call(t),!0)}catch(t){return!1}}(t);if(_(t))return!1;var e=g.call(t);return"[object Function]"===e||"[object GeneratorFunction]"===e};class O{constructor(t){this.assets=t||{},this.pyodide=new p}compile(t){return(0,o.defineAsyncComponent)((()=>this.compileAsync(t)))}async compileAsync(t){if("string"==typeof t){const e={moduleCache:{vue:o},getFile:async t=>{const e=t.toString();return{getContentData:async t=>{const r=w(this.assets)?this.assets(e):this.assets[e];if(r){if(!(r.buffer instanceof ArrayBuffer))throw Error(`asset of incorrect type: ${r}`);return t?r.buffer:(new TextDecoder).decode(r.buffer)}if(e.startsWith("https://")){const t=await fetch(e);return await t.text()}throw Error(`cannot resolve ${e} from provided assets`)},type:e.includes(".")?"."+e.split(".").pop():""}},addStyle(t){const e=Object.assign(document.createElement("style"),{textContent:t});document.head.appendChild(e)},handleModule:async(t,e,r)=>{const n=r.toString();if(".py"===t){const t=await e(!0);if("string"==typeof t)throw Error("getContentData(true) should have returned binary data but found a literal string instead");if(await this.pyodide.provisionAssets({[n]:new DataView(t)}),this.assets instanceof Function||await this.pyodide.provisionAssets(this.assets),(await this.pyodide.pyodide).registerJsModule("ipymuvue_vue_component_compiler",{VueComponentCompiler:O}),!n.endsWith(".py"))throw Error("Python file must end in .py");const r=n.replace(/\//g,".").substring(0,n.length-3);return(await this.pyodide.pyodide).pyimport(r)}},getResource(t,e){throw Error("not implemented")},pathResolve(t){throw Error("not implemented")}};delete e.getResource,delete e.pathResolve;const r=await(0,i.loadModule)(t,e);return t.toLowerCase().endsWith(".py")?r.component:r}{const e=t;return(async()=>Object.fromEntries(await Promise.all(Object.entries(e).map((async t=>{let[e,r]=t;return[e,await this.compileAsync(r)]})))))()}}}function A(t,e){return t===e||t!=t&&e!=e}function S(t,e){for(var r=t.length;r--;)if(A(t[r][0],e))return r;return-1}var x=Array.prototype.splice;function E(t){var e=-1,r=null==t?0:t.length;for(this.clear();++e<r;){var n=t[e];this.set(n[0],n[1])}}E.prototype.clear=function(){this.__data__=[],this.size=0},E.prototype.delete=function(t){var e=this.__data__,r=S(e,t);return!(r<0||(r==e.length-1?e.pop():x.call(e,r,1),--this.size,0))},E.prototype.get=function(t){var e=this.__data__,r=S(e,t);return r<0?void 0:e[r][1]},E.prototype.has=function(t){return S(this.__data__,t)>-1},E.prototype.set=function(t,e){var r=this.__data__,n=S(r,t);return n<0?(++this.size,r.push([t,e])):r[n][1]=e,this};var V="object"==typeof r.g&&r.g&&r.g.Object===Object&&r.g,W="object"==typeof self&&self&&self.Object===Object&&self,C=V||W||Function("return this")(),P=C.Symbol,z=Object.prototype,F=z.hasOwnProperty,M=z.toString,$=P?P.toStringTag:void 0,k=Object.prototype.toString,R=P?P.toStringTag:void 0;function D(t){return null==t?void 0===t?"[object Undefined]":"[object Null]":R&&R in Object(t)?function(t){var e=F.call(t,$),r=t[$];try{t[$]=void 0;var n=!0}catch(t){}var o=M.call(t);return n&&(e?t[$]=r:delete t[$]),o}(t):function(t){return k.call(t)}(t)}function U(t){var e=typeof t;return null!=t&&("object"==e||"function"==e)}function I(t){if(!U(t))return!1;var e=D(t);return"[object Function]"==e||"[object GeneratorFunction]"==e||"[object AsyncFunction]"==e||"[object Proxy]"==e}var B,T=C["__core-js_shared__"],L=(B=/[^.]+$/.exec(T&&T.keys&&T.keys.IE_PROTO||""))?"Symbol(src)_1."+B:"",q=Function.prototype.toString;function J(t){if(null!=t){try{return q.call(t)}catch(t){}try{return t+""}catch(t){}}return""}var N=/^\[object .+?Constructor\]$/,G=Function.prototype,Y=Object.prototype,H=G.toString,K=Y.hasOwnProperty,Q=RegExp("^"+H.call(K).replace(/[\\^$.*+?()[\]{}|]/g,"\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g,"$1.*?")+"$");function X(t,e){var r=function(t,e){return null==t?void 0:t[e]}(t,e);return function(t){return!(!U(t)||(e=t,L&&L in e))&&(I(t)?Q:N).test(J(t));var e}(r)?r:void 0}var Z=X(C,"Map"),tt=X(Object,"create"),et=Object.prototype.hasOwnProperty,rt=Object.prototype.hasOwnProperty;function nt(t){var e=-1,r=null==t?0:t.length;for(this.clear();++e<r;){var n=t[e];this.set(n[0],n[1])}}function ot(t,e){var r,n,o=t.__data__;return("string"==(n=typeof(r=e))||"number"==n||"symbol"==n||"boolean"==n?"__proto__"!==r:null===r)?o["string"==typeof e?"string":"hash"]:o.map}function it(t){var e=-1,r=null==t?0:t.length;for(this.clear();++e<r;){var n=t[e];this.set(n[0],n[1])}}function at(t){var e=this.__data__=new E(t);this.size=e.size}nt.prototype.clear=function(){this.__data__=tt?tt(null):{},this.size=0},nt.prototype.delete=function(t){var e=this.has(t)&&delete this.__data__[t];return this.size-=e?1:0,e},nt.prototype.get=function(t){var e=this.__data__;if(tt){var r=e[t];return"__lodash_hash_undefined__"===r?void 0:r}return et.call(e,t)?e[t]:void 0},nt.prototype.has=function(t){var e=this.__data__;return tt?void 0!==e[t]:rt.call(e,t)},nt.prototype.set=function(t,e){var r=this.__data__;return this.size+=this.has(t)?0:1,r[t]=tt&&void 0===e?"__lodash_hash_undefined__":e,this},it.prototype.clear=function(){this.size=0,this.__data__={hash:new nt,map:new(Z||E),string:new nt}},it.prototype.delete=function(t){var e=ot(this,t).delete(t);return this.size-=e?1:0,e},it.prototype.get=function(t){return ot(this,t).get(t)},it.prototype.has=function(t){return ot(this,t).has(t)},it.prototype.set=function(t,e){var r=ot(this,t),n=r.size;return r.set(t,e),this.size+=r.size==n?0:1,this},at.prototype.clear=function(){this.__data__=new E,this.size=0},at.prototype.delete=function(t){var e=this.__data__,r=e.delete(t);return this.size=e.size,r},at.prototype.get=function(t){return this.__data__.get(t)},at.prototype.has=function(t){return this.__data__.has(t)},at.prototype.set=function(t,e){var r=this.__data__;if(r instanceof E){var n=r.__data__;if(!Z||n.length<199)return n.push([t,e]),this.size=++r.size,this;r=this.__data__=new it(n)}return r.set(t,e),this.size=r.size,this};var ct=function(){try{var t=X(Object,"defineProperty");return t({},"",{}),t}catch(t){}}();function ut(t,e,r){"__proto__"==e&&ct?ct(t,e,{configurable:!0,enumerable:!0,value:r,writable:!0}):t[e]=r}var st=Object.prototype.hasOwnProperty;function lt(t,e,r){var n=t[e];st.call(t,e)&&A(n,r)&&(void 0!==r||e in t)||ut(t,e,r)}function ft(t,e,r,n){var o=!r;r||(r={});for(var i=-1,a=e.length;++i<a;){var c=e[i],u=n?n(r[c],t[c],c,r,t):void 0;void 0===u&&(u=t[c]),o?ut(r,c,u):lt(r,c,u)}return r}function pt(t){return null!=t&&"object"==typeof t}function dt(t){return pt(t)&&"[object Arguments]"==D(t)}var ht=Object.prototype,yt=ht.hasOwnProperty,bt=ht.propertyIsEnumerable,vt=dt(function(){return arguments}())?dt:function(t){return pt(t)&&yt.call(t,"callee")&&!bt.call(t,"callee")},_t=Array.isArray,gt="object"==typeof exports&&exports&&!exports.nodeType&&exports,jt=gt&&t&&!t.nodeType&&t,mt=jt&&jt.exports===gt?C.Buffer:void 0,wt=(mt?mt.isBuffer:void 0)||function(){return!1},Ot=/^(?:0|[1-9]\d*)$/;function At(t,e){var r=typeof t;return!!(e=null==e?9007199254740991:e)&&("number"==r||"symbol"!=r&&Ot.test(t))&&t>-1&&t%1==0&&t<e}function St(t){return"number"==typeof t&&t>-1&&t%1==0&&t<=9007199254740991}var xt={};function Et(t){return function(e){return t(e)}}xt["[object Float32Array]"]=xt["[object Float64Array]"]=xt["[object Int8Array]"]=xt["[object Int16Array]"]=xt["[object Int32Array]"]=xt["[object Uint8Array]"]=xt["[object Uint8ClampedArray]"]=xt["[object Uint16Array]"]=xt["[object Uint32Array]"]=!0,xt["[object Arguments]"]=xt["[object Array]"]=xt["[object ArrayBuffer]"]=xt["[object Boolean]"]=xt["[object DataView]"]=xt["[object Date]"]=xt["[object Error]"]=xt["[object Function]"]=xt["[object Map]"]=xt["[object Number]"]=xt["[object Object]"]=xt["[object RegExp]"]=xt["[object Set]"]=xt["[object String]"]=xt["[object WeakMap]"]=!1;var Vt="object"==typeof exports&&exports&&!exports.nodeType&&exports,Wt=Vt&&t&&!t.nodeType&&t,Ct=Wt&&Wt.exports===Vt&&V.process,Pt=function(){try{return Wt&&Wt.require&&Wt.require("util").types||Ct&&Ct.binding&&Ct.binding("util")}catch(t){}}(),zt=Pt&&Pt.isTypedArray,Ft=zt?Et(zt):function(t){return pt(t)&&St(t.length)&&!!xt[D(t)]},Mt=Object.prototype.hasOwnProperty;function $t(t,e){var r=_t(t),n=!r&&vt(t),o=!r&&!n&&wt(t),i=!r&&!n&&!o&&Ft(t),a=r||n||o||i,c=a?function(t,e){for(var r=-1,n=Array(t);++r<t;)n[r]=e(r);return n}(t.length,String):[],u=c.length;for(var s in t)!e&&!Mt.call(t,s)||a&&("length"==s||o&&("offset"==s||"parent"==s)||i&&("buffer"==s||"byteLength"==s||"byteOffset"==s)||At(s,u))||c.push(s);return c}var kt=Object.prototype;function Rt(t){var e=t&&t.constructor;return t===("function"==typeof e&&e.prototype||kt)}function Dt(t,e){return function(r){return t(e(r))}}var Ut=Dt(Object.keys,Object),It=Object.prototype.hasOwnProperty;function Bt(t){return null!=t&&St(t.length)&&!I(t)}function Tt(t){return Bt(t)?$t(t):function(t){if(!Rt(t))return Ut(t);var e=[];for(var r in Object(t))It.call(t,r)&&"constructor"!=r&&e.push(r);return e}(t)}var Lt=Object.prototype.hasOwnProperty;function qt(t){return Bt(t)?$t(t,!0):function(t){if(!U(t))return function(t){var e=[];if(null!=t)for(var r in Object(t))e.push(r);return e}(t);var e=Rt(t),r=[];for(var n in t)("constructor"!=n||!e&&Lt.call(t,n))&&r.push(n);return r}(t)}var Jt="object"==typeof exports&&exports&&!exports.nodeType&&exports,Nt=Jt&&t&&!t.nodeType&&t,Gt=Nt&&Nt.exports===Jt?C.Buffer:void 0,Yt=Gt?Gt.allocUnsafe:void 0;function Ht(){return[]}var Kt=Object.prototype.propertyIsEnumerable,Qt=Object.getOwnPropertySymbols,Xt=Qt?function(t){return null==t?[]:(t=Object(t),function(e,r){for(var n=-1,o=null==e?0:e.length,i=0,a=[];++n<o;){var c=e[n];u=c,Kt.call(t,u)&&(a[i++]=c)}var u;return a}(Qt(t)))}:Ht;function Zt(t,e){for(var r=-1,n=e.length,o=t.length;++r<n;)t[o+r]=e[r];return t}var te=Dt(Object.getPrototypeOf,Object),ee=Object.getOwnPropertySymbols?function(t){for(var e=[];t;)Zt(e,Xt(t)),t=te(t);return e}:Ht;function re(t,e,r){var n=e(t);return _t(t)?n:Zt(n,r(t))}function ne(t){return re(t,Tt,Xt)}function oe(t){return re(t,qt,ee)}var ie=X(C,"DataView"),ae=X(C,"Promise"),ce=X(C,"Set"),ue=X(C,"WeakMap"),se="[object Map]",le="[object Promise]",fe="[object Set]",pe="[object WeakMap]",de="[object DataView]",he=J(ie),ye=J(Z),be=J(ae),ve=J(ce),_e=J(ue),ge=D;(ie&&ge(new ie(new ArrayBuffer(1)))!=de||Z&&ge(new Z)!=se||ae&&ge(ae.resolve())!=le||ce&&ge(new ce)!=fe||ue&&ge(new ue)!=pe)&&(ge=function(t){var e=D(t),r="[object Object]"==e?t.constructor:void 0,n=r?J(r):"";if(n)switch(n){case he:return de;case ye:return se;case be:return le;case ve:return fe;case _e:return pe}return e});var je=ge,me=Object.prototype.hasOwnProperty,we=C.Uint8Array;function Oe(t){var e=new t.constructor(t.byteLength);return new we(e).set(new we(t)),e}var Ae=/\w*$/,Se=P?P.prototype:void 0,xe=Se?Se.valueOf:void 0;var Ee=Object.create,Ve=function(){function t(){}return function(e){if(!U(e))return{};if(Ee)return Ee(e);t.prototype=e;var r=new t;return t.prototype=void 0,r}}(),We=Pt&&Pt.isMap,Ce=We?Et(We):function(t){return pt(t)&&"[object Map]"==je(t)},Pe=Pt&&Pt.isSet,ze=Pe?Et(Pe):function(t){return pt(t)&&"[object Set]"==je(t)},Fe="[object Arguments]",Me="[object Function]",$e="[object Object]",ke={};function Re(t,e,r,n,o,i){var a,c=1&e,u=2&e,s=4&e;if(r&&(a=o?r(t,n,o,i):r(t)),void 0!==a)return a;if(!U(t))return t;var l=_t(t);if(l){if(a=function(t){var e=t.length,r=new t.constructor(e);return e&&"string"==typeof t[0]&&me.call(t,"index")&&(r.index=t.index,r.input=t.input),r}(t),!c)return function(t,e){var r=-1,n=t.length;for(e||(e=Array(n));++r<n;)e[r]=t[r];return e}(t,a)}else{var f=je(t),p=f==Me||"[object GeneratorFunction]"==f;if(wt(t))return function(t,e){if(e)return t.slice();var r=t.length,n=Yt?Yt(r):new t.constructor(r);return t.copy(n),n}(t,c);if(f==$e||f==Fe||p&&!o){if(a=u||p?{}:function(t){return"function"!=typeof t.constructor||Rt(t)?{}:Ve(te(t))}(t),!c)return u?function(t,e){return ft(t,ee(t),e)}(t,function(t,e){return t&&ft(e,qt(e),t)}(a,t)):function(t,e){return ft(t,Xt(t),e)}(t,function(t,e){return t&&ft(e,Tt(e),t)}(a,t))}else{if(!ke[f])return o?t:{};a=function(t,e,r){var n,o,i,a=t.constructor;switch(e){case"[object ArrayBuffer]":return Oe(t);case"[object Boolean]":case"[object Date]":return new a(+t);case"[object DataView]":return function(t,e){var r=e?Oe(t.buffer):t.buffer;return new t.constructor(r,t.byteOffset,t.byteLength)}(t,r);case"[object Float32Array]":case"[object Float64Array]":case"[object Int8Array]":case"[object Int16Array]":case"[object Int32Array]":case"[object Uint8Array]":case"[object Uint8ClampedArray]":case"[object Uint16Array]":case"[object Uint32Array]":return function(t,e){var r=e?Oe(t.buffer):t.buffer;return new t.constructor(r,t.byteOffset,t.length)}(t,r);case"[object Map]":case"[object Set]":return new a;case"[object Number]":case"[object String]":return new a(t);case"[object RegExp]":return(i=new(o=t).constructor(o.source,Ae.exec(o))).lastIndex=o.lastIndex,i;case"[object Symbol]":return n=t,xe?Object(xe.call(n)):{}}}(t,f,c)}}i||(i=new at);var d=i.get(t);if(d)return d;i.set(t,a),ze(t)?t.forEach((function(n){a.add(Re(n,e,r,n,t,i))})):Ce(t)&&t.forEach((function(n,o){a.set(o,Re(n,e,r,o,t,i))}));var h=l?void 0:(s?u?oe:ne:u?qt:Tt)(t);return function(t,e){for(var r=-1,n=null==t?0:t.length;++r<n&&!1!==e(t[r],r););}(h||t,(function(n,o){h&&(n=t[o=n]),lt(a,o,Re(n,e,r,o,t,i))})),a}function De(t){return Re(t,5)}ke[Fe]=ke["[object Array]"]=ke["[object ArrayBuffer]"]=ke["[object DataView]"]=ke["[object Boolean]"]=ke["[object Date]"]=ke["[object Float32Array]"]=ke["[object Float64Array]"]=ke["[object Int8Array]"]=ke["[object Int16Array]"]=ke["[object Int32Array]"]=ke["[object Map]"]=ke["[object Number]"]=ke[$e]=ke["[object RegExp]"]=ke["[object Set]"]=ke["[object String]"]=ke["[object Symbol]"]=ke["[object Uint8Array]"]=ke["[object Uint8ClampedArray]"]=ke["[object Uint16Array]"]=ke["[object Uint32Array]"]=!0,ke["[object Error]"]=ke[Me]=ke["[object WeakMap]"]=!1;function Ue(t){var e=-1,r=null==t?0:t.length;for(this.__data__=new it;++e<r;)this.add(t[e])}function Ie(t,e){for(var r=-1,n=null==t?0:t.length;++r<n;)if(e(t[r],r,t))return!0;return!1}function Be(t,e,r,n,o,i){var a=1&r,c=t.length,u=e.length;if(c!=u&&!(a&&u>c))return!1;var s=i.get(t),l=i.get(e);if(s&&l)return s==e&&l==t;var f=-1,p=!0,d=2&r?new Ue:void 0;for(i.set(t,e),i.set(e,t);++f<c;){var h=t[f],y=e[f];if(n)var b=a?n(y,h,f,e,t,i):n(h,y,f,t,e,i);if(void 0!==b){if(b)continue;p=!1;break}if(d){if(!Ie(e,(function(t,e){if(a=e,!d.has(a)&&(h===t||o(h,t,r,n,i)))return d.push(e);var a}))){p=!1;break}}else if(h!==y&&!o(h,y,r,n,i)){p=!1;break}}return i.delete(t),i.delete(e),p}function Te(t){var e=-1,r=Array(t.size);return t.forEach((function(t,n){r[++e]=[n,t]})),r}function Le(t){var e=-1,r=Array(t.size);return t.forEach((function(t){r[++e]=t})),r}Ue.prototype.add=Ue.prototype.push=function(t){return this.__data__.set(t,"__lodash_hash_undefined__"),this},Ue.prototype.has=function(t){return this.__data__.has(t)};var qe=P?P.prototype:void 0,Je=qe?qe.valueOf:void 0,Ne=Object.prototype.hasOwnProperty,Ge="[object Arguments]",Ye="[object Array]",He="[object Object]",Ke=Object.prototype.hasOwnProperty;function Qe(t,e,r,n,o){return t===e||(null==t||null==e||!pt(t)&&!pt(e)?t!=t&&e!=e:function(t,e,r,n,o,i){var a=_t(t),c=_t(e),u=a?Ye:je(t),s=c?Ye:je(e),l=(u=u==Ge?He:u)==He,f=(s=s==Ge?He:s)==He,p=u==s;if(p&&wt(t)){if(!wt(e))return!1;a=!0,l=!1}if(p&&!l)return i||(i=new at),a||Ft(t)?Be(t,e,r,n,o,i):function(t,e,r,n,o,i,a){switch(r){case"[object DataView]":if(t.byteLength!=e.byteLength||t.byteOffset!=e.byteOffset)return!1;t=t.buffer,e=e.buffer;case"[object ArrayBuffer]":return!(t.byteLength!=e.byteLength||!i(new we(t),new we(e)));case"[object Boolean]":case"[object Date]":case"[object Number]":return A(+t,+e);case"[object Error]":return t.name==e.name&&t.message==e.message;case"[object RegExp]":case"[object String]":return t==e+"";case"[object Map]":var c=Te;case"[object Set]":var u=1&n;if(c||(c=Le),t.size!=e.size&&!u)return!1;var s=a.get(t);if(s)return s==e;n|=2,a.set(t,e);var l=Be(c(t),c(e),n,o,i,a);return a.delete(t),l;case"[object Symbol]":if(Je)return Je.call(t)==Je.call(e)}return!1}(t,e,u,r,n,o,i);if(!(1&r)){var d=l&&Ke.call(t,"__wrapped__"),h=f&&Ke.call(e,"__wrapped__");if(d||h){var y=d?t.value():t,b=h?e.value():e;return i||(i=new at),o(y,b,r,n,i)}}return!!p&&(i||(i=new at),function(t,e,r,n,o,i){var a=1&r,c=ne(t),u=c.length;if(u!=ne(e).length&&!a)return!1;for(var s=u;s--;){var l=c[s];if(!(a?l in e:Ne.call(e,l)))return!1}var f=i.get(t),p=i.get(e);if(f&&p)return f==e&&p==t;var d=!0;i.set(t,e),i.set(e,t);for(var h=a;++s<u;){var y=t[l=c[s]],b=e[l];if(n)var v=a?n(b,y,l,e,t,i):n(y,b,l,t,e,i);if(!(void 0===v?y===b||o(y,b,r,n,i):v)){d=!1;break}h||(h="constructor"==l)}if(d&&!h){var _=t.constructor,g=e.constructor;_==g||!("constructor"in t)||!("constructor"in e)||"function"==typeof _&&_ instanceof _&&"function"==typeof g&&g instanceof g||(d=!1)}return i.delete(t),i.delete(e),d}(t,e,r,n,o,i))}(t,e,r,n,Qe,o))}function Xe(t){return t==t&&!U(t)}function Ze(t,e){return function(r){return null!=r&&r[t]===e&&(void 0!==e||t in Object(r))}}function tr(t){return"symbol"==typeof t||pt(t)&&"[object Symbol]"==D(t)}var er=/\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/,rr=/^\w*$/;function nr(t,e){if(_t(t))return!1;var r=typeof t;return!("number"!=r&&"symbol"!=r&&"boolean"!=r&&null!=t&&!tr(t))||rr.test(t)||!er.test(t)||null!=e&&t in Object(e)}function or(t,e){if("function"!=typeof t||null!=e&&"function"!=typeof e)throw new TypeError("Expected a function");var r=function(){var n=arguments,o=e?e.apply(this,n):n[0],i=r.cache;if(i.has(o))return i.get(o);var a=t.apply(this,n);return r.cache=i.set(o,a)||i,a};return r.cache=new(or.Cache||it),r}or.Cache=it;var ir,ar,cr,ur=/[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g,sr=/\\(\\)?/g,lr=(ir=function(t){var e=[];return 46===t.charCodeAt(0)&&e.push(""),t.replace(ur,(function(t,r,n,o){e.push(n?o.replace(sr,"$1"):r||t)})),e},ar=or(ir,(function(t){return 500===cr.size&&cr.clear(),t})),cr=ar.cache,ar),fr=P?P.prototype:void 0,pr=fr?fr.toString:void 0;function dr(t){if("string"==typeof t)return t;if(_t(t))return function(t,e){for(var r=-1,n=null==t?0:t.length,o=Array(n);++r<n;)o[r]=e(t[r],r,t);return o}(t,dr)+"";if(tr(t))return pr?pr.call(t):"";var e=t+"";return"0"==e&&1/t==-1/0?"-0":e}function hr(t,e){return _t(t)?t:nr(t,e)?[t]:lr(function(t){return null==t?"":dr(t)}(t))}function yr(t){if("string"==typeof t||tr(t))return t;var e=t+"";return"0"==e&&1/t==-1/0?"-0":e}function br(t,e){for(var r=0,n=(e=hr(e,t)).length;null!=t&&r<n;)t=t[yr(e[r++])];return r&&r==n?t:void 0}function vr(t,e){return null!=t&&e in Object(t)}function _r(t,e){return nr(t)&&Xe(e)?Ze(yr(t),e):function(r){var n=function(t,e,r){var n=null==t?void 0:br(t,e);return void 0===n?void 0:n}(r,t);return void 0===n&&n===e?function(t,e){return null!=t&&function(t,e,r){for(var n=-1,o=(e=hr(e,t)).length,i=!1;++n<o;){var a=yr(e[n]);if(!(i=null!=t&&r(t,a)))break;t=t[a]}return i||++n!=o?i:!!(o=null==t?0:t.length)&&St(o)&&At(a,o)&&(_t(t)||vt(t))}(t,e,vr)}(r,t):Qe(e,n,3)}}function gr(t){return t}function jr(t,e){var r,n,o,i,a,c={};return e="function"==typeof(r=e)?r:null==r?gr:"object"==typeof r?_t(r)?_r(r[0],r[1]):(a=function(t){for(var e=Tt(t),r=e.length;r--;){var n=e[r],o=t[n];e[r]=[n,o,Xe(o)]}return e}(i=r),1==a.length&&a[0][2]?Ze(a[0][0],a[0][1]):function(t){return t===i||function(t,e,r,n){var o=r.length,i=o;if(null==t)return!i;for(t=Object(t);o--;){var a=r[o];if(a[2]?a[1]!==t[a[0]]:!(a[0]in t))return!1}for(;++o<i;){var c=(a=r[o])[0],u=t[c],s=a[1];if(a[2]){if(void 0===u&&!(c in t))return!1}else{var l,f=new at;if(!(void 0===l?Qe(s,u,3,n,f):l))return!1}}return!0}(t,0,a)}):nr(n=r)?(o=yr(n),function(t){return null==t?void 0:t[o]}):function(t){return function(e){return br(e,t)}}(n),function(t,e){t&&function(t,e,r){for(var n=-1,o=Object(t),i=r(t),a=i.length;a--;){var c=i[++n];if(!1===e(o[c],c,o))break}}(t,e,Tt)}(t,(function(t,r,n){ut(c,r,e(t,r,n))})),c}class mr extends n.DOMWidgetView{render(){super.render(),(async()=>{await this.displayed;const t=document.createElement("div");if(this.el.appendChild(t),!(this.model instanceof c))throw Error("VueWidgetView can only be created from a VueWidgetModel");const e=await this.container;this.app=(0,o.createApp)((()=>(0,o.h)(e))),this.app.mount(t)})()}remove(){var t;return null===(t=this.app)||void 0===t||t.unmount(),super.remove()}get component(){return(async()=>{const t=this,e=this.model,r=this.model.get("_VueWidget__components");return(0,o.defineComponent)({name:e.get("_VueWidget__type"),template:e.get("_VueWidget__template"),data:()=>De(e.reactiveState),created(){for(const r of Object.keys(e.reactiveState))t.listenTo(t.model,`change:${r}`,(()=>t.onModelChange(r,this))),this.$watch(r,(()=>t.onDataChange(r,this)))},components:await new O(this.model.get("_VueWidget__assets")).compileAsync(r),methods:e.methods})})()}get container(){return(async()=>{const t=this,e=await this.component,r=this.modelRenderer;return(0,o.defineComponent)({name:"VueWidgetContainer",data:()=>({children:{}}),created(){const e=()=>t.onModelChange("_VueWidget__children",this,"children");t.listenTo(t.model,"change:_VueWidget__children",e),e()},render(){return(0,o.h)(e,null,jr(this.children,(t=>()=>(0,o.h)(r,{modelId:t.substring("IPY_MODEL_".length)}))))}})})()}get modelRenderer(){const t=this;return(0,o.defineComponent)({name:"ModelRenderer",props:{modelId:String},data:()=>({widget:null,trash:Object.freeze({views:[]})}),watch:{modelId:{async handler(e,r){if(e===r)return;const n=await t.model.widget_manager.get_model(e);if(void 0===n)return console.error(`ignoring child ${e} which has not active model`),null;null!=this.widget&&this.trash.views.push(this.widget.view),this.widget=Object.freeze({view:await t.create_child_view(n)})},immediate:!0}},render(){const t=this,e=this.widget;if(null!=e)return(0,o.h)((0,o.defineComponent)({mounted(){n.JupyterPhosphorWidget.attach(e.view.pWidget,this.$el),t.cleanup()},render:()=>(0,o.h)("div")}));this.cleanup()},destroyed(){this.cleanup()},methods:{cleanup(){for(;this.trash.views.length;)this.trash.views.pop().remove()}}})}onModelChange(t,e,r){e[r||t]=De(this.model.get(t))}onDataChange(t,e){const r=e[t];this.model.set(t,void 0===r?null:De(r)),this.model.save_changes()}}},565:t=>{t.exports={i8:"0.0.3"}}}]);