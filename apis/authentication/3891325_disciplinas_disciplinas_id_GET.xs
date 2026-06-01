// Get current user's disciplinas record by ID
query "disciplinas/{disciplinas_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int disciplinas_id? filters=min:1
  }

  stack {
    db.query disciplinas {
      where = $db.disciplinas.id == $input.disciplinas_id && $db.disciplinas.user_id == $auth.id
      return = {type: "single"}
    } as $model

    precondition ($model != null) {
      error_type = "notfound"
      error = "Disciplina não encontrada."
    }
  }

  response = $model
}
