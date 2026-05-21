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
        user_id: $auth.id
        disc_id: $input.disc_id
        nota   : $input.nota
      }
    } as $tarefas
  }

  response = $tarefas
}