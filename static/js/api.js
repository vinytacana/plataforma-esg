/**
 * Módulo para centralizar chamadas à API da Calculadora ESG
 */

const API = {
    async fetchJSON(url, options = {}) {
        const token = localStorage.getItem('esg_token');
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(url, {
            ...options,
            headers: headers,
        });

        if (response.status === 401) {
            localStorage.removeItem('esg_token');
            window.location.href = 'login.html';
            return;
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro na requisição');
        }
        return response.json();
    },

    // Emissões
    getHistoricoEmissoes() {
        return this.fetchJSON('/emissoes/historico');
    },
    salvarEmissoes(payload) {
        return this.fetchJSON('/emissoes/calcular', {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    },

    // Resíduos
    getHistoricoResiduos() {
        return this.fetchJSON('/residuos/historico');
    },
    salvarResiduos(payload) {
        return this.fetchJSON('/residuos/calcular', {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    },

    // Água
    getHistoricoAgua() {
        return this.fetchJSON('/agua/historico');
    },
    salvarAgua(payload) {
        return this.fetchJSON('/agua/registrar', {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    },

    // Métricas Genéricas (Social/Governança)
    getHistoricoMetricas(categoria = null) {
        let url = '/metricas/historico';
        if (categoria) url += `?categoria=${categoria}`;
        return this.fetchJSON(url);
    },
    salvarMetrica(payload) {
        return this.fetchJSON('/metricas/registrar', {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    },

    getMe() {
        return this.fetchJSON('/usuarios/me');
    }
};
