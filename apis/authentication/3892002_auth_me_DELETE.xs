// Delete the authenticated user's account.
query "auth/me" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
    } as $user

    precondition ($user != null) {
      error_type = "notfound"
      error = "Usuário não encontrado."
    }

    db.del user {
      field_name = "id"
      field_value = $auth.id
    }
  }

  response = null
}
