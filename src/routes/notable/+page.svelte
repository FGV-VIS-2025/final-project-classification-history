<!-- src/routes/notable/+page.svelte -->
<script lang="ts">
  import Futurework from '$lib/Futureworks.svelte';
  
</script>

<style>
  main {
    display: flex;
    gap: 2rem;
    padding: 1rem;
  }

  .description {
    flex: 0 0 30%;
    font-family: sans-serif;
    line-height: 1.5;
  }

  h1 {
    margin-bottom: 0.5rem;
    font-family: sans-serif;
  }
</style>

<main>
  <div class="description">
    <h1>Notable AI Models</h1>
    <p>
      Este gráfico mostra a evolução do esforço computacional (em FLOPs) necessário para treinar
      modelos de IA ao longo do tempo. O eixo X representa o ano de publicação de cada modelo e o
      eixo Y (escala logarítmica) exibe o número de FLOPs.
    </p>
    <p>
      A região sombreada marca a “Deep Learning Era” (a partir de 2010), quando houve um aumento
      expressivo no uso de computação para treinar redes neurais. Ao passar o mouse sobre cada
      ponto, aparece um tooltip próximo ao cursor mostrando o nome do modelo, o ano e a quantidade
      de FLOPs.
    </p>
  </div>

  <!-- Em vez de todo o código do gráfico aqui, apenas chamamos o componente -->
  <Futurework />
</main>
