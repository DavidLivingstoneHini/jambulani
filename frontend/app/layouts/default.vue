<template>
  <div>
    <AppHeader />
    <CartDrawer />
    <main>
      <slot />
    </main>
    <AppFooter />

    <Rewards />
  </div>
</template>