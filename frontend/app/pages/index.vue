<template>
  <div>
    <!-- Hero Banner -->
    <section
      class="relative overflow-hidden bg-gray-900"
      style="height: 340px;"
    >
      <div
        class="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style="background-image: url('/assets/images/hero-banner.jpg'); background-color: #1a1a2e;"
      />
      <div class="absolute inset-0 bg-black/35" />

      <div class="relative z-10 h-full flex items-center">
        <div class="px-1 md:px-[34px] w-full">
          <h1 class="font-display font-bold text-white text-[30px] md:text-[52px] leading-[1.05] uppercase drop-shadow-lg">
            Your favorite customized<br>
            <span class="text-primary">Club Jerseys.</span>
          </h1>
          <NuxtLink
            to="/products"
            class="inline-block mt-5 bg-primary text-black font-display font-bold uppercase
                   tracking-wider px-5 py-2.5 text-[13px] hover:bg-primary-600 transition-colors shadow"
          >
            Shop Now
          </NuxtLink>
        </div>
      </div>

      <div class="absolute bottom-4 left-1 md:left-[34px] flex items-center gap-1.5 z-10">
        <span class="block w-7 h-1.5 bg-primary" />
        <span class="block w-2.5 h-1.5 bg-white/40 cursor-pointer" />
        <span class="block w-2.5 h-1.5 bg-white/40 cursor-pointer" />
      </div>
    </section>

    <div class="px-1 md:px-[34px]">
      <!-- Feature Highlights -->
    <section class="pt-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">

        <div class="overflow-hidden bg-[#fdf9e0] p-5 pb-3">
          <div class="skewed bg-primary p-2 w-fit mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 22 16">
              <path d="M19 4H16V0H2C0.9 0 0 0.9 0 2V13H2C2 14.66 3.34 16 5 16C6.66 16 8 14.66 8 13H14C14 14.66 15.34 16 17 16C18.66 16 20 14.66 20 13H22V8L19 4ZM5 14.5C4.17 14.5 3.5 13.83 3.5 13C3.5 12.17 4.17 11.5 5 11.5C5.83 11.5 6.5 12.17 6.5 13C6.5 13.83 5.83 14.5 5 14.5ZM18.5 5.5L20.46 8H16V5.5H18.5ZM17 14.5C16.17 14.5 15.5 13.83 15.5 13C15.5 12.17 16.17 11.5 17 11.5C17.83 11.5 18.5 12.17 18.5 13C18.5 13.83 17.83 14.5 17 14.5Z" fill="white" />
            </svg>
          </div>
          <p class="font-semibold text-[12px] mb-1 inline-block">Secure Shipping</p>
          <p class="text-[10px]">on all orders</p>
        </div>

        <div class="overflow-hidden bg-[#fdf9e0] p-5 pb-3">
          <div class="skewed bg-primary p-2 w-fit mb-4">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17.01 12.38C15.78 12.38 14.59 12.18 13.48 11.82C13.13 11.7 12.74 11.79 12.47 12.06L10.9 14.03C8.07 12.68 5.42 10.13 4.01 7.2L5.96 5.54C6.23 5.26 6.31 4.87 6.2 4.52C5.83 3.41 5.64 2.22 5.64 0.99C5.64 0.45 5.19 0 4.65 0H1.19C0.65 0 0 0.24 0 0.99C0 10.28 7.73 18 17.01 18C17.72 18 18 17.37 18 16.82V13.37C18 12.83 17.55 12.38 17.01 12.38Z" fill="white" />
            </svg>
          </div>
          <p class="font-semibold text-[12px] mb-1 inline-block">Telephone</p>
          <p class="text-[10px]">+1 (25) 01 7880</p>
        </div>

        <div class="overflow-hidden bg-[#fdf9e0] p-5 pb-3">
          <div class="skewed bg-primary p-2 w-fit mb-4">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M14.582 11.9842C14.3338 11.8602 13.1099 11.2601 12.8818 11.178C12.6537 11.095 12.4879 11.054 12.3221 11.3021C12.1563 11.5491 11.6791 12.1082 11.5334 12.2733C11.3887 12.4383 11.243 12.4583 10.9948 12.3343C10.2613 12.0436 9.58432 11.628 8.99417 11.106C8.44988 10.6052 7.98325 10.0268 7.60952 9.38964C7.46483 9.14158 7.59445 9.00755 7.71905 8.88452C7.83058 8.7735 7.96824 8.59546 8.09184 8.45043C8.1942 8.32522 8.27811 8.18612 8.34103 8.03733C8.37414 7.96896 8.38956 7.89343 8.38587 7.81762C8.38219 7.7418 8.35952 7.66811 8.31993 7.60324C8.25763 7.47921 7.76025 6.25993 7.55325 5.76382C7.35128 5.28172 7.1463 5.34673 6.99256 5.33873C6.84787 5.33173 6.68207 5.32973 6.51628 5.32973C6.39016 5.33323 6.26613 5.36267 6.15199 5.4162C6.03786 5.46974 5.93609 5.54621 5.85309 5.6408C5.57177 5.90599 5.34901 6.22661 5.19902 6.58222C5.04903 6.93783 4.97509 7.32064 4.98191 7.70626C5.0626 8.6407 5.41567 9.53135 5.99779 10.2688C7.06483 11.8612 8.52957 13.15 10.2482 14.0087C10.7118 14.2069 11.1853 14.3812 11.667 14.5308C12.1748 14.6842 12.7116 14.7175 13.2345 14.6278C13.5809 14.558 13.9089 14.4174 14.1979 14.2149C14.4869 14.0124 14.7306 13.7525 14.9136 13.4515C15.0768 13.0814 15.1271 12.6717 15.0583 12.2733C14.997 12.1693 14.8312 12.1082 14.582 11.9842ZM17.086 2.90318C15.3778 1.20315 13.1071 0.178983 10.6967 0.0213433C8.28639 -0.136297 5.90062 0.583338 3.9836 2.04627C2.06658 3.5092 0.748953 5.61573 0.276019 7.97369C-0.196916 10.3316 0.207076 12.7803 1.41278 14.8639L0 20L5.27934 18.6227C6.7395 19.4141 8.37558 19.8288 10.0382 19.829H10.0422C12.0117 19.828 13.9368 19.2459 15.5742 18.1563C17.2115 17.0667 18.4877 15.5185 19.2415 13.7072C19.9953 11.8959 20.1928 9.90288 19.8092 7.9799C19.4255 6.05692 18.4779 4.29028 17.086 2.90317V2.90318ZM14.4403 16.8953C13.1221 17.7178 11.5979 18.1542 10.0422 18.1546H10.0382C8.55597 18.1545 7.10107 17.7575 5.82596 17.0053L5.52351 16.8273L2.39047 17.6455L3.22649 14.6048L3.03055 14.2927C2.16092 12.9123 1.72205 11.3061 1.76943 9.67735C1.81681 8.0486 2.34832 6.47042 3.29674 5.14236C4.24517 3.81429 5.56791 2.796 7.09771 2.21624C8.62752 1.63649 10.2957 1.5213 11.8912 1.88525C13.4868 2.2492 14.9381 3.07594 16.0617 4.26093C17.1852 5.44593 17.9305 6.93595 18.2034 8.54258C18.4762 10.1492 18.2643 11.8003 17.5945 13.2871C16.9247 14.7738 15.827 16.0295 14.4403 16.8953Z" fill="white" />
            </svg>
          </div>
          <p class="font-semibold text-[12px] mb-1 inline-block">Chat WhatsApp</p>
          <p class="text-[10px]">Mon – Fri: 9:00 – 21:00 · Sat – Sun: 9:00 – 17:00</p>
        </div>

        <div class="overflow-hidden bg-[#fdf9e0] p-5 pb-3">
          <div class="skewed bg-primary p-2 w-fit mb-4">
            <svg width="22" height="21" viewBox="0 0 22 21" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 10.5L19.56 7.71L19.9 4.02L16.29 3.2L14.4 0L11 1.46L7.6 0L5.71 3.19L2.1 4L2.44 7.7L0 10.5L2.44 13.29L2.1 16.99L5.71 17.81L7.6 21L11 19.53L14.4 20.99L16.29 17.8L19.9 16.98L19.56 13.29L22 10.5ZM9.09 15.22L5.29 11.41L6.77 9.93L9.09 12.26L14.94 6.39L16.42 7.87L9.09 15.22Z" fill="white" />
            </svg>
          </div>
          <p class="font-semibold text-[12px] mb-1 inline-block">Quality Guarantee</p>
          <p class="text-[10px]">Verified Purchase Reviews</p>
        </div>

      </div>
    </section>

    <!-- Featured Products -->
    <section class="px-4 pt-10 pb-6">
      <div class="flex items-center justify-between mb-5">
        <h2 class="section-title mb-0">MOST POPULAR T-SHIRTS</h2>
        <div class="flex gap-0">
          <button
            class="border border-gray-300 p-2 hover:bg-gray-100 transition-colors"
            aria-label="Previous"
            @click="prevPage"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button
            class="border border-gray-300 p-2 hover:bg-gray-100 transition-colors"
            aria-label="Next"
            @click="nextPage"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <div v-if="featuredPending" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div v-for="n in 6" :key="n" class="animate-pulse">
          <div class="aspect-square bg-gray-200 mb-2" />
          <div class="h-3 bg-gray-200 mb-1 rounded" />
          <div class="h-3 w-2/3 bg-gray-200 rounded" />
        </div>
      </div>

      <div v-else-if="visibleFeatured.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <ProductCard
          v-for="product in visibleFeatured"
          :key="product.id"
          :product="product"
        />
      </div>

      <p v-else class="text-center py-10 text-gray-400 font-body text-sm">
        No featured products yet
      </p>
    </section>


    <!-- Country Leagues -->
    <section class="px-4 pt-8 pb-6">
      <h2 class="section-title">COUNTRY LEAGUES</h2>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
        <NuxtLink
          v-for="league in staticLeagues"
          :key="league.slug"
          :to="`/products?league=${league.slug}`"
          class="relative overflow-hidden block cursor-pointer group"
          style="aspect-ratio: 1 / 1;"
        >
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat
                   transition-transform duration-500 group-hover:scale-105"
            :style="`background-image: url('/assets/images/leagues/${league.slug}.jpg');
                     background-color: ${league.color};`"
          />
          <div class="absolute inset-0 bg-black/20 group-hover:bg-black/35 transition-colors duration-300" />
          <span
            class="absolute bottom-0 inset-x-0 pb-2 pt-1.5 text-left text-black font-display
                   font-bold text-[11px] md:text-[12px] uppercase leading-tight px-2 z-10 bg-white/90"
          >
            {{ league.name }}
          </span>
        </NuxtLink>
      </div>
    </section>


    <!-- Other Collections -->
    <section class="pt-8 pb-10">
      <div class="flex items-start mb-3">
        <h2 class="mr-6 uppercase text-2xl font-bold">Other collections</h2>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-6">
        <NuxtLink
          v-for="col in staticCollections"
          :key="col.slug"
          :to="`/products?collection=${col.slug}`"
          class="bg-no-repeat bg-cover bg-center pt-40 block cursor-pointer"
          :style="`background-image: url('/assets/images/collections/${col.slug}.jpg'); background-color: ${col.color};`"
        >
          <div class="flex items-center justify-between bg-[#0000007d] backdrop-blur-sm">
            <small class="text-xs text-white font-medium pl-3">{{ col.name }}</small>
            <small class="bg-primary p-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 6 10">
                <path d="M5.64095 4.64463C5.83864 4.8403 5.83864 5.1597 5.64095 5.35537L1.60173 9.35316C1.28601 9.66564 0.75 9.442 0.75 8.99779L0.75 1.00221C0.75 0.557998 1.28601 0.334357 1.60173 0.646838L5.64095 4.64463Z" fill="#111112" />
              </svg>
            </small>
          </div>
        </NuxtLink>
      </div>
    </section>


    <!-- Personalization & Social Networks -->
    <section class="py-10 pb-14">
      <div class="grid md:grid-cols-2 grid-cols-1 gap-6 text-white">
        <div class="relative px-6 md:px-12 pt-52 pb-8">
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat"
            style="background-image: url('/assets/images/personalization.jpg'); background-color: #1a1a2e;"
          />
          <div class="absolute inset-0" style="background-color: rgba(0,0,0,0.5);" />
          <div class="relative z-10">
            <p class="uppercase text-lg font-bold mb-6">Personalization</p>
            <p class="font-light text-xs">Put a custom print on the football shirt of your choice with our Personalization service.</p>
            <p class="font-light text-xs mt-3">
              Tell us what name, what number and we put it. <b class="font-bold">FREE!!!</b>
            </p>
          </div>
        </div>

        <div class="relative px-6 md:px-12 pt-52 pb-8">
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat"
            style="background-image: url('/assets/images/social-networks.jpg'); background-color: #111827;"
          />
          <div class="absolute inset-0" style="background-color: rgba(0,0,0,0.5);" />
          <div class="relative z-10">
            <p class="uppercase text-lg font-bold mb-6">Social Networks</p>
            <p class="font-light text-xs">Share your shirts with us with the #CamisetasFutbolSpanish</p>
            <div class="flex items-center mt-3">
              <a href="#" aria-label="Facebook" class="bg-white py-2 px-3 mr-2 hover:opacity-80 transition-opacity">
                <svg width="9" height="18" viewBox="0 0 9 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M5.66764 17.4077V8.70281H8.07056L8.389 5.70307H5.66764L5.67172 4.20167C5.67172 3.41929 5.74606 3.00008 6.86978 3.00008H8.37198V0H5.96873C3.08203 0 2.06598 1.4552 2.06598 3.90238V5.70341H0.266602V8.70315H2.06598V17.4077H5.66764Z" fill="black" />
                </svg>
              </a>

              <a href="#" aria-label="Twitter" class="bg-white py-2 px-2 mr-2 hover:opacity-80 transition-opacity">
                <svg width="18" height="18" viewBox="0 0 18 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M8.32769 4.32321L8.36126 4.87685L7.80168 4.80906C5.7648 4.54919 3.98532 3.66789 2.47444 2.18776L1.73579 1.45334L1.54554 1.99568C1.14264 3.20464 1.40004 4.4814 2.23942 5.3401C2.68709 5.81464 2.58636 5.88243 1.81414 5.59997C1.54554 5.50958 1.31051 5.44178 1.28813 5.47568C1.20979 5.55477 1.47839 6.58295 1.69103 6.98971C1.98201 7.55464 2.57517 8.10828 3.22429 8.43594L3.77268 8.69581L3.12356 8.70711C2.49683 8.70711 2.47444 8.71841 2.54159 8.95568C2.76543 9.69009 3.64957 10.4697 4.63444 10.8087L5.32832 11.0459L4.72397 11.4075C3.82864 11.9272 2.77662 12.221 1.7246 12.2436C1.22098 12.2549 0.806885 12.3001 0.806885 12.334C0.806885 12.447 2.17227 13.0797 2.96688 13.3283C5.3507 14.0627 8.1822 13.7463 10.3086 12.4922C11.8195 11.5996 13.3304 9.82568 14.0354 8.10828C14.416 7.19308 14.7965 5.52088 14.7965 4.71867C14.7965 4.19893 14.83 4.13114 15.4568 3.50971C15.8261 3.14815 16.173 2.7527 16.2402 2.63971C16.3521 2.42503 16.3409 2.42503 15.7702 2.61711C14.8189 2.95607 14.6846 2.91088 15.1546 2.40244C15.5015 2.04088 15.9156 1.38555 15.9156 1.19347C15.9156 1.15958 15.7478 1.21607 15.5575 1.31776C15.3561 1.43075 14.9084 1.60023 14.5726 1.70192L13.9683 1.89399L13.4199 1.52114C13.1177 1.31776 12.6924 1.09179 12.4686 1.02399C11.8978 0.865812 11.0249 0.88841 10.5101 1.06919C9.1111 1.57763 8.22696 2.88828 8.32769 4.32321Z" fill="black" />
                </svg>
              </a>

              <a href="#" aria-label="Instagram" class="bg-white py-2 px-2 mr-2 hover:opacity-80 transition-opacity">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M5.48232 0.518231C6.39255 0.476809 6.6834 0.466675 9.00093 0.466675H8.99827C11.3165 0.466675 11.6063 0.476809 12.5165 0.518231C13.425 0.559832 14.0454 0.703655 14.5894 0.914679C15.1512 1.13246 15.6259 1.42402 16.1006 1.89869C16.5752 2.37301 16.8668 2.8491 17.0855 3.41035C17.2952 3.95293 17.4392 4.57303 17.4819 5.48148C17.5228 6.39171 17.5335 6.68256 17.5335 9.0001C17.5335 11.3176 17.5228 11.6078 17.4819 12.518C17.4392 13.4261 17.2952 14.0464 17.0855 14.5891C16.8668 15.1502 16.5752 15.6263 16.1006 16.1006C15.6264 16.5753 15.151 16.8676 14.59 17.0855C14.047 17.2965 13.4262 17.4404 12.5178 17.482C11.6075 17.5234 11.3176 17.5335 8.99986 17.5335C6.68251 17.5335 6.39184 17.5234 5.48161 17.482C4.57333 17.4404 3.95306 17.2965 3.41012 17.0855C2.84922 16.8676 2.37313 16.5753 1.89899 16.1006C1.4245 15.6263 1.13294 15.1502 0.914801 14.589C0.703955 14.0464 0.560132 13.4263 0.518353 12.5178C0.477108 11.6076 0.466797 11.3176 0.466797 9.0001C0.466797 6.68256 0.477464 6.39154 0.518175 5.4813C0.559064 4.57321 0.703066 3.95293 0.914624 3.41017C1.13329 2.8491 1.42485 2.37301 1.89952 1.89869C2.37384 1.4242 2.84993 1.13264 3.41118 0.914679C3.95377 0.703655 4.57386 0.559832 5.48232 0.518231ZM8.23541 2.00447C8.38405 2.00424 8.54396 2.00431 8.71652 2.00439L9.00093 2.00447C11.2794 2.00447 11.5494 2.01265 12.4491 2.05354C13.2812 2.09158 13.7327 2.2306 14.0335 2.34741C14.4317 2.50207 14.7157 2.68696 15.0142 2.98563C15.3128 3.2843 15.4977 3.56875 15.6527 3.96698C15.7695 4.26743 15.9087 4.71899 15.9466 5.55099C15.9875 6.45056 15.9964 6.72079 15.9964 8.99814C15.9964 11.2755 15.9875 11.5457 15.9466 12.4453C15.9086 13.2773 15.7695 13.7289 15.6527 14.0293C15.4981 14.4275 15.3128 14.7111 15.0142 15.0096C14.7155 15.3083 14.4319 15.4931 14.0335 15.6478C13.7331 15.7651 13.2812 15.9038 12.4491 15.9419C11.5496 15.9827 11.2794 15.9916 9.00093 15.9916C6.72233 15.9916 6.45228 15.9827 5.55272 15.9419C4.72071 15.9035 4.26915 15.7644 3.96817 15.6476C3.56994 15.493 3.28549 15.3081 2.98682 15.0094C2.68815 14.7107 2.50326 14.427 2.34824 14.0286C2.23144 13.7281 2.09224 13.2766 2.05437 12.4446C2.01348 11.545 2.0053 11.2748 2.0053 8.99601C2.0053 6.71723 2.01348 6.44843 2.05437 5.54886C2.09241 4.71685 2.23144 4.26529 2.34824 3.96449C2.50291 3.56626 2.68815 3.28182 2.98682 2.98315C3.28549 2.68448 3.56994 2.49959 3.96817 2.34456C4.26897 2.22723 4.72071 2.08856 5.55272 2.05034C6.33993 2.01478 6.645 2.00411 8.23541 2.00234V2.00447ZM12.532 4.44503C12.532 3.87951 12.9907 3.42137 13.556 3.42137C14.1213 3.42137 14.58 3.87969 14.58 4.44503C14.58 5.01037 14.1213 5.46904 13.556 5.46904C12.9907 5.46904 12.532 5.01037 12.532 4.44503ZM4.61866 9.0001C4.61866 6.57998 6.58082 4.61783 9.00093 4.61783C11.421 4.61783 13.3825 6.57998 13.3825 9.0001C13.3825 11.4202 11.421 13.3815 9.00093 13.3815C6.58082 13.3815 4.61866 11.4202 4.61866 9.0001ZM11.8454 9.0001C11.8454 7.42906 10.5718 6.15562 9.00093 6.15562C7.42989 6.15562 6.15646 7.42906 6.15646 9.0001C6.15646 10.571 7.42989 11.8446 9.00093 11.8446C10.5718 11.8446 11.8454 10.571 11.8454 9.0001Z" fill="black" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProductList } from '~/app/types'

const { apiFetch } = useApi()

const { data: featuredData, pending: featuredPending } = await useAsyncData(
  'featured-products',
  () => apiFetch<ProductList[]>('/products/featured/').catch(() => [] as ProductList[])
)
const featuredProducts = computed<ProductList[]>(() => featuredData.value ?? [])

const featuredOffset = ref(0)
const ITEMS_PER_PAGE = 6
const visibleFeatured = computed(() =>
  featuredProducts.value.slice(featuredOffset.value, featuredOffset.value + ITEMS_PER_PAGE)
)
function prevPage() {
  if (featuredOffset.value > 0) featuredOffset.value -= ITEMS_PER_PAGE
}
function nextPage() {
  if (featuredOffset.value + ITEMS_PER_PAGE < featuredProducts.value.length)
    featuredOffset.value += ITEMS_PER_PAGE
}

// Static leagues
const staticLeagues = [
  { slug: 'champions-league',     name: 'Champions League',    color: '#0d47a1' },
  { slug: 'europa-league',        name: 'Europe League',       color: '#1b5e20' },
  { slug: 'copa-america',         name: 'Copa America',        color: '#880e4f' },
  { slug: 'asian-cup',            name: 'Asian Cup',           color: '#b71c1c' },
  { slug: 'african-nations-cup',  name: 'African Nations Cup', color: '#1b5e20' },
]

// Static collections
const staticCollections = [
  { slug: 'kids',                 name: 'Kids',                  color: '#1565c0' },
  { slug: 'large-sizes',          name: 'Large sizes',           color: '#2e7d32' },
  { slug: 'goalkeeper',           name: 'Goalkeeper',            color: '#212121' },
  { slug: 'authentic-pro-player', name: 'Authentic / Pro Player',color: '#4a148c' },
  { slug: 'shorts',               name: 'Shorts',                color: '#b71c1c' },
  { slug: 'socks',                name: 'Socks',                 color: '#e65100' },
]

useHead({ title: 'Jambulani — Your Favorite Customized Club Jerseys' })
</script>

<style>
.skewed {
  position: relative;
}
.skewed::after,
.skewed::before {
  content: "";
  position: absolute;
  background-color: hsla(51, 95%, 50%, var(--alpha));
  width: 100%;
  height: 100%;
}
.skewed::before {
  --alpha: 0.16;
  top: -100%;
  left: -50%;
  transform: skewX(45deg);
}
.skewed::after {
  --alpha: 0.4;
  top: -50%;
  left: -100%;
  transform: skewY(45deg);
}
</style>