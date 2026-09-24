const root = document.documentElement;
const themeToggle = document.getElementById("themeToggle");
const themeText = document.getElementById("themeText");
const themeIcon = document.getElementById("themeIcon");

function setTheme(theme){
  root.setAttribute("data-theme", theme);
  localStorage.setItem("jobderv-theme", theme);
  themeText.textContent = theme === "dark" ? "Light mode" : "Dark mode";
  themeIcon.textContent = theme === "dark" ? "☀" : "☾";
  updateCharts();
}
setTheme(localStorage.getItem("jobderv-theme") || "light");
themeToggle.addEventListener("click",()=>setTheme(root.getAttribute("data-theme")==="dark"?"light":"dark"));

document.getElementById("mobileMenu").addEventListener("click",()=>{
  document.querySelector(".sidebar").classList.toggle("open");
});

const toast = document.getElementById("toast");
function showToast(message){
  toast.textContent=message; toast.classList.add("show");
  setTimeout(()=>toast.classList.remove("show"),1800);
}
document.querySelectorAll(".save-btn").forEach(btn=>btn.addEventListener("click",()=>{
  btn.textContent = btn.textContent === "Guardada ✓" ? "Guardar" : "Guardada ✓";
  showToast(btn.textContent.includes("✓") ? "Vaga guardada." : "Vaga removida.");
}));
document.querySelectorAll(".apply-btn").forEach(btn=>btn.addEventListener("click",()=>showToast("Aqui vamos abrir os detalhes da vaga.")));

document.getElementById("searchBtn").addEventListener("click",()=>{
  const q=document.getElementById("jobSearch").value.trim().toLowerCase();
  document.querySelectorAll(".job-card").forEach(card=>{
    card.style.display=!q || card.dataset.title.includes(q) ? "" : "none";
  });
});

let applicationsChart,statusChart;
function chartColors(){
  const dark=root.getAttribute("data-theme")==="dark";
  return {text:dark?"#9aaac0":"#667085", grid:dark?"#26364d":"#e8edf3"};
}
function updateCharts(){
  if(!window.Chart) return;
  const c=chartColors();
  if(applicationsChart){applicationsChart.options.scales.x.ticks.color=c.text;applicationsChart.options.scales.y.ticks.color=c.text;applicationsChart.options.scales.y.grid.color=c.grid;applicationsChart.update();}
  if(statusChart){statusChart.options.plugins.legend.labels.color=c.text;statusChart.update();}
}
function initCharts(){
  const c=chartColors();
  applicationsChart=new Chart(document.getElementById("applicationsChart"),{
    type:"bar",
    data:{labels:["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"],datasets:[
      {label:"Enviadas",data:[5,9,7,12,15,10,13],backgroundColor:"#1683f3",borderRadius:3},
      {label:"Respostas",data:[2,4,3,5,7,4,6],backgroundColor:"#24b47e",borderRadius:3}
    ]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{
      x:{grid:{display:false},ticks:{color:c.text,font:{size:9}}},
      y:{beginAtZero:true,grid:{color:c.grid},ticks:{color:c.text,font:{size:9}}}
    }}
  });
  statusChart=new Chart(document.getElementById("statusChart"),{
    type:"doughnut",
    data:{labels:["Enviadas","Entrevista","Resposta","Recusadas"],datasets:[{data:[60,20,15,5],backgroundColor:["#1683f3","#24b47e","#f5a524","#ef4444"],borderWidth:0}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:"62%",plugins:{legend:{display:false}}}
  });
}
initCharts();
