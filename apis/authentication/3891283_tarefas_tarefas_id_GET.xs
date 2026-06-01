// Get current user's tarefas record by ID
query "tarefas/{tarefas_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int tarefas_id? filters=min:1
  }

  stack {
    db.query tarefas {
      where = $db.tarefas.id == $input.tarefas_id && $db.tarefas.user_id == $auth.id
      return = {type: "single"}
    } as $tarefas

    precondition ($tarefas != null) {
      error_type = "notfound"
      error = "Tarefa não encontrada."
    }
  }

  response = $tarefas
}
