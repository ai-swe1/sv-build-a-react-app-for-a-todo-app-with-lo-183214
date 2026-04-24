const API = window.location.origin;
const todoList = document.getElementById('todo-list');
const createForm = document.getElementById('create-form');
const createBtn = document.getElementById('create-btn');
const todoInput = document.getElementById('todo-input');

// Load todo list on page load
window.addEventListener('load', async () => {
  try {
    const response = await fetch(`${API}/todos`);
    const todos = await response.json();
    renderTodoList(todos);
  } catch (error) {
    console.error(error);
    alert('Error loading todo list');
  }
});

// Create new todo item
createForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  try {
    const newTodo = { text: todoInput.value };
    const response = await fetch(`${API}/todos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTodo)
    });
    const todo = await response.json();
    renderTodoItem(todo);
    todoInput.value = '';
  } catch (error) {
    console.error(error);
    alert('Error creating new todo item');
  }
});

// Delete todo item
todoList.addEventListener('click', async (e) => {
  if (e.target.tagName === 'BUTTON') {
    try {
      const todoId = e.target.parentNode.dataset.id;
      const response = await fetch(`${API}/todos/${todoId}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        e.target.parentNode.remove();
      } else {
        alert('Error deleting todo item');
      }
    } catch (error) {
      console.error(error);
      alert('Error deleting todo item');
    }
  }
});

// Render todo list
function renderTodoList(todos) {
  todoList.innerHTML = '';
  todos.forEach((todo) => renderTodoItem(todo));
}

// Render single todo item
function renderTodoItem(todo) {
  const todoItem = document.createElement('div');
  todoItem.className = 'todo-item';
  todoItem.dataset.id = todo.id;
  if (todo.completed) {
    todoItem.classList.add('completed');
  }
  todoItem.innerHTML = `
    <span>${todo.text}</span>
    <button>Delete</button>
  `;
  todoList.appendChild(todoItem);
}