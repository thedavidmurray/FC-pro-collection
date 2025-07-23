# FC-Pro Trait Generator Pro

A professional web-based tool for creating NFT traits with proper dimensions, transparency, and layering support.

## Features

### 🎨 Core Features
- **600x600px Canvas** - Exact dimensions for FC-Pro NFT traits
- **Full Transparency Support** - Proper PNG export with alpha channel
- **Multi-Layer System** - Professional layer management like Photoshop
- **Reference Image Support** - Load multiple reference images for positioning
- **Dark Professional UI** - Easy on the eyes for extended use

### 🛠️ Drawing Tools
1. **Select/Move Tool** (V) - Click and drag layers
2. **Brush Tool** (B) - Variable size and opacity
3. **Eraser Tool** (E) - Remove parts with transparency
4. **Shape Tool** (S) - Rectangle, circle, line
5. **Text Tool** (T) - Add text with font options
6. **Mask Tool** - Advanced masking capabilities
7. **Fill Tool** - Flood fill with color

### 🔄 Transform Options
- **Position** - X/Y coordinate controls
- **Scale** - Width/height percentage
- **Rotation** - 0-360° rotation slider
- **Flip** - Horizontal/vertical flip buttons
- **Opacity** - Layer transparency control

### 🎭 Advanced Features
- **Masking System** - Create masks from selections, apply textures/patterns
- **Color Palette** - Customizable color swatches
- **Grid System** - Optional grid with snap-to-grid
- **Zoom Controls** - Mouse wheel + button controls
- **History** - Undo/redo support (Ctrl+Z)

## Quick Start

1. **Open the Generator**
   ```
   Open trait-generator/index.html in your web browser
   ```

2. **Create a New Trait**
   - Use Quick Generators for common traits (shirts, earrings, etc.)
   - Or create custom traits with drawing tools

3. **Layer Management**
   - Each element should be on its own layer
   - Use layer panel to organize, hide, or adjust opacity

4. **Export Your Trait**
   - Set filename format: `[Layer][Trait]_[variant]#[rarity].png`
   - Example: `ShirtWAGMI_black#5.png`
   - Click Export to download 600x600 PNG with transparency

## Keyboard Shortcuts

- **Ctrl/Cmd + Z** - Undo
- **Ctrl/Cmd + Shift + Z** - Redo
- **Ctrl/Cmd + S** - Export trait
- **Ctrl/Cmd + C** - Copy layer
- **Ctrl/Cmd + V** - Paste layer
- **V** - Select/Move tool
- **B** - Brush tool
- **E** - Eraser tool
- **S** - Shape tool
- **T** - Text tool

## NFT Trait Guidelines

### Naming Convention
```
[Layer][Trait]_[variant]#[rarity].png
```
- **Layer**: Body, Shirt, Eyes, Mouth, etc.
- **Trait**: Specific trait name
- **Variant**: Color or style variant
- **Rarity**: Weight number (1=ultra rare, 10=common)

### Examples:
- `ShirtWAGMI_black#5.png`
- `EarringsETH#5.png`
- `EyesLaser_red#2.png`
- `MouthGrillz_gold#3.png`

### Layer Order (Bottom to Top)
1. Background
2. Body/Skin
3. Shirt/Clothing
4. Face decorations
5. Eyes
6. Eyewear/Glasses
7. Mouth
8. Hair
9. Headwear/Hats
10. Accessories (earrings, etc.)

## Advanced Techniques

### Creating Masked Textures
1. Draw your shape on a layer
2. Click "Create Mask from Selection"
3. Click "Apply Texture to Mask"
4. Upload a texture image
5. The texture will be clipped to your shape

### Using Reference Images
1. Upload existing traits as references
2. Adjust reference opacity with layer controls
3. Draw new traits with perfect alignment
4. Hide references before exporting

### Batch Workflow
1. Create a base trait (e.g., shirt shape)
2. Duplicate the layer
3. Modify colors/patterns on each duplicate
4. Export each variant with proper naming

## Tips & Best Practices

1. **Always work at 600x600** - Don't resize after creation
2. **Use layers extensively** - One element per layer
3. **Save your work** - Export working files regularly
4. **Check transparency** - Disable grid before export
5. **Test compositing** - Preview how traits layer together
6. **Maintain style consistency** - Keep the flat vector aesthetic

## Integration with Art Engine

After creating traits:
1. Export with proper naming convention
2. Place in appropriate layer folder
3. Update `config.js` if adding new trait types
4. Test generation with art-engine

## Browser Compatibility

Works best in:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Known Issues

- Large textures may slow performance
- Complex masks require careful layer management
- Some browsers may have color profile differences

## Support

For issues or feature requests, please check the FC-Pro documentation or contact the development team.