<script>
    /** @type {number[] | null} */
    export let probabilities = null; // Array de 10 probabilidades
    /** @type {number | null} */
    export let predictedClass = null;
  
    const labels = Array.from({ length: 10 }, (_, i) => i.toString());
  
    /**
     * @param {number} prob
     * @returns {string}
     */
    function getBarHeight(prob) {
      return `${Math.max(0, Math.min(100, prob * 100))}%`;
    }
  </script>
  
  <div class="prediction-chart-container">
    {#if probabilities && probabilities.length === 10}
      <div class="bars">
        {#each probabilities as prob, i}
          <div class="bar-wrapper" title={`Classe ${labels[i]}: ${(prob * 100).toFixed(2)}%`}>
            <div
              class="bar"
              class:predicted={i === predictedClass}
              style:height={getBarHeight(prob)}
            >
              <span class="prob-value">{(prob * 100).toFixed(1)}%</span>
            </div>
            <div class="label">{labels[i]}</div>
          </div>
        {/each}
      </div>
      {#if predictedClass !== null}
        <p class="result">Predição: <strong>{predictedClass}</strong></p>
      {/if}
    {:else}
      <p>Aguardando predição...</p>
    {/if}
  </div>
  
  <style>
    .prediction-chart-container {
      font-family: sans-serif;
      padding: 15px;
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      background-color: #f9fafb;
      box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .bars {
      display: flex;
      justify-content: space-around;
      align-items: flex-end;
      height: 150px; /* Aumentado para melhor visualização dos valores */
      border-bottom: 1px solid #d1d5db;
      margin-bottom: 12px;
    }
    .bar-wrapper {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 9%;
    }
    .bar {
      width: 100%;
      background-color: #60a5fa; /* Azul mais suave */
      transition: height 0.3s ease-out, background-color 0.3s;
      display: flex;
      align-items: flex-end;
      justify-content: center;
      overflow: hidden;
      border-radius: 3px 3px 0 0; /* Bordas arredondadas no topo */
    }
    .bar.predicted {
      background-color: #3b82f6; /* Azul mais forte para predição */
    }
    .prob-value {
      font-size: 0.75em; /* Ligeiramente maior */
      color: white;
      padding-bottom: 3px;
      font-weight: 500;
       /* Removido rotação para simplicidade, pode ser adicionado se necessário */
    }
    .label {
      margin-top: 6px;
      font-size: 0.9em;
      color: #4b5563;
    }
    .result {
      text-align: center;
      font-size: 1.25em;
      margin-top: 15px;
      color: #1f2937;
    }
  </style>