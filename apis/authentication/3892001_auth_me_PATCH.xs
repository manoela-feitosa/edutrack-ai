// Update the authenticated user's account data.
query "auth/me" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    text name? filters=trim
    email email? filters=trim|lower
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

    db.patch user {
      field_name = "id"
      field_value = $auth.id
      data = {
        name : $input.name
        email: $input.email
      }|filter_null|filter_empty_text
    } as $updated_user
  }

  response = {
    id   : $updated_user.id
    name : $updated_user.name
    email: $updated_user.email
    role : $updated_user.role
  }
}
