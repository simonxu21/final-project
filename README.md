How to run the CLI tool:

python xu_simon_todo.py -h  for help

Examples:

list: 
python xu_simon_todo.py list

add: 

python xu_simon_todo.py add "Homework" "Coding Hw" "incomplete" (topic-description-status)


status change:

python xu_simon_todo.py change_status 1 "complete" (ID-Status)


update:

 python xu_simon_todo.py update 3 "buy groceries" "get fruits and meat" (ID-Topic-Description)

--list name:
 
python xu_simon_todo.py add "Homework" "Complete math homework" "incomplete" --list-name "new_todo_list.txt"

