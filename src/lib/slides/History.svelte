<script>
    import Timeline from "$lib/Timeline.svelte";
    import Architectures from "$lib/Architectures.svelte";

    let hoverModel = null;
    let lockedModel = null;

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

    $: displayModel = lockedModel || hoverModel;

    function clearSelection() {
        if (lockedModel) {
            lockedModel = null;
            hoverModel = null;
        }
    }
</script>

<!--
    A ideia é: qualquer clique dentro de `.app-wrapper` dispara clearSelection()
    EXCETO os cliques nos círculos da timeline, porque lá chamamos event.stopPropagation()
    antes de dispatch("select").
  -->
<div class="app-wrapper" on:click={clearSelection} aria-hidden="true">
    <div class="center">
        <Architectures model={displayModel} />
    </div>

    <div class="right">
        <Timeline on:hover={handleHover} on:select={handleSelect} />
    </div>
</div>

<style>
    .app-wrapper {
        width: 100%;
        height: 100vh;
        display: flex;
        height: 100%;
        box-sizing: border-box;
    }
    .center {
        width: 60%;
        padding: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #fff;
        box-sizing: border-box;
    }
    .right {
        width: 20%;
        padding: 1rem;
        background: #fafafa;
        border-left: 1px solid #ddd;
        box-sizing: border-box;
        overflow-y: auto;
    }
</style>
