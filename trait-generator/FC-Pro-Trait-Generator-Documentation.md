# FC-Pro Trait Generator Documentation

#nft #tools #trait-generation #fc-pro

## Overview

The FC-Pro Trait Generator is a professional web-based tool for creating NFT traits. It was developed to solve the quality issues with programmatic generation while maintaining the correct specifications for the FC-Pro collection.

## Problem It Solves

- **ImageMagick Limitations**: Poor quality output, incorrect positioning
- **AI Generation Issues**: No transparency support, wrong dimensions
- **Manual Work Burden**: Need for accessible tools without complex setup

## Key Specifications

- **Canvas Size**: 600x600px (exact)
- **Format**: PNG with full transparency
- **Style**: Flat vector art (CryptoPunks-inspired)
- **Layering**: Proper z-order for trait compositing

## Features

### Core Functionality
- [[Layers]] - Full layer management system
- [[Drawing Tools]] - Brush, eraser, shapes, text
- [[Transform Controls]] - Move, scale, rotate, flip
- [[Masking System]] - Advanced compositing
- [[Reference Images]] - Multiple reference support

### Quick Generators
Pre-built generators for common traits:
- Shirts (with text options)
- Earrings (crypto logos)
- Eyes (laser effects)
- Mouth (grillz)

### Professional UI
- Dark theme for extended use
- Keyboard shortcuts
- Tool persistence
- Clear visual feedback

## Workflow

### Basic Trait Creation
1. Open `index.html` in browser
2. Load reference trait for positioning
3. Create new layer for each element
4. Use tools to draw/generate trait
5. Export with proper naming

### Advanced Techniques

#### Texture Masking
```
1. Draw base shape
2. Create mask from selection
3. Apply texture to mask
4. Adjust as needed
```

#### Multi-Variant Creation
```
1. Create base trait
2. Duplicate layer
3. Modify each variant
4. Export separately
```

## File Naming Convention

```
[Layer][Trait]_[variant]#[rarity].png
```

Examples:
- `ShirtWAGMI_black#5.png`
- `EarringsETH#5.png`
- `EyesLaser_red#2.png`

## Integration with Art Engine

### Folder Structure
```
fc-pro-collection/
├── layers/
│   ├── Body.skin.race/
│   ├── Shirt/
│   ├── Eyes/
│   ├── Mouth/
│   └── Earrings/
└── trait-generator/
    ├── index.html
    ├── README.md
    └── TECHNICAL-GUIDE.md
```

### Config Updates
When adding new traits:
1. Place in appropriate layer folder
2. Update incompatibility rules if needed
3. Test with art engine generation

## Technical Details

- **Technology**: HTML5 Canvas API
- **Language**: Vanilla JavaScript
- **Dependencies**: None (standalone)
- **Browser Support**: Modern browsers

## Tips for Quality

1. **Always preview** with references before export
2. **Use layers** for non-destructive editing
3. **Check transparency** by disabling grid
4. **Test compositing** with other traits
5. **Maintain style** consistency

## Common Issues

### Performance
- Large textures may cause lag
- Solution: Resize textures before importing

### Color Matching
- Browser color profiles may vary
- Solution: Use hex values from existing traits

### Export Issues
- Some browsers block downloads
- Solution: Check browser permissions

## Future Enhancements

- [ ] Project save/load functionality
- [ ] Batch export capabilities
- [ ] Advanced brush engines
- [ ] SVG import support
- [ ] Collaboration features

## Related Documentation

- [[NFT Generation Pipeline]]
- [[Art Engine Configuration]]
- [[Trait Incompatibility Rules]]
- [[FC-Pro Style Guide]]

## Links

- [Generator Location](file:///Users/djm/claude-projects/github-repos/fc-pro-collection/trait-generator/index.html)
- [GitHub Repository](https://github.com/[your-username]/fc-pro-collection)
- [Art Engine Docs](../art-engine/README.md)

---

Created: 2024-01-23
Last Updated: 2024-01-23
Tags: #nft #tools #documentation