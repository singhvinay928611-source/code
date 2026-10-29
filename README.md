# Gesture Hill Climb — full-stack starter

A browser-based 2D hill-climb arcade game with hand-gesture driving.

## Stack
- React + Vite frontend
- HTML Canvas game loop
- MediaPipe Hands for in-browser gesture recognition
- Express HTTP server and health endpoint
- Socket.IO connection/presence scaffold

## Requirements
Node.js 20+ and npm.

## Run locally
```bash
npm install
npm run dev
```
Open the Vite URL shown in the terminal. Camera permissions are normally available on `localhost` or HTTPS. Gesture tracking downloads MediaPipe model assets from jsDelivr, so internet access is required. Keyboard controls work without camera access.

## Production build and server
```bash
npm install
npm run build
npm start
```
Open `http://localhost:3000`. Health check: `http://localhost:3000/api/health`.

## Controls
- Open palm: accelerate
- Fist: brake
- Move hand horizontally: lean while airborne
- Keyboard: Right/D accelerate, Left/A brake, Up/W and Down/S lean, R restart

## Deployment
Deploy to a Node.js host that supports WebSockets (for example, Render or Railway). Build command: `npm install && npm run build`. Start command: `npm start`. Set `PORT` only if the platform requires it. Use HTTPS for camera permissions.

## Scope notes
This is a functional full-stack starter, not an exact commercial Hill Climb Racing clone. Socket.IO currently provides connection presence; there is no account system, cloud save, database-backed leaderboard, or shared multiplayer physics yet. Those can be added as next steps.
