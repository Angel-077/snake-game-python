const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const bestScoreEl = document.getElementById('best-score');
const startBtn = document.getElementById('start-btn');

const gridSize = 21;
const tileSize = canvas.width / gridSize;

let snake;
let direction;
let nextDirection;
let food;
let score;
let bestScore = Number(localStorage.getItem('snake-best-score') || 0);
let animationId;
let isRunning = false;

function resetGame() {
  snake = [
    { x: 10, y: 10 },
    { x: 9, y: 10 },
    { x: 8, y: 10 }
  ];
  direction = { x: 1, y: 0 };
  nextDirection = { x: 1, y: 0 };
  score = 0;
  scoreEl.textContent = '0';
  placeFood();
  draw();
}

function placeFood() {
  food = {
    x: Math.floor(Math.random() * gridSize),
    y: Math.floor(Math.random() * gridSize)
  };

  for (const segment of snake) {
    if (segment.x === food.x && segment.y === food.y) {
      placeFood();
      return;
    }
  }
}

function update() {
  direction = nextDirection;

  const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };

  if (
    head.x < 0 ||
    head.x >= gridSize ||
    head.y < 0 ||
    head.y >= gridSize ||
    snake.some((segment) => segment.x === head.x && segment.y === head.y)
  ) {
    endGame();
    return;
  }

  snake.unshift(head);

  if (head.x === food.x && head.y === food.y) {
    score += 10;
    scoreEl.textContent = String(score);
    if (score > bestScore) {
      bestScore = score;
      localStorage.setItem('snake-best-score', String(bestScore));
      bestScoreEl.textContent = String(bestScore);
    }
    placeFood();
  } else {
    snake.pop();
  }
}

function draw() {
  ctx.fillStyle = '#020817';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      ctx.strokeStyle = 'rgba(148, 163, 184, 0.12)';
      ctx.strokeRect(i * tileSize, j * tileSize, tileSize, tileSize);
    }
  }

  ctx.fillStyle = '#fbbf24';
  ctx.fillRect(food.x * tileSize + 4, food.y * tileSize + 4, tileSize - 8, tileSize - 8);

  snake.forEach((segment, index) => {
    ctx.fillStyle = index === 0 ? '#34d399' : '#10b981';
    ctx.fillRect(segment.x * tileSize + 1, segment.y * tileSize + 1, tileSize - 2, tileSize - 2);
  });
}

function gameLoop() {
  if (!isRunning) return;

  update();
  draw();

  if (isRunning) {
    animationId = setTimeout(gameLoop, 120);
  }
}

function startGame() {
  isRunning = true;
  resetGame();
  startBtn.textContent = 'Restart game';
  if (animationId) clearTimeout(animationId);
  gameLoop();
}

function endGame() {
  isRunning = false;
  if (animationId) clearTimeout(animationId);
  draw();
  ctx.fillStyle = 'rgba(15, 23, 42, 0.7)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#e5e7eb';
  ctx.textAlign = 'center';
  ctx.font = 'bold 26px Arial';
  ctx.fillText('Game Over', canvas.width / 2, canvas.height / 2 - 10);
  ctx.font = '18px Arial';
  ctx.fillText('Press Start to play again', canvas.width / 2, canvas.height / 2 + 22);
}

function setDirection(newDir) {
  const isOpposite = newDir.x === -direction.x && newDir.y === -direction.y;
  if (!isOpposite) {
    nextDirection = newDir;
  }
}

document.addEventListener('keydown', (event) => {
  const key = event.key.toLowerCase();
  if (['arrowup', 'w'].includes(key)) setDirection({ x: 0, y: -1 });
  if (['arrowdown', 's'].includes(key)) setDirection({ x: 0, y: 1 });
  if (['arrowleft', 'a'].includes(key)) setDirection({ x: -1, y: 0 });
  if (['arrowright', 'd'].includes(key)) setDirection({ x: 1, y: 0 });

  if (key === ' ' && !isRunning) {
    startGame();
  }
});

startBtn.addEventListener('click', startGame);

bestScoreEl.textContent = String(bestScore);
resetGame();
