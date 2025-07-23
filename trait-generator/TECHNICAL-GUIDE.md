# Technical Guide - FC-Pro Trait Generator

## Architecture Overview

The trait generator is a single-page web application built with vanilla JavaScript and HTML5 Canvas API.

### Core Components

1. **Layer System**
   ```javascript
   class Layer {
       constructor(name, width = 600, height = 600)
       draw(targetCtx)
       clone()
   }
   ```
   - Each layer has its own canvas element
   - Supports transform properties (position, scale, rotation)
   - Implements masking capabilities

2. **Tool System**
   - Tools are modular and switchable
   - Each tool has its own options panel
   - Tool state is maintained globally

3. **Rendering Pipeline**
   ```
   References → Layers → Selection Overlay → Grid
   ```

## Key Features Implementation

### Multi-Layer Compositing
```javascript
layers.forEach(layer => {
    layer.draw(ctx);
});
```
- Layers are rendered bottom to top
- Each layer applies its own transforms
- Masking is applied during layer drawing

### Transform System
- **Position**: Direct pixel offset
- **Scale**: Percentage-based scaling
- **Rotation**: Degree-based rotation
- **Opacity**: Alpha channel blending

### Masking Implementation
1. Create mask from alpha channel
2. Store mask as separate canvas
3. Apply during rendering with `destination-in` composite operation

### Export Process
1. Create clean 600x600 canvas
2. Render only layers (no UI elements)
3. Export as PNG blob
4. Trigger download

## Data Structures

### Layer Object
```javascript
{
    name: string,
    canvas: HTMLCanvasElement,
    ctx: CanvasRenderingContext2D,
    visible: boolean,
    opacity: number (0-1),
    x: number,
    y: number,
    rotation: number (degrees),
    scaleX: number,
    scaleY: number,
    mask: HTMLCanvasElement | null,
    id: unique identifier
}
```

### Tool Options
```javascript
{
    brush: { size, opacity, color },
    shape: { type, filled, strokeWidth, color },
    text: { fontSize, fontFamily, fontStyle, color }
}
```

## Performance Considerations

1. **Canvas Optimization**
   - Use `requestAnimationFrame` for smooth updates
   - Minimize full canvas redraws
   - Cache static elements

2. **Memory Management**
   - Limit history to 50 states
   - Clear unused image references
   - Dispose of temporary canvases

3. **Large Image Handling**
   - Resize references on load
   - Use image compression for textures
   - Implement viewport culling for zoom

## Extension Points

### Adding New Tools
1. Add tool button to toolbar
2. Create tool handler in switch statements
3. Add tool options UI
4. Implement mouse event handlers

### Adding New Generators
1. Create generation function
2. Add button to quick generators
3. Implement shape/pattern logic
4. Use Layer class for output

### Custom Export Formats
1. Modify export function
2. Add format options
3. Implement conversion logic
4. Update file extension

## Browser APIs Used

- **Canvas 2D Context** - Core drawing
- **File API** - Image uploads
- **Blob API** - Export functionality
- **Local Storage** - (Future) Save projects
- **Pointer Events** - Better touch support

## Security Considerations

- No server communication required
- All processing client-side
- Images processed in browser sandbox
- CORS handled for cross-origin images

## Future Enhancements

1. **Project Save/Load**
   - Serialize layer state
   - Compress with LZ-string
   - Save to local storage

2. **Advanced Brushes**
   - Pressure sensitivity
   - Custom brush shapes
   - Texture brushes

3. **Animation Support**
   - Frame-based layers
   - Onion skinning
   - GIF export

4. **Collaborative Features**
   - WebRTC peer sharing
   - Shared canvas state
   - Real-time updates