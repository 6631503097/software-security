// Execute the unmodified instructor simulation with a minimal DOM adapter.
// This is an engine check, NOT browser execution or screenshot evidence.
const fs=require('fs'),vm=require('vm');
const elements={};
for(const id of ['priv','pub','mode-single','mode-merged','presets','verdict','explain','priv-card','pub-card'])elements[id]={value:'',checked:false,children:[],addEventListener(k,f){this[k]=f},appendChild(x){this.children.push(x)}};
for (const [id,other] of [['mode-single','mode-merged'],['mode-merged','mode-single']]) {let checked=false;Object.defineProperty(elements[id],'checked',{get(){return checked},set(v){checked=v;if(v)elements[other].checked=false}})}
elements.priv.value='1.4.0';elements.pub.value='99.0.0';elements['mode-merged'].checked=true;
const document={getElementById:id=>elements[id],createElement:()=>({addEventListener(k,f){this[k]=f}})};
const source='labs/live-quiz/static/sim/resolver-confusion.js';
vm.runInNewContext(fs.readFileSync(source,'utf8'),{document});
let results=[];
for (const button of elements.presets.children){button.click(); results.push({preset:button.textContent,private:elements.priv.value,public:elements.pub.value,mode:elements['mode-merged'].checked?'merged':'single',verdict:elements.verdict.textContent,explanation:elements.explain.textContent});}
console.log(JSON.stringify({method:'Unmodified instructor JS executed in Node vm with DOM adapter; browser interaction and screenshots remain pending',source,results},null,2));
