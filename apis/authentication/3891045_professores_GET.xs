// Query current user's professores records
query professores verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query professores {
      where = $db.professores.user_id == $auth.id
      sort = {professores.created_at: "desc"}
      return = {type: "list"}
    } as $professores
  }

  response = $professores
}
