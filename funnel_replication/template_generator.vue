
<template>
  <div class="landing-page" :class="template.style">
    <!-- Dynamic Hero Section -->
    <section class="hero" :style="heroStyles">
      <h1>{{ content.hero.heading }}</h1>
      <p>{{ content.hero.subheading }}</p>
      <call-to-action 
        :text="content.hero.cta.text"
        :style="content.hero.cta.style"
        @click="trackConversion('hero')"
      />
    </section>

    <!-- Benefits Section -->
    <section class="benefits">
      <div class="benefits-grid">
        <benefit-card
          v-for="(benefit, index) in content.benefits"
          :key="index"
          :benefit="benefit"
          :layout="template.benefitLayout"
        />
      </div>
    </section>

    <!-- Social Proof -->
    <section class="social-proof">
      <testimonial-slider 
        :testimonials="content.testimonials"
        :style="template.testimonialStyle"
      />
      <trust-badges :badges="content.trustBadges" />
    </section>

    <!-- Features -->
    <section class="features">
      <feature-comparison 
        :features="content.features"
        :highlight="content.highlightedFeatures"
      />
    </section>

    <!-- Final CTA -->
    <section class="final-cta">
      <h2>{{ content.finalCta.heading }}</h2>
      <call-to-action 
        :text="content.finalCta.text"
        :style="content.finalCta.style"
        @click="trackConversion('final')"
      />
    </section>
  </div>
</template>

<script>
export default {
  name: 'LandingPageTemplate',

  props: {
    content: {
      type: Object,
      required: true
    },
    template: {
      type: Object,
      required: true
    }
  },

  computed: {
    heroStyles() {
      return {
        backgroundImage: `url(${this.content.hero.background})`,
        ...this.template.heroStyle
      }
    }
  },

  methods: {
    trackConversion(location) {
      this.$emit('conversion', {
        location,
        timestamp: new Date(),
        template: this.template.id
      })
    }
  },

  components: {
    'benefit-card': require('./components/BenefitCard.vue'),
    'testimonial-slider': require('./components/TestimonialSlider.vue'),
    'trust-badges': require('./components/TrustBadges.vue'),
    'feature-comparison': require('./components/FeatureComparison.vue'),
    'call-to-action': require('./components/CallToAction.vue')
  }
}
</script>

<style lang="scss">
.landing-page {
  max-width: 1200px;
  margin: 0 auto;

  section {
    padding: 4rem 2rem;

    @media (max-width: 768px) {
      padding: 2rem 1rem;
    }
  }

  .hero {
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background-size: cover;
    background-position: center;
  }

  .benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
  }
}
</style>
