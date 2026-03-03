<template>
  <div>
    <AppHeader />
    <CartDrawer />
    <main>
      <slot />
    </main>
    <AppFooter />

    <!-- ═══════════════════════════════════════════════
         REWARDS — fixed left tab, visible on every page
         Matches design: yellow pill peaking from left edge,
         star icon + vertical "Rewards" text
    ═══════════════════════════════════════════════ -->
    <div class="rewards-float">
      <svg
        class="w-3.5 h-3.5 text-black shrink-0"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0
             00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0
             00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1
             1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1
             1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0
             00.951-.69l1.07-3.292z"
        />
      </svg>
      <span class="rewards-text">Rewards</span>
    </div>
  </div>
</template>

<style>
/* Fixed Rewards tab — left edge, vertically centred */
.rewards-float {
  position: fixed;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 40;
  background-color: #f5c518;        /* primary yellow */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 10px 8px 12px;
  cursor: pointer;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
  transition: background-color 0.15s;
}
.rewards-float:hover {
  background-color: #d4a017;
}

/* Vertical text — bottom-to-top */
.rewards-text {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #000;
  writing-mode: vertical-rl;
  text-orientation: mixed;
  transform: rotate(180deg);
}
</style>
