// Edit current user's disciplinas record
query "disciplinas/{disciplinas_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int disciplinas_id? filters=min:1
    dblink {
      table = "disciplinas"
    }
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

    db.patch disciplinas {
      field_name = "id"
      field_value = $input.disciplinas_id
      data = {
        prof_id        : $input.prof_id
        nome_disciplina: $input.nome_disciplina
      }|filter_null|filter_empty_text
    } as $model
  }

  response = $model
}
