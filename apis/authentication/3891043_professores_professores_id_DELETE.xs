// Delete current user's professores record.
query "professores/{professores_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int professores_id? filters=min:1
  }

  stack {
    db.query professores {
      where = $db.professores.id == $input.professores_id && $db.professores.user_id == $auth.id
      return = {type: "single"}
    } as $professor_existente

    precondition ($professor_existente != null) {
      error_type = "notfound"
      error = "Professor não encontrado."
    }

    db.del professores {
      field_name = "id"
      field_value = $input.professores_id
    }
  }

  response = null
}
