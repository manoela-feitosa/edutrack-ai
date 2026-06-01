// Delete current user's tarefas record.
query "tarefas/{tarefas_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int tarefas_id? filters=min:1
  }

  stack {
    db.query tarefas {
      where = $db.tarefas.id == $input.tarefas_id && $db.tarefas.user_id == $auth.id
      return = {type: "single"}
    } as $tarefa_existente

    precondition ($tarefa_existente != null) {
      error_type = "notfound"
      error = "Tarefa não encontrada."
    }

    db.del tarefas {
      field_name = "id"
      field_value = $input.tarefas_id
    }
  }

  response = null
}
