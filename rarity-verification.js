#!/usr/bin/env node

/**
 * FC Pro Collection - Rarity Verification Script
 * Calculates exact trait probabilities for 10,000 NFT collection
 */

const fs = require('fs');
const path = require('path');

const LAYERS_DIR = '/Users/djm/claude-projects/GitHub/art-engine/layers';
const TARGET_COLLECTION_SIZE = 10000;

// Color codes for output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

function parseTraitWeight(filename) {
    const match = filename.match(/#(\d+)\.png$/);
    return match ? parseInt(match[1]) : 0;
}

function getTraitName(filename) {
    return filename.replace(/#\d+\.png$/, '');
}

function analyzeLayer(layerPath) {
    const layerName = path.basename(layerPath);
    const files = fs.readdirSync(layerPath).filter(f => f.endsWith('.png'));
    
    const traits = files.map(file => ({
        name: getTraitName(file),
        weight: parseTraitWeight(file),
        filename: file
    }));
    
    const totalWeight = traits.reduce((sum, trait) => sum + trait.weight, 0);
    
    return {
        layerName,
        traits,
        totalWeight,
        traitCount: traits.length
    };
}

function calculateProbabilities(layerData) {
    return layerData.traits.map(trait => ({
        ...trait,
        probability: (trait.weight / layerData.totalWeight) * 100,
        expectedCount: Math.round((trait.weight / layerData.totalWeight) * TARGET_COLLECTION_SIZE)
    }));
}

function categorizeTraits(traitsWithProbs) {
    const categories = {
        ultraRare: [], // < 1%
        veryRare: [],  // 1-5%
        rare: [],      // 5-15%
        uncommon: [],  // 15-30%
        common: [],    // > 30%
        none: []       // NON3 variants
    };
    
    traitsWithProbs.forEach(trait => {
        if (trait.name.includes('NON3')) {
            categories.none.push(trait);
        } else if (trait.probability < 1) {
            categories.ultraRare.push(trait);
        } else if (trait.probability < 5) {
            categories.veryRare.push(trait);
        } else if (trait.probability < 15) {
            categories.rare.push(trait);
        } else if (trait.probability < 30) {
            categories.uncommon.push(trait);
        } else {
            categories.common.push(trait);
        }
    });
    
    return categories;
}

function printLayerAnalysis(layerData) {
    const traitsWithProbs = calculateProbabilities(layerData);
    const categories = categorizeTraits(traitsWithProbs);
    
    console.log(`\n${colors.bright}${colors.cyan}📁 ${layerData.layerName}${colors.reset}`);
    console.log(`${colors.blue}Total traits: ${layerData.traitCount} | Total weight: ${layerData.totalWeight}${colors.reset}`);
    
    // Print NON3 (None) variants first if they exist
    if (categories.none.length > 0) {
        console.log(`\n${colors.yellow}⭕ No ${layerData.layerName}:${colors.reset}`);
        categories.none.forEach(trait => {
            console.log(`   ${trait.probability.toFixed(1)}% (${trait.expectedCount.toLocaleString()} NFTs) - ${trait.name}`);
        });
    }
    
    // Print other categories
    const categoryOrder = [
        { key: 'ultraRare', label: '💎 Ultra Rare (<1%)', color: colors.magenta },
        { key: 'veryRare', label: '🔥 Very Rare (1-5%)', color: colors.red },
        { key: 'rare', label: '⭐ Rare (5-15%)', color: colors.yellow },
        { key: 'uncommon', label: '🟡 Uncommon (15-30%)', color: colors.green },
        { key: 'common', label: '⚪ Common (>30%)', color: colors.reset }
    ];
    
    categoryOrder.forEach(({ key, label, color }) => {
        if (categories[key].length > 0) {
            console.log(`\n${color}${label}:${colors.reset}`);
            categories[key]
                .sort((a, b) => a.probability - b.probability)
                .forEach(trait => {
                    console.log(`   ${trait.probability.toFixed(1)}% (${trait.expectedCount.toLocaleString()} NFTs) - ${trait.name}`);
                });
        }
    });
    
    return {
        layerName: layerData.layerName,
        totalTraits: layerData.traitCount,
        categories,
        totalWeight: layerData.totalWeight
    };
}

function generateSummaryReport(allLayerResults) {
    console.log(`\n${colors.bright}${colors.green}═══════════════════════════════════════════════════════════════════════════════${colors.reset}`);
    console.log(`${colors.bright}${colors.green}📊 FC PRO COLLECTION - RARITY SUMMARY REPORT (10,000 NFTs)${colors.reset}`);
    console.log(`${colors.bright}${colors.green}═══════════════════════════════════════════════════════════════════════════════${colors.reset}`);
    
    let totalUltraRare = 0;
    let totalVeryRare = 0;
    let totalRare = 0;
    
    console.log(`\n${colors.bright}Layer Overview:${colors.reset}`);
    allLayerResults.forEach(result => {
        const ultraRareCount = result.categories.ultraRare.length;
        const veryRareCount = result.categories.veryRare.length;
        const rareCount = result.categories.rare.length;
        const totalTraits = result.totalTraits;
        
        totalUltraRare += ultraRareCount;
        totalVeryRare += veryRareCount;
        totalRare += rareCount;
        
        console.log(`${colors.cyan}${result.layerName.padEnd(20)}${colors.reset} ${totalTraits.toString().padStart(3)} traits | ` +
                   `${colors.magenta}${ultraRareCount} ultra${colors.reset} | ` +
                   `${colors.red}${veryRareCount} very rare${colors.reset} | ` +
                   `${colors.yellow}${rareCount} rare${colors.reset}`);
    });
    
    console.log(`\n${colors.bright}Collection Rarity Breakdown:${colors.reset}`);
    console.log(`${colors.magenta}💎 Ultra Rare traits: ${totalUltraRare}${colors.reset}`);
    console.log(`${colors.red}🔥 Very Rare traits: ${totalVeryRare}${colors.reset}`);
    console.log(`${colors.yellow}⭐ Rare traits: ${totalRare}${colors.reset}`);
    
    // Highlight key distribution insights
    console.log(`\n${colors.bright}Key Insights:${colors.reset}`);
    
    // Find skin distribution
    const bodyLayer = allLayerResults.find(r => r.layerName === 'Body.skin.race');
    if (bodyLayer) {
        const commonSkins = bodyLayer.categories.common.concat(bodyLayer.categories.uncommon);
        const totalCommonSkinPercentage = commonSkins.reduce((sum, trait) => sum + trait.probability, 0);
        console.log(`🎨 Common skin tones: ${totalCommonSkinPercentage.toFixed(1)}% of collection`);
    }
    
    // Find accessory coverage
    const accessoryLayers = ['Face decoration', 'Earrings', 'Glasses', 'Hat', 'Friend'];
    accessoryLayers.forEach(layerName => {
        const layer = allLayerResults.find(r => r.layerName === layerName);
        if (layer && layer.categories.none.length > 0) {
            const nonePercentage = layer.categories.none[0].probability;
            const withAccessoryPercentage = 100 - nonePercentage;
            console.log(`👕 ${layerName}: ${withAccessoryPercentage.toFixed(1)}% will have this accessory`);
        }
    });
    
    console.log(`\n${colors.green}✅ Verification complete! Collection ready for 10K generation.${colors.reset}`);
}

function main() {
    console.log(`${colors.bright}${colors.blue}🎨 FC Pro Collection - Rarity Verification${colors.reset}`);
    console.log(`${colors.blue}Target collection size: ${TARGET_COLLECTION_SIZE.toLocaleString()} NFTs${colors.reset}`);
    console.log(`${colors.blue}Analyzing layers in: ${LAYERS_DIR}${colors.reset}`);
    
    if (!fs.existsSync(LAYERS_DIR)) {
        console.error(`${colors.red}❌ Error: Layers directory not found: ${LAYERS_DIR}${colors.reset}`);
        process.exit(1);
    }
    
    const layerDirectories = fs.readdirSync(LAYERS_DIR)
        .map(dir => path.join(LAYERS_DIR, dir))
        .filter(dir => fs.statSync(dir).isDirectory());
    
    const allLayerResults = [];
    
    layerDirectories.forEach(layerPath => {
        try {
            const layerData = analyzeLayer(layerPath);
            const result = printLayerAnalysis(layerData);
            allLayerResults.push(result);
        } catch (error) {
            console.error(`${colors.red}❌ Error analyzing layer ${path.basename(layerPath)}: ${error.message}${colors.reset}`);
        }
    });
    
    generateSummaryReport(allLayerResults);
}

// Run the verification
if (require.main === module) {
    main();
}

module.exports = { analyzeLayer, calculateProbabilities, categorizeTraits };