# python-json-lisfy

## Usage

```bash
$ poetry install
$ poetry run json-lisfy
```

## Example

```bash
$ poetry run json-lisfy
json-lisfy> 1
(int nil 1)

json-lisfy> 2.4
(float nil 2.4)

json-lisfy> false
(symbol nil "false")

json-lisfy> {"a": 1, "b": 2}
(object nil (item nil (str nil "a") (int nil 1)) (item nil (str nil "b") (int nil 2)))

json-lisfy> [ 1, 2, "asdf",    true ]
(array nil (int nil 1) (int nil 2) (str nil "asdf") (symbol nil "true"))
```
