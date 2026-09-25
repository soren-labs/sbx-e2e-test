(() => {
  const API_URL = 'http://localhost:8000';
  const STORAGE_KEY = 'today-tasks-offline';
  const form = document.querySelector('#add-form');
  const input = document.querySelector('#new-todo');
  const list = document.querySelector('#todo-list');
  const count = document.querySelector('#task-count');
  const emptyState = document.querySelector('#empty-state');
  const connectionStatus = document.querySelector('#connection-status');
  let todos = [];
  let online = true;

  const makeId = () => `local-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  const normalize = (todo) => ({
    id: todo.id ?? todo._id ?? makeId(),
    title: String(todo.title ?? todo.text ?? todo.name ?? ''),
    completed: Boolean(todo.completed ?? todo.done ?? todo.isCompleted),
  });

  function saveOffline() { localStorage.setItem(STORAGE_KEY, JSON.stringify(todos)); }
  function setConnection(isOnline) {
    online = isOnline;
    connectionStatus.textContent = isOnline ? 'Synced with backend' : 'Offline · saved on this device';
    connectionStatus.classList.toggle('offline', !isOnline);
  }

  async function request(path, options = {}) {
    const response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    });
    if (!response.ok) throw new Error(`Request failed: ${response.status}`);
    if (response.status === 204) return null;
    return response.json();
  }

  async function loadTodos() {
    try {
      const result = await request('/todos');
      const records = Array.isArray(result) ? result : (result.todos || result.data || []);
      todos = records.map(normalize).filter((todo) => todo.title);
      saveOffline();
      setConnection(true);
    } catch (error) {
      try { todos = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]').map(normalize); }
      catch { todos = []; }
      setConnection(false);
    }
    render();
  }

  async function addTodo(title) {
    const localTodo = normalize({ id: makeId(), title, completed: false });
    todos.unshift(localTodo);
    render();
    try {
      const result = await request('/todos', { method: 'POST', body: JSON.stringify({ title }) });
      const savedTodo = normalize(result?.todo || result || localTodo);
      todos = todos.map((todo) => todo.id === localTodo.id ? savedTodo : todo);
      setConnection(true);
    } catch { setConnection(false); }
    saveOffline();
    render();
  }

  async function updateTodo(todo, completed) {
    const previous = todo.completed;
    todo.completed = completed;
    render();
    try {
      await request(`/todos/${encodeURIComponent(todo.id)}`, { method: 'PATCH', body: JSON.stringify({ completed }) });
      setConnection(true);
    } catch { todo.completed = previous; setConnection(false); render(); }
    saveOffline();
  }

  async function deleteTodo(todo) {
    const position = todos.indexOf(todo);
    todos = todos.filter((item) => item !== todo);
    render();
    try {
      await request(`/todos/${encodeURIComponent(todo.id)}`, { method: 'DELETE' });
      setConnection(true);
    } catch { todos.splice(position, 0, todo); setConnection(false); render(); }
    saveOffline();
  }

  function render() {
    list.replaceChildren(...todos.map((todo) => {
      const item = document.createElement('li');
      item.className = `todo-item${todo.completed ? ' is-done' : ''}`;
      const label = document.createElement('label');
      label.className = 'todo-label';
      const checkbox = document.createElement('input');
      checkbox.className = 'todo-checkbox'; checkbox.type = 'checkbox'; checkbox.checked = todo.completed;
      checkbox.setAttribute('aria-label', `Mark “${todo.title}” ${todo.completed ? 'not done' : 'done'}`);
      checkbox.addEventListener('change', () => updateTodo(todo, checkbox.checked));
      const text = document.createElement('span'); text.className = 'todo-text'; text.textContent = todo.title;
      label.append(checkbox, text);
      const remove = document.createElement('button');
      remove.className = 'delete-button'; remove.type = 'button'; remove.setAttribute('aria-label', `Delete “${todo.title}”`); remove.textContent = '×';
      remove.addEventListener('click', () => deleteTodo(todo));
      item.append(label, remove);
      return item;
    }));
    const remaining = todos.filter((todo) => !todo.completed).length;
    count.textContent = `${remaining} ${remaining === 1 ? 'task' : 'tasks'} remaining`;
    emptyState.hidden = todos.length > 0;
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const title = input.value.trim();
    if (!title) return;
    input.value = '';
    addTodo(title);
    input.focus();
  });

  window.addEventListener('online', loadTodos);
  loadTodos();
})();
