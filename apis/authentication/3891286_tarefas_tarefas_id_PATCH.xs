// Edit current user's tarefas record
query "tarefas/{tarefas_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int tarefas_id? filters=min:1
    dblink {
      table = "tarefas"
    }
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

    db.patch tarefas {
      field_name = "id"
      field_value = $input.tarefas_id
      data = {
        disc_id      : $input.disc_id
        nome_tarefa  : $input.nome_tarefa
        nome         : $input.nome
        status       : $input.status
        tipo         : $input.tipo
        data         : $input.data
        nota         : $input.nota
      }|filter_null|filter_empty_text
    } as $tarefas
  }

  response = $tarefas
}
