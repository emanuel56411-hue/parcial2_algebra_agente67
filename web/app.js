"use strict";

const A_BASE = [[2,1,3,1,2,1],[1,3,2,2,1,2],[3,2,4,1,3,2],[1,1,1,4,2,1],[2,1,2,1,5,3],[1,2,1,2,1,4]];
const B_GUIDE = [155,160,225,140,215,175];
const scenarios = {
  original:{title:"TechChip · datos originales",note:"Disponibilidades transcritas de la guía, sin correcciones ocultas.",A:A_BASE,B:B_GUIDE,production:true},
  compatible:{title:"TechChip · vector esperado",note:"Variante didáctica con B = A·X esperado; no es la disponibilidad original de la guía.",A:A_BASE,B:[185,200,280,150,245,195],production:true},
  scarcity:{title:"Escasez · resina a 100 kg",note:"Parte de B original y modifica únicamente B₃ = 100.",A:A_BASE,B:[155,160,100,140,215,175],production:true},
  singular:{title:"Singular · sin solución",note:"F₆ = 2F₁, conservando B₆ = 175; aparece una contradicción.",A:[...A_BASE.slice(0,5),A_BASE[0].map(v=>2*v)],B:B_GUIDE,production:true},
  infinite:{title:"Singular · infinitas soluciones",note:"F₆ = 2F₁ y B₆ = 2B₁; una variable queda libre.",A:[...A_BASE.slice(0,5),A_BASE[0].map(v=>2*v)],B:[155,160,225,140,215,310],production:true},
  example:{title:"Ejemplo guiado · 3 × 3",note:"Sistema pequeño con solución X = (2, 3, −1).",A:[[2,1,-1],[-3,-1,2],[-2,1,2]],B:[8,-11,-3],production:false}
};
const labels={unique:"Solución única",infinite:"Infinitas soluciones",inconsistent:"Sin solución"};
const methodLabels={diagnosis:"Diagnóstico",gauss:"Eliminación de Gauss",gauss_jordan:"Gauss-Jordan",inverse:"Matriz inversa"};
const $=selector=>document.querySelector(selector);
let currentInput=null,currentReport=null,currentStep=0,currentSteps=[],tutorHistory=[],stepContext=null;

function applyTheme(theme,persist=false){
  const normalized=theme==="dark"?"dark":"light",dark=normalized==="dark";
  document.documentElement.dataset.theme=normalized;
  const toggle=$("#theme-toggle"),meta=document.querySelector('meta[name="theme-color"]');
  if(toggle){
    toggle.setAttribute("aria-pressed",String(dark));
    toggle.setAttribute("aria-label",dark?"Activar modo claro":"Activar modo oscuro");
    toggle.querySelector(".theme-icon").textContent=dark?"☀":"☾";
    toggle.querySelector(".theme-label").textContent=dark?"Claro":"Oscuro";
  }
  if(meta)meta.content=dark?"#0b1614":"#123b35";
  if(persist){try{localStorage.setItem("techchip-theme",normalized);}catch(_){} }
}

function initTheme(){
  applyTheme(document.documentElement.dataset.theme||"light");
  $("#theme-toggle").addEventListener("click",()=>applyTheme(document.documentElement.dataset.theme==="dark"?"light":"dark",true));
}

function clone(value){return JSON.parse(JSON.stringify(value));}
function escapeHtml(value){return String(value).replace(/[&<>'"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"})[c]);}
function numeric(value){const [a,b="1"]=String(value).split("/");return Number(a)/Number(b);}
function decimal(value){const n=numeric(value);if(!Number.isFinite(n))return "—";if(n!==0&&(Math.abs(n)>=1e9||Math.abs(n)<1e-5))return n.toExponential(5);return n.toLocaleString("es-SV",{maximumFractionDigits:6});}

function init(){
  initTheme();
  const select=$("#scenario");
  Object.entries(scenarios).forEach(([key,item])=>select.add(new Option(item.title,key)));
  select.value="original";
  select.addEventListener("change",loadScenario);
  $("#source").addEventListener("change",changeSource);
  $("#dimension").addEventListener("change",loadCustom);
  $("#solve").addEventListener("click",solve);
  $("#new-analysis").addEventListener("click",()=>$("#workspace").scrollIntoView());
  $("#method").addEventListener("change",()=>loadMethod($("#method").value));
  $("#prev-step").addEventListener("click",()=>showStep(currentStep-1));
  $("#next-step").addEventListener("click",()=>showStep(currentStep+1));
  $("#step-range").addEventListener("input",event=>showStep(Number(event.target.value)-1));
  $("#step-view").addEventListener("click",()=>setProcedureView("single"));
  $("#all-view").addEventListener("click",()=>setProcedureView("all"));
  $("#expand-all").addEventListener("click",()=>document.querySelectorAll("#all-steps details").forEach(item=>item.open=true));
  $("#collapse-all").addEventListener("click",()=>document.querySelectorAll("#all-steps details").forEach(item=>item.open=false));
  $("#explain-step").addEventListener("click",explainCurrentStep);
  $("#chat-form").addEventListener("submit",event=>{event.preventDefault();sendTutorQuestion($("#chat-input").value);});
  $("#chat-messages").addEventListener("click",event=>{if(event.target.dataset.question)sendTutorQuestion(event.target.dataset.question);});
  document.querySelectorAll("[role=tab]").forEach(tab=>tab.addEventListener("click",()=>activateTab(tab.dataset.tab)));
  $("#download-result").addEventListener("click",()=>download("resultado-techchip.json",currentReport));
  $("#download-input").addEventListener("click",()=>download("sistema.json",{A:currentInput.A,B:currentInput.B}));
  $("#print-result").addEventListener("click",()=>window.print());
  loadScenario();
}

function loadScenario(){
  const item=scenarios[$("#scenario").value];
  $("#scenario-note").textContent=item.note;
  $("#production").checked=item.production;
  $("#production-row").classList.toggle("hidden",item.production);
  $("#guide-warning").classList.toggle("hidden",$("#scenario").value==="example");
  renderEditor(clone(item.A),clone(item.B));
}

function changeSource(){
  const source=$("#source").value;
  $("#scenario-field").classList.toggle("hidden",source!=="scenario");
  $("#dimension-field").classList.toggle("hidden",source!=="custom");
  $("#json-field").classList.toggle("hidden",source!=="json");
  $("#guide-warning").classList.toggle("hidden",source!=="scenario"||$("#scenario").value==="example");
  $("#production-row").classList.remove("hidden");
  if(source==="scenario")loadScenario();
  else if(source==="custom"){$("#production").checked=false;loadCustom();}
  else{$("#production").checked=false;renderEditor([[2,1],[1,-1]],[5,1]);}
}

function loadCustom(){
  const n=Math.max(1,Math.min(12,Number($("#dimension").value)||3));
  $("#dimension").value=n;
  renderEditor(Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?1:0)),Array(n).fill(1));
}

function renderEditor(A,B){
  const n=A.length,head=$("#matrix-editor thead"),body=$("#matrix-editor tbody");
  head.replaceChildren();body.replaceChildren();
  const hr=document.createElement("tr");hr.append(document.createElement("th"));
  [...Array(n)].forEach((_,i)=>{const th=document.createElement("th");th.textContent=`x${i+1}`;hr.append(th);});
  const bth=document.createElement("th");bth.textContent="B";hr.append(bth);head.append(hr);
  A.forEach((row,i)=>{const tr=document.createElement("tr"),label=document.createElement("td");label.textContent=`F${i+1}`;tr.append(label);
    [...row,B[i]].forEach((value,j)=>{const td=document.createElement("td"),input=document.createElement("input");input.value=value;input.dataset.row=i;input.dataset.col=j;input.setAttribute("aria-label",j===n?`B, fila ${i+1}`:`A, fila ${i+1}, columna ${j+1}`);td.append(input);tr.append(td);});body.append(tr);});
  $("#size-badge").textContent=`${n} × ${n}`;
}

function editorData(){
  const rows=[...document.querySelectorAll("#matrix-editor tbody tr")];
  const A=[],B=[];
  rows.forEach(row=>{const values=[...row.querySelectorAll("input")].map(input=>input.value.trim());A.push(values.slice(0,-1));B.push(values.at(-1));});
  return {A,B};
}

async function solve(){
  const button=$("#solve"),error=$("#error");error.classList.add("hidden");
  try{
    let data;
    if($("#source").value==="json"){
      try{data=JSON.parse($("#json-input").value);}catch(_){throw new Error("El texto no es JSON válido.");}
      if(!data||!Array.isArray(data.A)||!Array.isArray(data.B))throw new Error("El JSON debe contener las matrices A y B.");
    }else data=editorData();
    data.production=$("#production").checked;
    currentInput=clone(data);button.disabled=true;button.textContent="Analizando…";
    const response=await fetch("/api/solve",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
    const result=await response.json().catch(()=>({error:"La API no devolvió una respuesta válida."}));
    if(!response.ok)throw new Error(result.error||"No se pudo resolver el sistema.");
    currentReport=result;tutorHistory=[];stepContext=null;renderTutorMessages();renderResults(result);$("#results").classList.remove("hidden");$("#results").scrollIntoView({behavior:"smooth"});
  }catch(exc){error.textContent=exc.message;error.classList.remove("hidden");}
  finally{button.disabled=false;button.innerHTML='Resolver sistema <span aria-hidden="true">→</span>';}
}

function renderResults(report){
  $("#metric-status").textContent=labels[report.status]||report.status;
  $("#metric-det").textContent=report.determinant;
  $("#metric-ranks").textContent=`${report.rank_A} / ${report.rank_augmented}`;
  $("#metric-error").textContent=report.max_error??"No aplica";
  const interpretation=$("#interpretation");interpretation.textContent=report.interpretation[0]||"Análisis completado.";
  interpretation.className="message"+(report.status==="inconsistent"?" error":report.solution&&report.production&&report.solution.some(v=>numeric(v)<0)?" warning":"");
  renderSummary(report);renderProcedure(report);renderVerification(report);activateTab("summary");
}

function renderSummary(report){
  const panel=$("#tab-summary");
  if(report.solution){
    const max=Math.max(...report.solution.map(v=>Math.abs(numeric(v))),1);
    const rows=report.solution.map((v,i)=>`<tr><td>x${i+1}</td><td>${escapeHtml(v)}</td><td>${escapeHtml(decimal(v))}</td>${report.production?`<td>${numeric(v)<0?"No viable":"No negativa"}</td>`:""}</tr>`).join("");
    const bars=report.solution.map((v,i)=>`<div class="value-row"><b>x${i+1}</b><div class="bar-track"><div class="bar ${numeric(v)<0?"negative":""}" style="width:${Math.max(2,Math.abs(numeric(v))/max*100)}%"></div></div><span>${escapeHtml(decimal(v))}</span></div>`).join("");
    panel.innerHTML=`<div class="solution-layout"><div><h3>Solución por variable</h3><table class="data-table"><thead><tr><th>Variable</th><th>Exacto</th><th>Decimal ≈</th>${report.production?"<th>Factibilidad</th>":""}</tr></thead><tbody>${rows}</tbody></table></div><div><h3>Distribución de la solución</h3><div class="value-bars">${bars}</div></div></div>${interpretationList(report)}`;
  }else if(report.particular){
    const terms=report.nullspace.map((v,i)=>`t${i+1} · (${v.map(escapeHtml).join(", ")})`).join(" + ");
    panel.innerHTML=`<h3>Familia de soluciones</h3><div class="family">X = (${report.particular.map(escapeHtml).join(", ")})${terms?" + "+terms:""}<br><small>t₁, t₂, … son parámetros reales libres.</small></div>${interpretationList(report)}`;
  }else panel.innerHTML=`<h3>El sistema no tiene solución</h3>${interpretationList(report)}`;
}

function interpretationList(report){return report.interpretation.length>1?`<ul class="interpretation-list">${report.interpretation.slice(1).map(v=>`<li>${escapeHtml(v)}</li>`).join("")}</ul>`:"";}

function renderProcedure(report){
  const select=$("#method");select.replaceChildren();
  const keys=["diagnosis",...Object.keys(report.methods)];keys.forEach(key=>select.add(new Option(methodLabels[key],key)));
  const preferred=$("#preferred-method").value;
  loadMethod(report.methods[preferred]?preferred:"diagnosis");
  setProcedureView("single");
}

function loadMethod(key){
  const goals={diagnosis:"Decidir si existe una solución y si es única",gauss:"Construir U y resolver de abajo hacia arriba",gauss_jordan:"Convertir A en I para leer X directamente",inverse:"Construir A⁻¹ y calcular X = A⁻¹B"};
  $("#method").value=key;$("#procedure-goal").textContent=goals[key];currentSteps=key==="diagnosis"?currentReport.diagnostic_steps:currentReport.methods[key].steps;showStep(0);renderAllSteps();
}

function stepPhase(step){
  if(step.kind==="swap")return "ELECCIÓN DE PIVOTE";
  if(step.kind==="scale")return "NORMALIZACIÓN";
  if(step.kind==="add")return "ELIMINACIÓN";
  if(step.kind==="substitution")return "SUSTITUCIÓN HACIA ATRÁS";
  if(step.kind==="multiplication")return "PRODUCTO A⁻¹B";
  if(step.operation.includes("det(A)"))return "DIAGNÓSTICO";
  if(step.operation.includes("lectura")||step.operation.includes("inversa obtenida"))return "RESULTADO DEL MÉTODO";
  return "PUNTO DE CONTROL";
}

function equivalenceReason(step){
  const reasons={swap:"Mismas ecuaciones, solo cambia el orden.",scale:"Se multiplica por un factor no nulo; la operación puede deshacerse.",add:"Se suma un múltiplo de otra ecuación; la operación puede deshacerse.",substitution:"Se despeja una incógnita usando igualdades ya obtenidas.",multiplication:"Se aplica la identidad X = A⁻¹B componente por componente."};
  return reasons[step.kind]||"La matriz se conserva como evidencia del estado alcanzado.";
}

function formatRow(row){return `[ ${row.map(escapeHtml).join("     ")} ]`;}

function showStep(index){
  if(!currentSteps.length)return;currentStep=Math.max(0,Math.min(currentSteps.length-1,index));const step=currentSteps[currentStep];
  $("#step-counter").textContent=`${currentStep+1} / ${currentSteps.length}`;$("#step-label").textContent=`PASO ${String(currentStep+1).padStart(2,"0")}`;
  $("#step-phase").textContent=stepPhase(step);$("#step-operation").textContent=step.operation;$("#step-explanation").textContent=step.explanation;
  $("#step-reasoning").innerHTML=`<span>POR QUÉ ES VÁLIDO</span><p>${escapeHtml(equivalenceReason(step))}</p>`;
  const previous=currentStep?currentSteps[currentStep-1].matrix:null;
  $("#step-matrix").innerHTML=matrixHtml(step.matrix,step.split,step,previous);
  const change=$("#row-change");
  if(previous&&Number.isInteger(step.target)&&previous[step.target]){
    change.innerHTML=`<span>FILA AFECTADA F${step.target+1}</span><div><code><small>ANTES</small>${formatRow(previous[step.target])}</code><b aria-hidden="true">→</b><code><small>DESPUÉS</small>${formatRow(step.matrix[step.target])}</code></div>`;change.classList.remove("hidden");
  }else{change.replaceChildren();change.classList.add("hidden");}
  $("#step-range").max=currentSteps.length;$("#step-range").value=currentStep+1;$("#prev-step").disabled=currentStep===0;$("#next-step").disabled=currentStep===currentSteps.length-1;
}

function matrixHtml(matrix,split,step=null,previous=null){return `<table class="rendered-matrix"><tbody>${matrix.map((row,rowIndex)=>`<tr class="${step&&rowIndex===step.target?"target-row":step&&rowIndex===step.source?"source-row":""}">${row.map((value,i)=>{const changed=previous&&previous[rowIndex]&&String(previous[rowIndex][i])!==String(value);return `<td class="${i===split?"split ":""}${changed?"changed-cell":""}">${escapeHtml(value)}</td>`;}).join("")}</tr>`).join("")}</tbody></table>`;}

function setProcedureView(view){
  const all=view==="all";$("#single-step").classList.toggle("hidden",all);$(".step-actions").classList.toggle("hidden",all);$("#explain-step").classList.toggle("hidden",all);$("#complete-toolbar").classList.toggle("hidden",!all);$("#all-steps").classList.toggle("hidden",!all);$("#step-view").classList.toggle("active",!all);$("#all-view").classList.toggle("active",all);$("#step-counter").textContent=all?`${currentSteps.length} pasos documentados`:`${currentStep+1} / ${currentSteps.length}`;
}

function renderAllSteps(){
  $("#all-steps").innerHTML=currentSteps.map((step,i)=>{const previous=i?currentSteps[i-1].matrix:null;return `<details class="all-step" ${i===0||i===currentSteps.length-1?"open":""}><summary><span>PASO ${String(i+1).padStart(2,"0")} · ${stepPhase(step)}</span><h3>${escapeHtml(step.operation)}</h3><i aria-hidden="true">+</i></summary><div class="all-step-content"><p>${escapeHtml(step.explanation)}</p><div class="inline-proof"><b>Por qué es válido:</b> ${escapeHtml(equivalenceReason(step))}</div><div class="matrix-scroll">${matrixHtml(step.matrix,step.split,step,previous)}</div></div></details>`;}).join("");
}

function currentTitle(){
  if($("#source").value==="scenario")return scenarios[$("#scenario").value].title;
  return $("#source").value==="json"?"Sistema importado":"Sistema personalizado";
}

function currentNote(){return $("#source").value==="scenario"?scenarios[$("#scenario").value].note:"Datos proporcionados por el usuario.";}

function explainCurrentStep(){
  stepContext={method:$("#method").value,step_index:currentStep};
  activateTab("tutor");
  sendTutorQuestion("Explica este paso completo: identifica la operación aplicada, justifica por qué conserva las soluciones y verifica cómo cambia cada entrada, incluido el bloque derecho.",true);
}

async function sendTutorQuestion(rawQuestion,useStep=false){
  const question=String(rawQuestion||"").trim(),button=$("#send-question"),error=$("#tutor-error");
  if(!currentReport||!currentInput)return;
  if(!question||question.length>1500){error.textContent="Escribe una pregunta de 1 a 1500 caracteres.";error.classList.remove("hidden");return;}
  error.classList.add("hidden");tutorHistory.push({role:"user",content:question});renderTutorMessages();$("#chat-input").value="";button.disabled=true;button.textContent="Consultando…";
  const context=useStep?stepContext:null;
  try{
    const payload={...currentInput,question,history:tutorHistory.slice(0,-1).slice(-6),title:currentTitle(),note:currentNote()};
    if(context){payload.method=context.method;payload.step_index=context.step_index;}
    const response=await fetch("/api/tutor",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)}),result=await response.json().catch(()=>({error:"El tutor no devolvió una respuesta válida."}));
    if(!response.ok)throw new Error(result.error||"El Tutor IA no pudo responder.");
    tutorHistory.push({role:"assistant",content:result.answer,meta:`${result.model} · ${result.input_tokens} entrada / ${result.output_tokens} salida`});
    tutorHistory=tutorHistory.slice(-12);renderTutorMessages();
  }catch(exc){tutorHistory.pop();renderTutorMessages();error.textContent=exc.message;error.classList.remove("hidden");}
  finally{button.disabled=false;button.textContent="Enviar pregunta";stepContext=null;}
}

function renderTutorMessages(){
  const box=$("#chat-messages");if(!box)return;
  if(!tutorHistory.length){box.innerHTML='<div class="chat-empty"><strong>Preguntas sugeridas</strong><button type="button" data-question="¿Por qué este sistema tiene este diagnóstico?">¿Por qué aparece este diagnóstico?</button><button type="button" data-question="Explica la interpretación empresarial de la solución sin cambiar los resultados.">¿Qué significa para la planta?</button><button type="button" data-question="Compara los tres métodos y explica por qué deben coincidir.">¿Por qué coinciden los métodos?</button></div>';return;}
  box.innerHTML=tutorHistory.map(message=>`<div class="chat-message ${message.role}">${escapeHtml(message.content)}${message.meta?`<small>${escapeHtml(message.meta)}</small>`:""}</div>`).join("");box.scrollTop=box.scrollHeight;
}

function renderVerification(report){
  const panel=$("#tab-verification");
  if(report.solution){
    const names=Object.values(report.methods);const rows=report.solution.map((_,i)=>`<tr><td>x${i+1}</td>${names.map(m=>`<td>${escapeHtml(m.solution[i])}</td>`).join("")}</tr>`).join("");
    panel.innerHTML=`<div class="message verification-note">Los tres métodos coinciden exactamente. El error racional por componente es ${escapeHtml(report.max_error)}.</div><table class="method-table"><thead><tr><th>Variable</th>${names.map(m=>`<th>${escapeHtml(m.name)}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table><h3>Sustitución directa</h3><div class="substitutions">${report.substitution.map(v=>`<code>${escapeHtml(v)}</code>`).join("")}</div>`;
  }else panel.innerHTML=`<div class="message">det(A) = 0 · rango(A) = ${report.rank_A} · rango([A|B]) = ${report.rank_augmented}</div><p>${report.status==="inconsistent"?"Una fila de la forma 0 = c, con c ≠ 0, demuestra la incompatibilidad.":"La familia se verifica con A·Xₚ = B y A·v = 0 para cada dirección libre."}</p>`;
}

function activateTab(name){
  document.querySelectorAll("[role=tab]").forEach(tab=>tab.setAttribute("aria-selected",String(tab.dataset.tab===name)));
  document.querySelectorAll(".tab-panel").forEach(panel=>panel.classList.toggle("hidden",panel.id!==`tab-${name}`));
}

function download(filename,data){
  if(!data)return;const blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"}),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=filename;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}

document.addEventListener("DOMContentLoaded",init);
