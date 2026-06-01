// Query current user's tarefas records
query tarefas verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query tarefas {
      where = $db.tarefas.user_id == $auth.id
      sort = {tarefas.created_at: "desc"}
      return = {type: "list"}
    } as $tarefas
  }

  response = $tarefas
}
