from flask import current_app


def add_to_index(index, model):
  payload = {}
  for field in model.__searchable__:
    payload[field] = getattr(model, field)
  current_app.elasticsearch.index(index=index, id=model.id, document=payload)

def remove_from_index(index, model):
  current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query):
  return current_app.elasticsearch.search(
    index=index,
    query={"multi_match":{"query":query, "fields":["*"], "fuzziness":"AUTO:3,6"}}
  )