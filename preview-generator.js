#!/usr/bin/env node

/**
 * FC Pro Collection - Preview Generator
 * Simulates trait distribution for first 100 test NFTs
 */

const fs = require('fs');
const path = require('path');

const LAYERS_DIR = '/Users/djm/claude-projects/GitHub/art-engine/layers';
const PREVIEW_COUNT = 100;

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

// Import functions from rarity verification
const { analyzeLayer, calculateProbabilities } = require('./rarity-verification.js');

function weightedRandomSelect(traitsWithProbs) {
    const totalWeight = traitsWithProbs.reduce((sum, trait) => sum + trait.weight, 0);
    let random = Math.random() * totalWeight;
    
    for (const trait of traitsWithProbs) {
        random -= trait.weight;
        if (random <= 0) {
            return trait;
        }
    }
    
    // Fallback to last trait
    return traitsWithProbs[traitsWithProbs.length - 1];
}

function generateSingleNFT(layerAnalysis, nftId) {
    const selectedTraits = {};
    
    // Generate traits for each layer
    Object.entries(layerAnalysis).forEach(([layerName, layerData]) => {
        const selectedTrait = weightedRandomSelect(layerData.traits);
        selectedTraits[layerName] = {
            name: selectedTrait.name,
            weight: selectedTrait.weight,
            probability: selectedTrait.probability
        };
    });
    
    return {
        id: nftId,
        traits: selectedTraits
    };
}

function analyzeGeneratedTraits(generatedNFTs) {
    const traitCounts = {};
    const layerStats = {};
    
    // Initialize counters
    generatedNFTs.forEach(nft => {
        Object.entries(nft.traits).forEach(([layerName, trait]) => {
            if (!traitCounts[layerName]) {
                traitCounts[layerName] = {};
                layerStats[layerName] = { total: 0, withTrait: 0, withoutTrait: 0 };
            }
            
            if (!traitCounts[layerName][trait.name]) {
                traitCounts[layerName][trait.name] = 0;
            }
            
            traitCounts[layerName][trait.name]++;
            layerStats[layerName].total++;
            
            if (trait.name.includes('NON3')) {
                layerStats[layerName].withoutTrait++;
            } else {
                layerStats[layerName].withTrait++;
            }
        });
    });
    
    return { traitCounts, layerStats };
}

function printPreviewResults(generatedNFTs, analysis) {
    const { traitCounts, layerStats } = analysis;
    
    console.log(`\n${colors.bright}${colors.green}═══════════════════════════════════════════════════════════════════════════════${colors.reset}`);
    console.log(`${colors.bright}${colors.green}🎯 FC PRO COLLECTION - PREVIEW GENERATION (${PREVIEW_COUNT} NFTs)${colors.reset}`);
    console.log(`${colors.bright}${colors.green}═══════════════════════════════════════════════════════════════════════════════${colors.reset}`);
    
    // Print layer-by-layer statistics
    Object.entries(layerStats).forEach(([layerName, stats]) => {
        console.log(`\n${colors.bright}${colors.cyan}📁 ${layerName}${colors.reset}`);
        
        if (stats.withoutTrait > 0) {
            const withoutPercentage = (stats.withoutTrait / stats.total * 100).toFixed(1);
            const withPercentage = (stats.withTrait / stats.total * 100).toFixed(1);
            console.log(`${colors.yellow}   Without ${layerName}: ${stats.withoutTrait}/${stats.total} (${withoutPercentage}%)${colors.reset}`);
            console.log(`${colors.green}   With ${layerName}: ${stats.withTrait}/${stats.total} (${withPercentage}%)${colors.reset}`);
        } else {
            console.log(`${colors.green}   All NFTs have ${layerName} traits${colors.reset}`);
        }
        
        // Show most common traits
        const sortedTraits = Object.entries(traitCounts[layerName])
            .filter(([traitName]) => !traitName.includes('NON3'))
            .sort(([,a], [,b]) => b - a)
            .slice(0, 5);
        
        if (sortedTraits.length > 0) {
            console.log(`${colors.blue}   Top traits:${colors.reset}`);
            sortedTraits.forEach(([traitName, count]) => {
                const percentage = (count / stats.total * 100).toFixed(1);
                console.log(`     ${traitName}: ${count} (${percentage}%)`);
            });
        }
    });
    
    // Identify rare combinations
    console.log(`\n${colors.bright}${colors.magenta}💎 RARE TRAIT COMBINATIONS FOUND:${colors.reset}`);
    
    const rareNFTs = generatedNFTs.filter(nft => {
        // Check for ultra-rare body types
        const bodyTrait = nft.traits['Body.skin.race'];
        const hasUltraRareBody = bodyTrait && bodyTrait.probability < 1;
        
        // Check for rare face decorations
        const faceTrait = nft.traits['Face decoration'];
        const hasRareFace = faceTrait && !faceTrait.name.includes('NON3');
        
        // Check for costume
        const costumeTrait = nft.traits['Costume'];
        const hasCostume = costumeTrait && !costumeTrait.name.includes('NON3');
        
        return hasUltraRareBody || hasRareFace || hasCostume;
    });
    
    if (rareNFTs.length > 0) {
        rareNFTs.slice(0, 10).forEach(nft => {
            console.log(`\n${colors.magenta}   NFT #${nft.id}:${colors.reset}`);
            
            Object.entries(nft.traits).forEach(([layerName, trait]) => {
                if (trait.probability < 2 || layerName === 'Body.skin.race' || 
                    (layerName === 'Face decoration' && !trait.name.includes('NON3')) ||
                    (layerName === 'Costume' && !trait.name.includes('NON3'))) {
                    
                    const rarity = trait.probability < 1 ? '💎 Ultra Rare' : 
                                  trait.probability < 5 ? '🔥 Very Rare' : '⭐ Rare';
                    console.log(`     ${layerName}: ${trait.name} ${rarity} (${trait.probability.toFixed(1)}%)`);
                }
            });
        });
    } else {
        console.log(`   No ultra-rare combinations in this ${PREVIEW_COUNT} NFT sample`);
    }
    
    // Print collection insights
    console.log(`\n${colors.bright}${colors.blue}📊 COLLECTION INSIGHTS:${colors.reset}`);
    
    // Skin tone distribution
    const bodyStats = traitCounts['Body.skin.race'];
    if (bodyStats) {
        const commonSkins = ['Black', 'Black 2', 'Pink', 'Tan', 'Tan 2', 'White'];
        const commonSkinCount = commonSkins.reduce((sum, skin) => sum + (bodyStats[skin] || 0), 0);
        const commonSkinPercentage = (commonSkinCount / PREVIEW_COUNT * 100).toFixed(1);
        console.log(`🎨 Common skin tones: ${commonSkinCount}/${PREVIEW_COUNT} (${commonSkinPercentage}%)`);
    }
    
    // Accessory coverage
    const accessoryLayers = [
        { layer: 'Face decoration', name: 'face decorations' },
        { layer: 'Earrings', name: 'earrings' },
        { layer: 'Glasses', name: 'glasses' },
        { layer: 'Hat', name: 'hats' },
        { layer: 'Friend', name: 'friends' }
    ];
    
    accessoryLayers.forEach(({ layer, name }) => {
        const stats = layerStats[layer];
        if (stats && stats.withTrait !== undefined) {
            const percentage = (stats.withTrait / stats.total * 100).toFixed(1);
            console.log(`👕 NFTs with ${name}: ${stats.withTrait}/${stats.total} (${percentage}%)`);
        }
    });
    
    console.log(`\n${colors.green}✅ Preview generation complete! Sample shows good trait distribution.${colors.reset}`);
}

function savePreviewData(generatedNFTs, analysis) {
    const outputData = {
        generatedAt: new Date().toISOString(),
        previewCount: PREVIEW_COUNT,
        nfts: generatedNFTs,
        analysis: analysis,
        summary: {
            totalNFTs: generatedNFTs.length,
            layerCount: Object.keys(analysis.layerStats).length,
            rareNFTs: generatedNFTs.filter(nft => {
                const bodyTrait = nft.traits['Body.skin.race'];
                return bodyTrait && bodyTrait.probability < 1;
            }).length
        }
    };
    
    const outputPath = '/Users/djm/claude-projects/GitHub/FC-pro-collection/preview-results.json';
    fs.writeFileSync(outputPath, JSON.stringify(outputData, null, 2));
    console.log(`\n${colors.blue}💾 Preview data saved to: ${outputPath}${colors.reset}`);
}

function main() {
    console.log(`${colors.bright}${colors.blue}🎯 FC Pro Collection - Preview Generator${colors.reset}`);
    console.log(`${colors.blue}Generating ${PREVIEW_COUNT} sample NFTs to preview trait distribution...${colors.reset}`);
    
    if (!fs.existsSync(LAYERS_DIR)) {
        console.error(`${colors.red}❌ Error: Layers directory not found: ${LAYERS_DIR}${colors.reset}`);
        process.exit(1);
    }
    
    // Analyze all layers
    const layerDirectories = fs.readdirSync(LAYERS_DIR)
        .map(dir => path.join(LAYERS_DIR, dir))
        .filter(dir => fs.statSync(dir).isDirectory());
    
    const layerAnalysis = {};
    
    layerDirectories.forEach(layerPath => {
        try {
            const layerData = analyzeLayer(layerPath);
            const traitsWithProbs = calculateProbabilities(layerData);
            layerAnalysis[layerData.layerName] = {
                ...layerData,
                traits: traitsWithProbs
            };
        } catch (error) {
            console.error(`${colors.red}❌ Error analyzing layer ${path.basename(layerPath)}: ${error.message}${colors.reset}`);
        }
    });
    
    // Generate sample NFTs
    console.log(`\n${colors.yellow}🎲 Generating ${PREVIEW_COUNT} sample NFTs...${colors.reset}`);
    
    const generatedNFTs = [];
    for (let i = 1; i <= PREVIEW_COUNT; i++) {
        const nft = generateSingleNFT(layerAnalysis, i);
        generatedNFTs.push(nft);
    }
    
    // Analyze results
    const analysis = analyzeGeneratedTraits(generatedNFTs);
    
    // Print results
    printPreviewResults(generatedNFTs, analysis);
    
    // Save data
    savePreviewData(generatedNFTs, analysis);
}

// Run the preview generator
if (require.main === module) {
    main();
}

module.exports = { generateSingleNFT, analyzeGeneratedTraits };