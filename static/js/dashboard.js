/**
 * Lógica do Dashboard ESG
 */

document.addEventListener('DOMContentLoaded', async () => {
    if (!localStorage.getItem('esg_token')) {
        window.location.href = 'login.html';
        return;
    }
    configurarSidebar();
    await carregarDashboardCompleto();
});

function logout() {
    localStorage.removeItem('esg_token');
    window.location.href = 'login.html';
}

async function carregarDashboardCompleto() {
    console.log("🔄 Atualizando Dashboard...");
    await Promise.all([
        carregarPerfilUsuario(),
        carregarDadosEmissoes(),
        carregarDadosResiduos(),
        carregarDadosAgua(),
        carregarDadosGerais()
    ]);
}

async function carregarPerfilUsuario() {
    try {
        const user = await API.getMe();
        const elEmpresa = document.querySelector('.user-profile span');
        const elAvatar = document.querySelector('.user-profile .avatar');
        if (elEmpresa) elEmpresa.innerText = user.nome_empresa;
        if (elAvatar) elAvatar.innerText = user.nome_empresa.charAt(0).toUpperCase();
    } catch (e) { console.error("Erro ao carregar perfil:", e); }
}

async function carregarDadosEmissoes() {
    try {
        const dados = await API.getHistoricoEmissoes();
        let s1 = 0, s2 = 0, s3 = 0, total = 0;
        let qCO2 = 0, qCH4 = 0, qN2O = 0;

        dados.forEach(item => {
            s1 += item.escopo1 || 0;
            s2 += item.escopo2 || 0;
            s3 += item.escopo3 || 0;
            total += item.total || 0;
            qCO2 += item.total_co2 || 0;
            qCH4 += item.total_ch4 || 0;
            qN2O += item.total_n2o || 0;
        });

        const totalTon = (total / 1000).toFixed(3);
        const elTotal = document.getElementById('total-emissoes-display');
        if (elTotal) elTotal.innerText = totalTon + " t";
        
        const elRegistros = document.getElementById('qtd-registros-display');
        if (elRegistros) elRegistros.innerText = dados.length + " registros";

        atualizarGraficoEmissoes(s1, s2, s3);
        atualizarGraficoQuimico(qCO2, qCH4, qN2O);
    } catch (error) {
        console.error("Erro Emissões:", error);
    }
}

async function carregarDadosResiduos() {
    try {
        const dados = await API.getHistoricoResiduos();
        let totalKg = 0, pesoReciclado = 0, pesoAterro = 0, pesoReciclagemPura = 0, pesoCompostagem = 0;

        dados.forEach(item => {
            const peso = item.peso_kg || 0;
            totalKg += peso;
            const destino = (item.destino || "").toLowerCase().trim();

            if (destino === 'reciclagem') {
                pesoReciclagemPura += peso;
                pesoReciclado += peso;
            } else if (destino === 'compostagem') {
                pesoCompostagem += peso;
                pesoReciclado += peso;
            } else {
                pesoAterro += peso;
            }
        });

        const taxa = totalKg > 0 ? ((pesoReciclado / totalKg) * 100).toFixed(1) : 0;
        const elRecic = document.getElementById('reciclagem-display');
        if (elRecic) elRecic.innerText = taxa + "%";

        const elResTotal = document.getElementById('residuos-total-display');
        if (elResTotal) elResTotal.innerText = totalKg + " kg processados";

        atualizarGraficoResiduos(pesoAterro, pesoReciclagemPura, pesoCompostagem);
    } catch (error) {
        console.error("Erro Resíduos:", error);
    }
}

async function carregarDadosAgua() {
    try {
        const dados = await API.getHistoricoAgua();
        let totalM3 = 0, totalCusto = 0;
        dados.forEach(item => {
            totalM3 += item.consumo_m3;
            totalCusto += item.custo_estimado;
        });
        
        const elAgua = document.getElementById('agua-display');
        if (elAgua) elAgua.innerText = totalM3.toFixed(1) + " m³";
        
        const elCusto = document.getElementById('agua-custo-display');
        if (elCusto) elCusto.innerText = "Custo: R$ " + totalCusto.toFixed(2);
    } catch (error) {
        console.error("Erro Água:", error);
    }
}

async function carregarDadosGerais() {
    // Aqui podemos carregar métricas sociais e de governança para o dashboard
    try {
        const social = await API.getHistoricoMetricas('social');
        const gov = await API.getHistoricoMetricas('governanca');
        
        // Exemplo: atualizar score ou indicadores específicos se existirem elementos no HTML
        console.log("Métricas Sociais:", social);
        console.log("Métricas Governança:", gov);
    } catch (e) { console.error(e); }
}

// --- Funções de Gráfico (Wrappers para Chart.js) ---

function destroyExistingChart(canvasId) {
    const existing = Chart.getChart(canvasId);
    if (existing) existing.destroy();
}

function atualizarGraficoQuimico(co2, ch4, n2o) {
    const canvasId = 'graficoQuimico';
    const canvas = document.getElementById(canvasId);
    if (!canvas || (co2 + ch4 + n2o === 0)) return;

    destroyExistingChart(canvasId);

    new Chart(canvas.getContext('2d'), {
        type: 'polarArea',
        data: {
            labels: ['CO₂', 'CH₄', 'N₂O'],
            datasets: [{
                data: [co2, ch4, n2o],
                backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 206, 86, 0.6)', 'rgba(153, 102, 255, 0.6)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'right' } }
        }
    });
}

function atualizarGraficoEmissoes(s1, s2, s3) {
    const canvasId = 'graficoEmissoes';
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    destroyExistingChart(canvasId);

    new Chart(canvas.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Escopo 1', 'Escopo 2', 'Escopo 3'],
            datasets: [{
                data: [s1, s2, s3],
                backgroundColor: ['#C62828', '#FF9800', '#4DB6AC'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function atualizarGraficoResiduos(aterro, reciclagem, compostagem) {
    const canvasId = 'graficoResiduos';
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    destroyExistingChart(canvasId);

    new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels: ['Aterro', 'Reciclagem', 'Compostagem'],
            datasets: [{
                label: 'Peso (kg)',
                data: [aterro, reciclagem, compostagem],
                backgroundColor: ['#5d4037', '#4CAF50', '#8BC34A'],
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true } }
        }
    });
}

// --- UI Helpers ---

function abrirModal(id) { document.getElementById(id).style.display = "block"; }
function fecharModal(id) { document.getElementById(id).style.display = "none"; }

function configurarSidebar() {
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menu-toggle');
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            const icon = menuToggle.querySelector('.material-icons');
            icon.textContent = sidebar.classList.contains('active') ? 'close' : 'menu';
        });
    }
}

// --- Funções de Ação (Salvar) ---

async function salvarEmissoes() {
    const payload = {
        consumo_gasolina_l: parseFloat(document.getElementById('gasolina').value || 0),
        consumo_diesel_l: parseFloat(document.getElementById('diesel').value || 0),
        consumo_eletricidade_kwh: parseFloat(document.getElementById('energia').value || 0),
        viagens_km: parseFloat(document.getElementById('viagens').value || 0)
    };
    try {
        await API.salvarEmissoes(payload);
        alert("Emissões salvas!");
        location.reload();
    } catch (e) { alert(e.message); }
}

async function salvarResiduos() {
    const payload = {
        tipo: document.getElementById('tipoResiduo').value,
        destino: document.getElementById('destinoResiduo').value,
        peso_kg: parseFloat(document.getElementById('pesoResiduo').value || 0)
    };
    try {
        await API.salvarResiduos(payload);
        alert("Resíduos salvos!");
        location.reload();
    } catch (e) { alert(e.message); }
}

async function salvarAgua() {
    const payload = {
        consumo_m3: parseFloat(document.getElementById('consumoAgua').value || 0),
        origem: document.getElementById('origemAgua').value,
        preco_m3: 5.5
    };
    try {
        await API.salvarAgua(payload);
        alert("Consumo de água salvo!");
        location.reload();
    } catch (e) { alert(e.message); }
}
