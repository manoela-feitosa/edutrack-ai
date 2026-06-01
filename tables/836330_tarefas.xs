table tarefas {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int user_id? {
      table = "user"
    }
  
    int disc_id? {
      table = "disciplinas"
    }
  
    text nome_tarefa? filters=trim
    text nome? filters=trim
    text status? filters=trim
    text tipo? filters=trim|lower
    date data?
    decimal nota?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id"}, {name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id"}, {name: "tipo"}]}
  ]
}
