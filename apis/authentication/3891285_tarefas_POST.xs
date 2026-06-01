// Add tarefas record
query tarefas verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    dblink {
      table = "tarefas"
    }
  }

  stack {
    db.add tarefas {
      data = {
        created_at   : "now"
        user_id      : $auth.id
        disc_id      : $input.disc_id
        nome_tarefa  : $input.nome_tarefa
        nome         : $input.nome
        status       : $input.status
        tipo         : $input.tipo
        data         : $input.data
        nota         : $input.nota
      }
    } as $tarefas
  }

  response = $tarefas
}
