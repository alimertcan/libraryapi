
schema_book = {
    "type": "object",
"properties" : {
    "is_taken": { "type": "boolean" },
    "name": {"type" : "string"},
},
"required": ["name"]
}

schema_take_book = {
"type": "object",
"properties" : {
    "book_name": { "type": "string" },
    "user": {"type" : "string"},
},
"required": ["book_name", "user"]
}
schema_drop_book = {
"type": "object",
"properties" : {
    "book_name": { "type": "string" },
    "user": {"type" : "string"},
},
"required": ["book_name", "user"]
}