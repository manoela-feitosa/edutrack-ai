// Query current user's disciplinas records
query disciplinas verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query disciplinas {
      where = $db.disciplinas.user_id == $auth.id
      sort = {disciplinas.created_at: "desc"}
      return = {type: "list"}
    } as $model
  }

  response = $model
}
