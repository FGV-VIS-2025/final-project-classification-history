<script>
    /**
     * Este componente simplesmente mostra:
     * - Se `model === null`: placeholder "Hover over models"
     * - Se `model` existe: nome, imagem da arquitetura, autores, descrição e link para o paper
     */
    export let model = null;
  </script>
  
  <style>
    .center-box {
      width: 100%;
      height: 100%;
      border: 2px dashed #aaa;
      border-radius: 8px;
      background: #f5f5f5;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      box-sizing: border-box;
      text-align: center;
    }
  
    .center-box img {
      max-width: 80%;
      height: auto;
      margin: 1rem 0;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
      border-radius: 4px;
    }
  
    .placeholder-text {
      font-size: 1.2rem;
      color: #666;
      font-style: italic;
    }
  
    .model-name {
      margin: 0;
      font-size: 1.4rem;
      font-weight: bold;
      color: #333;
    }
  
    .model-authors,
    .model-description {
      margin: 0.5rem 0;
      font-size: 0.95rem;
      color: #444;
    }
  
    .model-link {
      margin-top: 0.5rem;
      font-size: 0.9rem;
      color: #0366d6;
      text-decoration: none;
    }
    .model-link:hover {
      text-decoration: underline;
    }
  </style>
  
  <div class="center-box">
    {#if model}
      <h3 class="model-name">{model.name}</h3>
      <img src={model.imgPath} alt={model.name} />
      <p class="model-authors"><strong>Authors:</strong> {model.authors}</p>
      <p class="model-description">{model.description}</p>
      {#if model.paper}
        <a
          class="model-link"
          href={model.paper}
          target="_blank"
          rel="noopener noreferrer"
        >
          Read paper
        </a>
      {/if}
    {:else}
      <p class="placeholder-text">Hover over models</p>
    {/if}
  </div>