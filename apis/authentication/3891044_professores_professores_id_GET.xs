// Get current user's professores record by ID
query "professores/{professores_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int professores_id? filters=min:1
  }

  stack {
    db.query professores {
      where = $db.professores.id == $input.professores_id && $db.professores.user_id == $auth.id
      return = {type: "single"}
    } as $professores

    precondition ($professores != null) {
      error_type = "notfound"
      error = "Professor não encontrado."
    }
  }

  response = $professores
}
