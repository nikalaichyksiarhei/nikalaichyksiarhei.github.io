<script setup>
import { onMounted, onUnmounted, onBeforeUnmount, ref, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'

import themeImg from '@/assets/img/theme.webp'
import analyticsImg from '@/assets/img/analitics.webp'
import mainImg from '@/assets/img/main.webp'
import transactionImg from '@/assets/img/transaction.webp'
import limitsImg from '@/assets/img/limits.webp'

const { t } = useI18n()

const phonesContainerRef = ref(null)
const dotsRef = ref(null)
const parallaxStyle = ref({})
let scrollListener = null

onMounted(() => {
  if (window.innerWidth > 768) {
    window.addEventListener('mousemove', handleMouseMove)
  }
  nextTick(() => {
    initMobileCarousel()
    initScrollReveal()
  })
})

onUnmounted(() => {
  if (window.innerWidth > 768) {
    window.removeEventListener('mousemove', handleMouseMove)
  }
  if (phonesContainerRef.value && scrollListener) {
    phonesContainerRef.value.removeEventListener('scroll', scrollListener)
  }
})

function handleMouseMove(e) {
  // Parallax Logic for Phones
  const { clientX, clientY } = e
  const { innerWidth, innerHeight } = window

  // Calculate rotation based on cursor position relative to center
  const x = (clientX - innerWidth / 2) / innerWidth // -0.5 to 0.5
  const y = (clientY - innerHeight / 2) / innerHeight // -0.5 to 0.5

  parallaxStyle.value = {
    transform: `rotateY(${x * 10}deg) rotateX(${-y * 10}deg)`
  }

  // Spotlight Logic for Feature Cards
  const cards = document.querySelectorAll('.feature-card')
  for(const card of cards) {
    const rect = card.getBoundingClientRect()
    const x = clientX - rect.left
    const y = clientY - rect.top
    card.style.setProperty('--mouse-x', `${x}px`)
    card.style.setProperty('--mouse-y', `${y}px`)
  }
}

function initScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card').forEach((el, index) => {
        el.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(el);
    });
}

function initMobileCarousel() {
    if (window.innerWidth > 768) return;

    const container = phonesContainerRef.value;
    if (!container) return;

    const phones = container.querySelectorAll('.phone');

    if (phones.length === 0) return;

    // Center the middle phone initially
    const centerPhone = phones[2];
    if (centerPhone) {
        const scrollLeft = centerPhone.offsetLeft - (window.innerWidth / 2) + (centerPhone.offsetWidth / 2);
        container.scrollLeft = scrollLeft;
    }

    // Create pagination dots
    const dotsContainer = dotsRef.value;
    if (dotsContainer) {
        dotsContainer.innerHTML = '';
        phones.forEach((_, index) => {
            const dot = document.createElement('div');
            dot.classList.add('carousel-dot');
            if (index === 2) dot.classList.add('active');
            dotsContainer.appendChild(dot);
        });
    }

    const dots = dotsContainer ? dotsContainer.querySelectorAll('.carousel-dot') : [];

    const observerOptions = {
        root: container,
        threshold: 0.5,
        rootMargin: "0px -10% 0px -10%"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                phones.forEach(p => p.classList.remove('active'));
                entry.target.classList.add('active');

                const index = Array.from(phones).indexOf(entry.target);
                if (dots && dots.length > 0) {
                    dots.forEach(d => d.classList.remove('active'));
                    if (dots[index]) {
                        dots[index].classList.add('active');
                    }
                }
            }
        });
    }, observerOptions);

    phones.forEach(phone => observer.observe(phone));

    const updateScales = () => {
        const containerCenter = container.offsetWidth / 2;

        phones.forEach(phone => {
            const rect = phone.getBoundingClientRect();
            const phoneCenter = rect.left + (rect.width / 2);
            const distance = Math.abs(containerCenter - phoneCenter);

            const maxDistance = 180;
            const minScale = 0.85;
            const maxScale = 1.0;

            let scale = maxScale - ((distance / maxDistance) * (maxScale - minScale));

            if (scale < minScale) scale = minScale;
            if (scale > maxScale) scale = maxScale;

            phone.style.transform = `scale(${scale})`;
        });
    };

    scrollListener = () => {
        requestAnimationFrame(updateScales);
    };

    container.addEventListener('scroll', scrollListener);
    updateScales();
}
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <h1 v-html="t('hero.title')"></h1>
                <p v-html="t('hero.subtitle')"></p>
                <a href="https://apps.apple.com/app/id6756549886" class="btn btn-primary" target="_blank">
                    <svg viewBox="0 0 384 512" width="20" fill="currentColor">
                        <path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 52.3-11.4 69.5-34.3z" />
                    </svg>
                    {{ t('hero.cta') }}
                </a>
            </div>

            <!-- Phones Animation Showcase -->
            <div class="phones-container" ref="phonesContainerRef" :style="parallaxStyle">
                <!-- Left 2: Theme -->
                <div class="phone left-2">
                    <div class="phone-screen">
                        <img v-lazy="themeImg" alt="Theme Screen" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                </div>

                <!-- Left 1: Analytics -->
                <div class="phone left-1">
                    <div class="phone-screen">
                        <img v-lazy="analyticsImg" alt="Analytics Screen" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                </div>

                <!-- Center: Home Screen -->
                <div class="phone center">
                    <div class="phone-screen">
                        <img v-lazy="mainImg" alt="Main Screen" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                </div>

                <!-- Right 1: Add Transaction -->
                <div class="phone right-1">
                    <div class="phone-screen">
                        <img v-lazy="transactionImg" alt="Add Transaction" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                </div>

                <!-- Right 2: Limits -->
                <div class="phone right-2">
                    <div class="phone-screen">
                        <img v-lazy="limitsImg" alt="Limits Screen" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                </div>
            </div>

            <!-- Mobile Carousel Controls -->
            <div class="carousel-controls">
                <div class="carousel-dots" ref="dotsRef"></div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="section">
        <div class="container">
            <h2>{{ t('features.title') }}</h2>
            <div class="features-grid">
                <!-- Smart Analytics -->
                <div class="feature-card">
                    <div class="feature-icon">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <!-- Axis -->
                            <line x1="3" y1="20" x2="21" y2="20" stroke-opacity="0.3"></line>
                            <line x1="3" y1="20" x2="3" y2="4" stroke-opacity="0.3"></line>
                            <!-- Animated Graph Line -->
                            <path class="anim-graph-path" d="M3 20 L9 14 L15 16 L21 6" stroke="#009688" stroke-dasharray="100" stroke-dashoffset="100"></path>
                        </svg>
                    </div>
                    <h3>{{ t('features.analytics.title') }}</h3>
                    <p>{{ t('features.analytics.desc') }}</p>
                </div>

                <!-- Home Screen Widgets -->
                <div class="feature-card">
                    <div class="feature-icon">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect class="anim-widget-rect" x="3" y="3" width="7" height="7" rx="1" stroke="#009688"></rect>
                            <rect class="anim-widget-rect" x="14" y="3" width="7" height="7" rx="1"></rect>
                            <rect class="anim-widget-rect" x="14" y="14" width="7" height="7" rx="1" stroke="#009688"></rect>
                            <rect class="anim-widget-rect" x="3" y="14" width="7" height="7" rx="1"></rect>
                        </svg>
                    </div>
                    <h3>{{ t('features.widgets.title') }}</h3>
                    <p>{{ t('features.widgets.desc') }}</p>
                </div>

                <!-- Spending Limits -->
                <div class="feature-card">
                    <div class="feature-icon">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <!-- Background Circle -->
                            <circle cx="12" cy="12" r="9" stroke-opacity="0.2"></circle>
                            <!-- Animated Progress -->
                            <path class="anim-limits-path" d="M12 3 A 9 9 0 1 1 3 12" stroke="#009688" stroke-dasharray="60" stroke-dashoffset="60" stroke-linecap="round"></path>
                            <!-- Checkmark -->
                            <path d="M9 12l2 2 4-4" stroke-width="1.5"></path>
                        </svg>
                    </div>
                    <h3>{{ t('features.limits.title') }}</h3>
                    <p>{{ t('features.limits.desc') }}</p>
                </div>

                <!-- Light & Dark Modes -->
                <div class="feature-card">
                    <div class="feature-icon">
                        <svg class="anim-theme-icon" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="5"></circle>
                            <line x1="12" y1="1" x2="12" y2="3"></line>
                            <line x1="12" y1="21" x2="12" y2="23"></line>
                            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                            <line x1="1" y1="12" x2="3" y2="12"></line>
                            <line x1="21" y1="12" x2="23" y2="12"></line>
                            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                        </svg>
                    </div>
                    <h3>{{ t('features.theme.title') }}</h3>
                    <p>{{ t('features.theme.desc') }}</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="section" style="text-align: center; background: linear-gradient(180deg, transparent 0%, rgba(0,150,136,0.1) 100%);">
        <div class="container">
            <h2 style="margin-bottom: 1rem;">{{ t('cta.title') }}</h2>
            <p style="margin-bottom: 30px; color: var(--text-secondary);">{{ t('cta.subtitle') }}</p>
            <a href="https://apps.apple.com/app/id6756549886" class="btn btn-primary" style="padding: 15px 40px; font-size: 1.1rem;">
                {{ t('cta.button') }}
            </a>
        </div>
    </section>
  </div>
</template>