import threading
from typing import Dict, List, Optional
from .models import Todo
from .schemas import TodoCreate, TodoUpdate

class TodoRepository:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        self._data: Dict[int, Todo] = {}
        self._next_id: int = 1
        self._data_lock = threading.Lock()

    def create(self, payload: TodoCreate) -> Todo:
        with self._data_lock:
            todo = Todo(id=self._next_id, title=payload.title, completed=payload.completed)
            self._data[self._next_id] = todo
            self._next_id += 1
            return todo

    def get(self, todo_id: int) -> Optional[Todo]:
        with self._data_lock:
            return self._data.get(todo_id)

    def get_all(self) -> List[Todo]:
        with self._data_lock:
            return list(self._data.values())

    def update(self, todo_id: int, payload: TodoUpdate) -> Optional[Todo]:
        with self._data_lock:
            todo = self._data.get(todo_id)
            if not todo:
                return None
            if payload.title is not None:
                todo.title = payload.title
            if payload.completed is not None:
                todo.completed = payload.completed
            return todo

    def delete(self, todo_id: int) -> bool:
        with self._data_lock:
            return self._data.pop(todo_id, None) is not None

# Export singleton‑style helper functions for fastapi routes
_repo = TodoRepository()

def create(payload: TodoCreate) -> Todo:
    return _repo.create(payload)

def get(todo_id: int) -> Optional[Todo]:
    return _repo.get(todo_id)

def get_all() -> List[Todo]:
    return _repo.get_all()

def update(todo_id: int, payload: TodoUpdate) -> Optional[Todo]:
    return _repo.update(todo_id, payload)

def delete(todo_id: int) -> bool:
    return _repo.delete(todo_id)