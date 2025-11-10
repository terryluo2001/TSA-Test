# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a React + TypeScript frontend application built with Vite. It appears to be part of a larger TSA (Transportation Security Administration) testing system, serving as the frontend component.

## Development Commands

### Development Server
```bash
npm run dev
```
Starts the Vite development server with hot module replacement (HMR).

### Build
```bash
npm run build
```
Compiles TypeScript and builds the production bundle. Uses `tsc -b` for type checking followed by `vite build`.

### Linting
```bash
npm run lint
```
Runs ESLint across the codebase using the configured rules.

### Preview
```bash
npm run preview
```
Serves the production build locally for testing.

## Architecture

### Build System
- **Vite**: Primary build tool with React plugin
- **TypeScript**: Strict configuration with separate configs for app (`tsconfig.app.json`) and node (`tsconfig.node.json`)
- **ESLint**: Configured with React hooks, React refresh, and TypeScript rules

### Project Structure
```
src/
├── App.tsx          # Main application component
├── App.css          # App-specific styles
├── main.tsx         # Application entry point
├── index.css        # Global styles
└── assets/          # Static assets (SVGs, images)
```

### TypeScript Configuration
- **Strict mode enabled**: All strict TypeScript checks are active
- **Modern target**: ES2022 for app code, ES2023 for build tools
- **React JSX**: Uses `react-jsx` transform
- **Bundler mode**: Optimized for Vite bundling

### Entry Point
The application bootstraps through `src/main.tsx`, which renders the `App` component into the root element using React 18's `createRoot`.

## Key Technologies

- **React 19.1.1**: Latest React version with concurrent features
- **TypeScript 5.9.3**: Modern TypeScript with strict checking
- **Vite 7.1.7**: Fast build tool and dev server
- **ESLint 9.36.0**: Modern ESLint configuration

## Development Notes

- The project uses ES modules (`"type": "module"` in package.json)
- Hot module replacement is configured through Vite
- Strict TypeScript settings include unused variable detection and no unchecked side effect imports
- Currently contains minimal starter template code that should be replaced with TSA-specific functionality