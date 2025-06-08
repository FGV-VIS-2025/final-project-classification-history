<script>
  import { createEventDispatcher } from "svelte";

  // Components
  import Timeline from "$lib/components/Timeline.svelte";
  import Architectures from "$lib/components/Architectures.svelte";

  const dispatch = createEventDispatcher();

  let hoverModel = null;
  let lockedModel = null;
  $: displayModel = lockedModel || hoverModel;

  function handleHover(event) {
    if (lockedModel) return;
    hoverModel = event.detail;
  }
  function handleSelect(event) {
    const clicked = event.detail;
    if (!clicked) return;
    if (lockedModel && lockedModel.name === clicked.name) {
      lockedModel = null;
      hoverModel = null;
    } else {
      lockedModel = clicked;
    }
  }

  function handleReadyLegend(event) {
    dispatch("readyLegend", {
      categories: event.detail.categories,
      colorScale: event.detail.colorScale,
    });
  }

  function clearSelection() {
    if (lockedModel) {
      lockedModel = null;
      hoverModel = null;
    }
  }
</script>

<div class="app-wrapper" on:click={clearSelection} aria-hidden="true">
  <div class="center">
    <Architectures model={displayModel} />
  </div>

  <div class="right">
    <Timeline
      on:readyLegend={handleReadyLegend}
      on:hover={handleHover}
      on:select={handleSelect}
    />
  </div>
</div>

<style>
  .app-wrapper {
    width: 100%;
    height: 100%;
    display: flex;
    box-sizing: border-box;
  }
  .center {
    width: 60%;
    height: 100%;
    padding: 1rem;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
  }
  .right {
    width: 40%;
    height: 100%;
    padding: 1rem;
    background: #fafafa;
    border-left: 1px solid #ddd;
    box-sizing: border-box;
    overflow-y: auto;
  }
</style>
