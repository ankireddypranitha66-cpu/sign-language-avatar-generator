# Sign Language Avatar Generator

A browser-based accessibility tool that converts spoken or typed English into a simplified ASL (American Sign Language) gloss and animates a 2D stick-figure avatar to perform the corresponding signs.

**[Live Demo](https://ankireddypranitha66-cpu.github.io/sign-language-avatar-generator/)**

## Overview

This project explores the pipeline behind sign language avatar systems: taking natural language input (speech or text), translating it into a sign-language-appropriate representation (gloss), and rendering that as animated sign language output. It was built as a learning project to understand the intersection of NLP, accessibility technology, and browser-based animation.

## Features

- **Speech-to-text** input via the Web Speech API (Chrome)
- **Text-to-gloss conversion**: a rule-based simplification that removes English-specific grammar elements (articles, auxiliary verbs, infinitive markers) not used in ASL gloss
- **2D animated avatar**: a custom-built skeletal stick-figure renderer using HTML5 Canvas, with keyframe-based pose interpolation
- **42-word sign library** covering greetings, pronouns, common verbs, question words, common nouns, numbers, time words, and feelings/states
- Graceful handling of unknown words (skips words with no defined sign, rather than failing)

## How It Works

1. **Input**: The user speaks (via microphone) or types a sentence
2. **Gloss conversion**: The sentence is tokenized and simplified — determiners (a/an/the), auxiliary verbs (is/am/are), and infinitive markers (to) are removed to approximate ASL gloss structure
3. **Sign lookup**: Each remaining word is checked against a sign library of hand-designed keyframe animations
4. **Animation**: Recognized words are played in sequence as a stick-figure avatar, interpolating smoothly between keyframe poses for each sign

## Tech Stack

- **Frontend**: Vanilla HTML, CSS, JavaScript (no frameworks — kept intentionally simple)
- **Speech recognition**: Web Speech API (`SpeechRecognition` / `webkitSpeechRecognition`)
- **Animation**: HTML5 Canvas with custom keyframe interpolation (linear interpolation between joint coordinates)
- **Sign data**: Hand-authored JSON-like keyframe definitions, referenced against [Lifeprint ASL Dictionary](https://www.lifeprint.com) for sign accuracy where possible

## Running Locally

1. Clone this repository:
