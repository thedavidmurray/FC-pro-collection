# FC Pro Collection (Protardio)

A Farcaster-themed NFT collection featuring community culture, memes, and inside jokes from the decentralized social protocol.

## Overview

Protardio is a generative NFT collection celebrating Farcaster culture, featuring trait combinations inspired by the community, popular users, channels, and ecosystem memes. The collection uses HashLips Art Engine for procedural generation with carefully curated traits that reflect the authentic spirit of Farcaster.

## Project Structure

```
FC-pro-collection/
├── layers/                    # Trait layers for generation
│   └── Backgrounds/          # Background trait images
├── hashlips_art_engine/      # Core generation engine
├── protardio-bg-tools/       # Custom background editing tools
├── previews/                 # Preview GIFs of generated art
├── pngs/                     # Generated PNG outputs
├── og traits/                # Original trait designs
├── traits-checklist.md      # Trait planning and status
└── README.md                # This file
```

## Features

### Trait Categories
- **Backgrounds**: Farcaster-themed environments and memes
- **Race/Species**: Different character types including OG Farcaster, Clanker, Wassie variants
- **Hair**: Various styles from dev messy to founder slicked
- **Eyes**: Color variations including higher-pilled and rainbow options
- **Hats**: Higher hats, degen gear, protocol merchandise
- **Shirts**: Channel references, protocol messaging, community slogans
- **Accessories**: Glasses (noggles, oviators), earrings, necklaces
- **Friends**: Companion characters from the ecosystem

### Custom Tools
The `protardio-bg-tools/` directory contains custom HTML tools for:
- Background overlay effects
- Batch blur processing
- Trait editing interfaces
- Image resizing utilities
- Oviator shine effects

## Getting Started

### Prerequisites
- Node.js and npm/yarn
- Basic understanding of HashLips Art Engine

### Installation
1. Clone the repository
2. Navigate to the `hashlips_art_engine` directory
3. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

### Configuration
Edit the configuration files in the art engine to adjust:
- Layer order and rarity weights
- Output resolution and format
- Generation parameters
- Metadata attributes

### Generation
Run the art generation process:
```bash
npm run generate
# or
yarn generate
```

## Trait Development Status

See `traits-checklist.md` for detailed progress on trait categories and specific items needed. The project aims for comprehensive representation of Farcaster culture while maintaining artistic coherence.

## Community Integration

This collection draws inspiration from:
- Farcaster protocol features and terminology
- Popular community members and their aesthetics
- Channel cultures and inside jokes
- Ecosystem projects and collaborations
- Meme culture and viral content

## License

This project is released under a dual license:
- Viral Public License (Copyleft)
- CC0 1.0 Universal

All rights are relinquished to promote free culture and community collaboration.

## Contributing

Community contributions are welcome, especially:
- New trait designs reflecting current Farcaster culture
- Tool improvements and optimizations
- Documentation and tutorial content
- Testing and quality assurance

## Acknowledgments

Built using HashLips Art Engine and inspired by the vibrant Farcaster community. Special recognition to the creators, builders, and memers who make the protocol a unique cultural space.