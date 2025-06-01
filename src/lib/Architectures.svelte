<script>
    import data from "../data/models_timeline.json";
    import { onMount } from "svelte";
  
    const filenameMap = {
      "Support Vector Machine":      "svm_arch.png",
      "Random Forest":               "rf_arch.png",
      "Gradient Boosting Machine":   "gbm_arch.png",
      "AlexNet":                     "alexnet_arch.png",
      "VGG":                         "vgg_arch.png",
      "ResNet":                      "resnet_arch.png",
      "XGBoost":                     "xgboost_arch.png",
      "BERT":                        "bert_arch.png",
      "ViT":    "vit_arch.png",
      "Swin Transformer":            "swin_arch.png"
    };
  
    let items = [];
  
    onMount(() => {
      items = data.map(d => {
        const filename = filenameMap[d.name] || "not_found.png";
  
        return {
          name: d.name,
          imgPath: `/architectures/${filename}`
        };
      });
    });
  
    let showModal = false;
    let activeImage = "";
    let activeLabel = "";
  
    function openModal(item) {
      activeImage = item.imgPath;
      activeLabel = item.name;
      showModal = true;
    }
  
    function closeModal() {
      showModal = false;
      activeImage = "";
      activeLabel = "";
    }
  </script>
  
  <style>
    .grid-container {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
      gap: 1rem;
      margin: 2rem 0;
    }
  
    .thumb {
      cursor: pointer;
      border: 1px solid #ddd;
      border-radius: 4px;
      overflow: hidden;
      background: #f9f9f9;
      transition: transform 0.15s ease;
      role: button;
    }
    .thumb:hover {
      transform: scale(1.05);
    }
    .thumb img {
      width: 100%;
      height: auto;
      display: block;
    }
    .thumb-label {
      text-align: center;
      font-size: 0.85rem;
      padding: 4px 0;
      background: #fff;
    }
  
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.6);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 100;
    }
  
    .modal-content {
      background: #fff;
      border-radius: 6px;
      max-width: 90%;
      max-height: 90%;
      overflow: auto;
      position: relative;
      padding: 1rem;
    }
  
    .modal-content img {
      display: block;
      max-width: 100%;
      height: auto;
      margin: 0 auto;
    }
  
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }
    .modal-header h3 {
      margin: 0;
      font-size: 1.2rem;
    }
    .modal-close {
      cursor: pointer;
      font-size: 1.2rem;
      border: none;
      background: transparent;
    }
  </style>
  
  <div>
    <h2 style="text-align: center; margin-top: 2rem;">
      Arquiteturas dos Modelos
    </h2>
  
    <div class="grid-container">
      {#each items as item}
        <div class="thumb" role="button" on:click={() => openModal(item)}>
          <img src={item.imgPath} alt={`Arquitetura ${item.name}`} />
          <div class="thumb-label">{item.name}</div>
        </div>
      {/each}
    </div>
  
    {#if showModal}
      <div class="modal-overlay" on:click={() => closeModal()}>
        <div class="modal-content" on:click|stopPropagation>
          <div class="modal-header">
            <h3>{activeLabel}</h3>
            <button class="modal-close" aria-label="Fechar" on:click={() => closeModal()}>
              ✕
            </button>
          </div>
          <img src={activeImage} alt={activeLabel} />
        </div>
      </div>
    {/if}
  </div>
  