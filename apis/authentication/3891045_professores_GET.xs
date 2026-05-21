// Query all professores records
query professores verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query professores {
      return = {type: "list"}
    } as $professores
  }

  response = $professores
}