
class MultiArmedBandit {
    constructor(variants) {
        this.variants = variants.map(variant => ({
            ...variant,
            impressions: 0,
            conversions: 0,
            value: 0
        }));
        this.totalImpressions = 0;
    }

    selectVariant() {
        // Thompson sampling implementation
        const samples = this.variants.map(variant => {
            const alpha = variant.conversions + 1;
            const beta = variant.impressions - variant.conversions + 1;
            return {
                variant: variant,
                sample: this.getBetaSample(alpha, beta)
            };
        });

        return samples.reduce((best, current) => 
            current.sample > best.sample ? current : best
        ).variant;
    }

    getBetaSample(alpha, beta) {
        // Beta distribution sampling
        let x = 0;
        let y = 0;

        while (true) {
            x = Math.random();
            y = Math.random();

            if (Math.pow(x, alpha - 1) * Math.pow(1 - x, beta - 1) > y) {
                return x;
            }
        }
    }

    recordImpression(variantId) {
        const variant = this.variants.find(v => v.id === variantId);
        if (variant) {
            variant.impressions++;
            this.totalImpressions++;
        }
    }

    recordConversion(variantId, value = 1) {
        const variant = this.variants.find(v => v.id === variantId);
        if (variant) {
            variant.conversions++;
            variant.value += value;
        }
    }

    getStats() {
        return this.variants.map(variant => ({
            id: variant.id,
            impressions: variant.impressions,
            conversions: variant.conversions,
            conversionRate: variant.impressions === 0 ? 0 : 
                variant.conversions / variant.impressions,
            averageValue: variant.conversions === 0 ? 0 :
                variant.value / variant.conversions
        }));
    }
}

// Test tracking implementation
class ABTestTracker {
    constructor(testId, variants) {
        this.testId = testId;
        this.bandit = new MultiArmedBandit(variants);
        this.storage = window.localStorage;
    }

    initialize() {
        const variant = this.bandit.selectVariant();
        this.storage.setItem(`ab_test_${this.testId}`, variant.id);
        this.bandit.recordImpression(variant.id);
        return variant;
    }

    getVariant() {
        return this.storage.getItem(`ab_test_${this.testId}`);
    }

    trackConversion(value = 1) {
        const variantId = this.getVariant();
        if (variantId) {
            this.bandit.recordConversion(variantId, value);
        }
    }
}

module.exports = {
    MultiArmedBandit,
    ABTestTracker
};
