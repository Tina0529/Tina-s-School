# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is "Tina's School" (馨儿的知识乐园), a static educational website built with HTML, CSS, and JavaScript. The site serves as a knowledge repository for a student named Tina, containing interactive educational content across multiple subjects.

## Architecture & Structure

The project is organized as a **static website** with the following structure:

```
.
├── index.html              # Main homepage with subject categories
├── math.html              # Mathematics subject overview page
├── img/                   # Static assets (icons, logos)
├── 数学/                  # Math-specific content
│   ├── circular_track_race.html      # Interactive circular track simulation
│   └── triangle_inequality.html      # Interactive triangle geometry
├── 英语/                  # English content (external textbook)
├── 历史/                  # History content (empty)
└── 语文/                  # Chinese language content (empty)
```

### Key Design Patterns

1. **Subject-based Organization**: Content is organized by academic subjects (数学, 英语, 历史, 语文)
2. **Interactive Learning**: Each math topic includes interactive HTML5 Canvas-based visualizations
3. **Progressive Enhancement**: Uses CDN resources for styling (TailwindCSS, FontAwesome) with fallbacks
4. **Responsive Design**: Mobile-first approach with Tailwind CSS grid system

## Technology Stack

- **Frontend**: Pure HTML5, CSS3, JavaScript (ES6+)
- **Styling**: 
  - TailwindCSS 2.2.19 (via CDN)
  - Custom CSS for animations and card interactions
  - Google Fonts (Noto Sans SC, Noto Serif SC)
- **Icons**: FontAwesome 6.4.0
- **Visualization**: HTML5 Canvas for mathematical simulations
- **Diagrams**: Mermaid.js for knowledge graphs

## Development Approach

### File Naming Convention
- Chinese directory names for subject organization
- English filenames for individual content pages
- Descriptive naming (e.g., `circular_track_race.html`, `triangle_inequality.html`)

### CSS Architecture
- **Utility-first** with TailwindCSS for layout and basic styling
- **Component-based** custom CSS for interactive elements:
  - `.knowledge-card` for subject cards with hover effects
  - `.topic-card` for individual topic cards
  - `.principle` for highlighted educational principles

### JavaScript Patterns
- **Canvas-based simulations** for mathematical concepts
- **Event-driven interactions** with sliders, buttons, and input controls
- **Real-time calculations** and visual feedback
- **Animation loops** using `requestAnimationFrame`

## Content Structure

### Mathematics Section
Each math topic follows this pattern:
1. **Interactive Visualization**: HTML5 Canvas with real-time simulation
2. **Educational Principles**: Highlighted explanation boxes
3. **User Controls**: Sliders, inputs, and buttons for interaction
4. **Problem-Solution Format**: Clear question and answer presentation

### Expected Content Expansion
The site structure suggests planned expansion into:
- 语文 (Chinese Literature)
- 英语 (English Language) 
- 历史 (History)
- 科学 (Science)
- 艺术 (Art)

## Development Commands

This is a static website with no build process. For development:

```bash
# Serve locally (any static server)
python -m http.server 8000
# or
npx serve .

# Open in browser
open http://localhost:8000
```

## Key Implementation Notes

### Canvas-based Learning Tools
- Use `requestAnimationFrame` for smooth animations
- Implement zoom and pan controls for better user experience
- Include reset functionality for simulations
- Provide visual feedback for mathematical constraints

### Chinese Language Support
- Use appropriate Chinese fonts (Noto Sans SC, Noto Serif SC)
- Implement proper text rendering for mixed Chinese/English content
- Consider character encoding (UTF-8) for all Chinese text

### Interactive Features
- Implement input validation for mathematical parameters
- Provide immediate visual feedback for user actions
- Include explanatory text alongside interactive elements
- Design for both desktop and mobile interaction patterns

## Future Development Considerations

1. **Content Management**: Consider implementing a simple CMS for non-technical content updates
2. **Performance**: Optimize Canvas rendering for complex mathematical simulations
3. **Accessibility**: Add ARIA labels and keyboard navigation support
4. **Internationalization**: Structure allows for easy addition of English translations
5. **Analytics**: Consider adding educational progress tracking