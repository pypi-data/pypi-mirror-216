/*! For license information please see 54512-EFnW6fGHE-M.js.LICENSE.txt */
export const id=54512;export const ids=[54512];export const modules={53973:(e,t,r)=>{r(56299),r(65660),r(97968);var n=r(9672),o=r(50856),a=r(33760);(0,n.k)({_template:o.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[a.U]})},82160:(e,t,r)=>{function n(e){return new Promise(((t,r)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>r(e.error)}))}function o(e,t){const r=indexedDB.open(e);r.onupgradeneeded=()=>r.result.createObjectStore(t);const o=n(r);return(e,r)=>o.then((n=>r(n.transaction(t,e).objectStore(t))))}let a;function s(){return a||(a=o("keyval-store","keyval")),a}function p(e,t=s()){return t("readonly",(t=>n(t.get(e))))}function c(e,t,r=s()){return r("readwrite",(r=>(r.put(t,e),n(r.transaction))))}function l(e=s()){return e("readwrite",(e=>(e.clear(),n(e.transaction))))}r.d(t,{MT:()=>o,RV:()=>n,U2:()=>p,ZH:()=>l,t8:()=>c})}};
//# sourceMappingURL=54512-EFnW6fGHE-M.js.map