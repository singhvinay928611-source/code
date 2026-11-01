import express from 'express';
import { createServer } from 'node:http';
import { Server } from 'socket.io';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, { cors: { origin: true } });
const port = process.env.PORT || 3000;
app.use(express.static(path.join(__dirname, 'dist')));
app.get('/api/health', (_req, res) => res.json({ ok: true, game: 'Gesture Hill Climb', time: new Date().toISOString() }));
io.on('connection', socket => {
  io.emit('online', io.engine.clientsCount);
  socket.on('disconnect', () => io.emit('online', io.engine.clientsCount));
});
app.get('*', (_req, res) => res.sendFile(path.join(__dirname, 'dist', 'index.html')));
httpServer.listen(port, '0.0.0.0', () => console.log(`Gesture Hill Climb server listening on ${port}`));