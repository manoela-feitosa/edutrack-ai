// Delete current user's disciplinas record.
query "disciplinas/{disciplinas_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int disciplinas_id? filters=min:1
  }

  stack {
    db.query disciplinas {
      where = $db.disciplinas.id == $input.disciplinas_id && $db.disciplinas.user_id == $auth.id
      return = {type: "single"}
    } as $disciplina_existente

    precondition ($disciplina_existente != null) {
      error_type = "notfound"
      error = "Disciplina não encontrada."
    }

    db.del disciplinas {
      field_name = "id"
      field_value = $input.disciplinas_id
    }
  }

  response = null
}
